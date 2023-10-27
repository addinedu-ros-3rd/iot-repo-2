import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from datetime import datetime as dt

import re
import time
import serial
import mysql.connector
import configparser

from_class = uic.loadUiType("conveyer.ui")[0]

class WindowClass(QMainWindow, from_class) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("System Manager")
        
        self.minInTime = self.inTimeStart.dateTime()
        self.maxInTime = self.inTimeEnd.dateTime()
        self.minUpdateTime = self.updateTimeStart.dateTime()
        self.maxUpdateTime = self.updateTimeEnd.dateTime()
        self.minOutTime = self.outTimeStart.dateTime()
        self.maxOutTime = self.outTimeEnd.dateTime()
        
        self.btnStart.setEnabled(False)
        # self.initBelt()
        # self.btnStart.clicked.connect(self.controlBelt)
        
        self.initDatabase()
        self.setCombo()
        # self.setDateFromDatabase()
        
        self.statusCombo.currentIndexChanged.connect(self.setDateSelectable)
        
        self.btnFilterReset.clicked.connect(self.resetDate)
        self.btnSearch.clicked.connect(self.search)
        
        
    def initBelt(self):
        self.isBeltRunning = False

        try:
            self.ser = serial.Serial("/dev/ttyACM0", 9600)
            time.sleep(1)
        except:
            print("Device cannot be found.")
            sys.exit(0)


    def controlBelt(self):
        if self.isBeltRunning == False:
            self.ser.write(b'1')
            self.isBeltRunning = True
            self.btnStart.setText("Stop")
        else:
            self.ser.write(b'0')
            self.isBeltRunning = False
            self.btnStart.setText("Start")
            
            
    def initDatabase(self):
        config = configparser.ConfigParser()
        config.read('../config.ini')
        dev = config['dev']
        
        try:
            self.remote = mysql.connector.connect(
                user = dev['user'],
                password = dev['password'],
                port = dev['port'],
                host = dev['host'],
                database = dev['database'])
            self.mycursor = self.remote.cursor(buffered=True)
        except Exception as e:
            print("Failed to connect database", e)
            
            
    def resetDate(self):
        self.inTimeStart.setDateTime(self.minInTime)
        self.inTimeEnd.setDateTime(self.maxInTime)
        self.updateTimeStart.setDateTime(self.minUpdateTime)
        self.updateTimeEnd.setDateTime(self.maxUpdateTime)
        self.outTimeStart.setDateTime(self.minOutTime)
        self.outTimeEnd.setDateTime(self.maxOutTime)
        self.categoryCombo.setCurrentText("전체")
        self.rfidInput.clear()
        
        
    def setCombo(self):
        self.sql = "select ko_name from category order by id"
        self.mycursor.execute(self.sql)
        categoryList = self.mycursor.fetchall()
        
        self.categoryCombo.addItem("전체")
        for item in categoryList:
            self.categoryCombo.addItem(item[0])
            
        self.statusCombo.addItem("전체")
        self.statusCombo.addItem("미입고")
        self.statusCombo.addItem("입고")
        self.statusCombo.addItem("출고")


    def setDateSelectable(self):
        status = self.statusCombo.currentText()
        
        if status == "미입고":
            self.inTimeStart.setEnabled(False)
            self.inTimeEnd.setEnabled(False)
            self.updateTimeStart.setEnabled(False)
            self.updateTimeEnd.setEnabled(False)
            self.outTimeStart.setEnabled(False)
            self.outTimeEnd.setEnabled(False)
        else:  # 출고
            self.inTimeStart.setEnabled(True)
            self.inTimeEnd.setEnabled(True)
            self.updateTimeStart.setEnabled(True)
            self.updateTimeEnd.setEnabled(True)
            self.outTimeStart.setEnabled(True)
            self.outTimeEnd.setEnabled(True)
            

            
    def search(self):
        self.rfid = self.rfidInput.toPlainText()
        
        if self.rfid != "":
            pattern = re.compile("([\w]{2})\s([\w]{2})\s([\w]{2})\s([\w]{2})")
            
            if pattern.match(self.rfid) == None:
                self.rfidInputHelp.setText("RFID 형식은 [00 00 00 0D]입니다.")
                self.rfidInputHelp.setStyleSheet("Color : red")
            else:
                self.rfidInputHelp.setText("")
                self.selectFromDatabase()
                
        else:
            self.rfidInputHelp.setText("")
            self.selectFromDatabase()
            
    
    def selectFromDatabase(self):
        self.table.setRowCount(0)
        
        inTimeStart = self.inTimeStart.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        inTimeEnd = self.inTimeEnd.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        updateTimeStart = self.updateTimeStart.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        updateTimeEnd = self.updateTimeEnd.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        outTimeStart = self.outTimeStart.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        outTimeEnd = self.outTimeEnd.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        
        self.sql = ("select id, uid, \
                            (select ko_name from category where id=category_id) as category_name, \
                            in_time, \
                            section_update_time, \
                            out_time, \
                            tag_info \
                    from rfid \
                    where 1=1 \
                    AND (in_time IS NULL OR in_time >= timestamp('" + inTimeStart + "')) \
                    AND (in_time IS NULL OR in_time <= timestamp('" + inTimeEnd + "')) \
                    AND (section_update_time IS NULL OR section_update_time >= timestamp('" + updateTimeStart + "')) \
                    AND (section_update_time IS NULL OR section_update_time <= timestamp('" + updateTimeEnd + "')) \
                    AND (out_time IS NULL OR out_time >= timestamp('" + outTimeStart + "')) \
                    AND (out_time IS NULL OR out_time <= timestamp('" + outTimeEnd + "'))")
        
        if self.rfid != "":
            self.sql += " AND uid = '" + self.rfid + "'"
        if self.categoryCombo.currentText() != "전체":
            self.sql += " AND category_id = (select id from category where ko_name = '" + self.categoryCombo.currentText() + "')"
        
        if self.statusCombo.currentText() == "미입고":
            self.sql += " AND in_time IS NULL"
        elif self.statusCombo.currentText() == "입고":
            self.sql += " AND (in_time IS NOT NULL) AND (out_time IS NULL)"
        elif self.statusCombo.currentText() == "출고":
            self.sql += " AND out_time IS NOT NULL"
            
        # print(self.sql)
        
        self.mycursor.execute(self.sql)
        result = self.mycursor.fetchall()
        
        for row in result:
            resultRow = self.table.rowCount()
            self.table.insertRow(resultRow)
            for i, v in enumerate(row):
                self.table.setItem(resultRow, i, QTableWidgetItem(str(v)))
        
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()
    sys.exit(app.exec_())