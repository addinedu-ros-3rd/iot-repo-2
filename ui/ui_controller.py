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
        
        # self.initBelt()
        self.btnStart.clicked.connect(self.controlBelt)
        
        self.initDatabase()
        # self.setFromDatabase()
        
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

    def setFromDatabase(self):
        self.sql = """select DATE_FORMAT(min(in_time), "%Y-%m-%d %H:%i:%s") from rfid"""
        self.mycursor.execute(self.sql)
        minInTimeStr = self.mycursor.fetchone()
        self.minInTime = QDateTime.fromString(minInTimeStr[0], "yyyy-MM-dd hh:mm:ss")
        
        self.sql = """select DATE_FORMAT(max(in_time), "%Y-%m-%d %H:%i:%s") from rfid"""
        self.mycursor.execute(self.sql)
        maxInTimeStr = self.mycursor.fetchone()
        self.maxInTime = QDateTime.fromString(maxInTimeStr[0], "yyyy-MM-dd hh:mm:ss")
        
        self.sql = """select DATE_FORMAT(min(section_update_time), "%Y-%m-%d %H:%i:%s") from rfid"""
        self.mycursor.execute(self.sql)
        minUpdateTimeStr = self.mycursor.fetchone()
        self.minUpdateTime = QDateTime.fromString(minUpdateTimeStr[0], "yyyy-MM-dd hh:mm:ss")
        
        self.sql = """select DATE_FORMAT(max(section_update_time), "%Y-%m-%d %H:%i:%s") from rfid"""
        self.mycursor.execute(self.sql)
        maxUpdateTimeStr = self.mycursor.fetchone()
        self.maxUpdateTime = QDateTime.fromString(maxUpdateTimeStr[0], "yyyy-MM-dd hh:mm:ss")
        
        self.sql = """select DATE_FORMAT(min(out_time), "%Y-%m-%d %H:%i:%s") from rfid"""
        self.mycursor.execute(self.sql)
        minOutTimeStr = self.mycursor.fetchone()
        self.minOutTime = QDateTime.fromString(minOutTimeStr[0], "yyyy-MM-dd hh:mm:ss")
        
        self.sql = """select DATE_FORMAT(max(out_time), "%Y-%m-%d %H:%i:%s") from rfid"""
        self.mycursor.execute(self.sql)
        maxOutTimeStr = self.mycursor.fetchone()
        self.maxOutTime = QDateTime.fromString(maxOutTimeStr[0], "yyyy-MM-dd hh:mm:ss")
        
        self.inTimeStart.setDateTimeRange(self.minInTime, self.maxInTime)
        self.inTimeEnd.setDateTimeRange(self.minInTime, self.maxInTime)
        self.updateTimeStart.setDateTimeRange(self.minUpdateTime, self.maxUpdateTime)
        self.updateTimeEnd.setDateTimeRange(self.minUpdateTime, self.maxUpdateTime)
        self.outTimeStart.setDateTimeRange(self.minOutTime, self.maxOutTime)
        self.outTimeEnd.setDateTimeRange(self.minOutTime, self.maxOutTime)
        
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

        self.statusCombo.currentIndexChanged.connect(self.change)


    def change(self, index):
        if index == 1:
            self.inTimeStart.setDisabled(True)
            self.inTimeEnd.setDisabled(True)
            self.updateTimeStart.setDisabled(True)
            self.updateTimeEnd.setDisabled(True)
            self.outTimeStart.setDisabled(True)
            self.outTimeEnd.setDisabled(True)
        elif index == 0:
            self.inTimeStart.setEnabled(True)
            self.inTimeEnd.setEnabled(True)
            self.updateTimeStart.setEnabled(True)
            self.updateTimeEnd.setEnabled(True)
            self.outTimeStart.setEnabled(True)
            self.outTimeEnd.setEnabled(True)
        elif index == 1:
            self.inTimeStart.setEnabled(True)
            self.inTimeEnd.setEnabled(True)
            self.updateTimeStart.setEnabled(True)
            self.updateTimeEnd.setEnabled(True)
            self.outTimeStart.setEnabled(True)
            self.outTimeEnd.setEnabled(True)
        elif index == 2:
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
                            out_time \
                    from rfid \
                    where 1=1 \
                    AND in_time >= timestamp('" + inTimeStart + "') \
                    AND in_time <= timestamp('" + inTimeEnd + "') \
                    AND section_update_time >= timestamp('" + updateTimeStart + "') \
                    AND section_update_time <= timestamp('" + updateTimeEnd + "') \
                    AND out_time >= timestamp('" + outTimeStart + "') \
                    AND out_time <= timestamp('" + outTimeEnd + "')")
        
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
            
        print(self.sql)
        
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
    