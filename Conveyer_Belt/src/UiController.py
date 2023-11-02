from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from PyQt5.QtCore import QThread, pyqtSignal
from DB import *

import sys
import datetime
import cv2
import time
import re
import time
import serial
import logging


from_class = uic.loadUiType("Conveyor.ui")[0]

class Camera(QThread):
    update = pyqtSignal()

    def __init__(self, sec=0, parent=None):
        super().__init__()
        self.main = parent
        self.running = True


    def run(self):
        count = 0
        while self.running == True:
            self.update.emit()
            time.sleep(0.05)

    def stop(self):
        self.running == False

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
        
        self.setCombo()
        # self.setDateFromDatabase()
        
        self.statusCombo.currentIndexChanged.connect(self.setDateSelectable)
        
        self.btnFilterReset.clicked.connect(self.reset)
        self.btnSearch.clicked.connect(self.search)

        self.isCameraOn = False
        self.isRecStart = False
        self.btnRecord.hide()
        self.btnCapture.hide()

        self.pixmap = QPixmap()
        self.image = None

        self.camera = Camera(self)
        self.camera.deamon = True

        self.record =Camera(self)
        self.record.deamon = True 

        self.play = Camera(self)
        self.play.daemon = True

        self.btnCamera.clicked.connect(self.clickCamera)
        self.camera.update.connect(self.updateCamera)
        self.btnRecord.clicked.connect(self.clickRecord)
        self.record.update.connect(self.updateRecording)
        self.btnCapture.clicked.connect(self.capture)

        self.count = 0
        
        
    def initBelt(self):
        self.isBeltRunning = False

        try:
            self.ser = serial.Serial("/dev/ttyACM0", 9600)
            time.sleep(1)
        except:
            logging.error("Device cannot be found.")
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
            
            
    def reset(self):
        self.inTimeStart.setDateTime(self.minInTime)
        self.inTimeEnd.setDateTime(self.maxInTime)
        self.updateTimeStart.setDateTime(self.minUpdateTime)
        self.updateTimeEnd.setDateTime(self.maxUpdateTime)
        self.outTimeStart.setDateTime(self.minOutTime)
        self.outTimeEnd.setDateTime(self.maxOutTime)
        
        self.inTimeStart.setEnabled(True)
        self.inTimeEnd.setEnabled(True)
        self.updateTimeStart.setEnabled(True)
        self.updateTimeEnd.setEnabled(True)
        self.outTimeStart.setEnabled(True)
        self.outTimeEnd.setEnabled(True)

        self.categoryCombo.setCurrentText("전체")
        self.statusCombo.setCurrentText("전체")
        
        self.rfidInput.clear()
        
        
    def setCombo(self):
        db = DB()
        
        self.sql = "select ko_name from category order by id"
        db.execute(self.sql)
        categoryList = db.fetchAll()
        db.disconnect()
        
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
            pattern = re.compile("([\da-zA-Z]{2})\s([\da-zA-Z]{2})\s([\da-zA-Z]{2})\s([\da-zA-Z]{2})")
            
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
        
        db = DB()
        
        self.sql = ("select id, uid, tag_info, \
                            (select ko_name from category where id=category_id) as category_name, \
                            in_time, \
                            section_update_time, \
                            out_time \
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
            
        logging.info(self.sql)
        
        db.execute(self.sql)
        result = db.fetchAll()
        db.disconnect()
        
        for row in result:
            resultRow = self.table.rowCount()
            self.table.insertRow(resultRow)
            for i, v in enumerate(row):
                self.table.setItem(resultRow, i, QTableWidgetItem(str(v)))
        
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        

    def capture(self):
        self.now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.now + ".png"

        cv2.imwrite(filename, cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
    
    
    def updateRecording(self):
        self.writer.write(cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR))
    
    
    def clickRecord(self):
        if self.isRecStart == False:
            self.btnRecord.setText("Rec Stop")
            self.isRecStart = True

            self.recordingStart()
            
        else:
            self.btnRecord.setText("Rec Start")
            self.isRecStart = False

            self.recordingStop()


    def recordingStart(self):
        self.record.running = True
        self.record.start()

        self.now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.now + ".avi"
        self.fourcc = cv2.VideoWriter_fourcc(*'VP80')

        w = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.writer = cv2.VideoWriter(filename, self.fourcc, 20.0, (w, h))


    def recordingStop(self):
        self.record.running = False

        if self.isRecStart == True:
            self.writer.release()
    
    
    def clickCamera(self):
        if self.isCameraOn == False:
            self.isCameraOn = True
            self.btnCamera.setText("Camera Off")
            self.btnRecord.show()
            self.btnCapture.show()
            
            self.cameraStart()
        
        else:
            self.isCameraOn = False
            self.btnCamera.setText("Camera On")
            self.btnRecord.hide()
            self.btnCapture.hide()
            
            self.cameraStop()
            self.recordingStop()
    
    
    def cameraStart(self):
        self.camera.running = True
        self.camera.start()
        self.video = cv2.VideoCapture(-1)


    def cameraStop(self):
        self.camera.running = False
        self.video.release()
    
    
    def updateCamera(self):
        retval, image = self.video.read()
        if retval:
            self.image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            h, w, c = self.image.shape
            qimage = QImage(self.image.data, w, h, w*c, QImage.Format_RGB888)

            self.pixmap = self.pixmap.fromImage(qimage)
            self.pixmap = self.pixmap.scaled(self.label.width(), self.label.height())

            self.label.setPixmap(self.pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()
    sys.exit(app.exec_())