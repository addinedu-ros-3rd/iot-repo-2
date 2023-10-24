import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
import time
import serial

from_class = uic.loadUiType("./ui/conveyer.ui")[0]

class WindowClass(QMainWindow, from_class) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Camera")
        
        self.isBeltRunning = False

        try:
            self.ser = serial.Serial("/dev/ttyACM0", 9600)
            time.sleep(1)
        except:
            print("Device cannot be found.")
            sys.exit(0)
        
        self.btnStart.clicked.connect(self.startBelt)

    def startBelt(self):
        if self.isBeltRunning == False:
            self.ser.write(b'1')
            self.isBeltRunning = True
            self.btnStart.setText("Stop")
        else:
            self.ser.write(b'0')
            self.isBeltRunning = False
            self.btnStart.setText("Start")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()
    sys.exit(app.exec_())