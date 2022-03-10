#!/usr/bin/env python
from PyQt5 import QtWidgets, QtGui, QtCore,  uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QThread
import socket
import os
import threading
import sys, time


HOST = 'localhost'
PORT = 5005


server_created_flag = False
global server
global conn

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        global server_created_flag
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(600,800)
        MainWindow.setWindowTitle('Server')
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
    
        self.centralwidget.setStyleSheet("background-color:white;")
        
        # Start server button
        self.server_start = QtWidgets.QPushButton(MainWindow)
        self.server_start.setText("Start server")
        self.server_start.setStyleSheet("font: bold; font-size: 15px;")
        self.server_start.setGeometry(QtCore.QRect(200, 170, 200, 40))
        self.server_start.clicked.connect(self.start_server)

        ### Set DTC

        # Set DTC1
        self.dtc1 = QtWidgets.QPushButton(MainWindow)
        self.dtc1 .setText("Set DTC1 active")
        self.dtc1 .setStyleSheet("font: bold; font-size: 15px;")
        self.dtc1 .setGeometry(QtCore.QRect(70, 300, 200, 40))
        self.dtc1.clicked.connect(lambda : self.set_dtc1(7,0.1))

        # Set DTC2
        self.dtc2 = QtWidgets.QPushButton(MainWindow)
        self.dtc2 .setText("Set DTC2 active")
        self.dtc2 .setStyleSheet("font: bold; font-size: 15px;")
        self.dtc2 .setGeometry(QtCore.QRect(70, 370, 200, 40))
        self.dtc2.clicked.connect(lambda : self.set_dtc2(6,0.1))

        # Set DTC3
        self.dtc3= QtWidgets.QPushButton(MainWindow)
        self.dtc3 .setText("Set DTC3 active")
        self.dtc3 .setStyleSheet("font: bold; font-size: 15px;")
        self.dtc3 .setGeometry(QtCore.QRect(70, 440, 200, 40))
        self.dtc3.clicked.connect(lambda : self.set_dtc3(5,0.1))

        # Set DTC4
        self.dtc4 = QtWidgets.QPushButton(MainWindow)
        self.dtc4 .setText("Set DTC4 active")
        self.dtc4 .setStyleSheet("font: bold; font-size: 15px;")
        self.dtc4 .setGeometry(QtCore.QRect(70, 510, 200, 40))
        self.dtc4.clicked.connect(lambda : self.set_dtc4(4,0.1))

        ### LEDS
        # Led 1
        self.led1_state = QtWidgets.QLabel(MainWindow)
        self.led1_state.setGeometry(QtCore.QRect(330, 300, 40,40))

        # Led 2
        self.led2_state = QtWidgets.QLabel(MainWindow)
        self.led2_state.setGeometry(QtCore.QRect(330, 370, 40,40))

        #Led 3
        self.led3_state = QtWidgets.QLabel(MainWindow)
        self.led3_state.setGeometry(QtCore.QRect(330, 441, 40,40))

        # Led 4
        self.led4_state = QtWidgets.QLabel(MainWindow)
        self.led4_state.setGeometry(QtCore.QRect(330, 510, 40,40))

        # Set all DTC's
        self.set_all_dtc = QtWidgets.QPushButton(MainWindow)
        self.set_all_dtc .setText("Set all DTC")
        self.set_all_dtc .setStyleSheet("font: bold; font-size: 15px;")
        self.set_all_dtc .setGeometry(QtCore.QRect(70, 580, 200, 40))
        self.set_all_dtc.clicked.connect(self.set_all)
 
        # Start server label
        self.server_label = QtWidgets.QLabel(self.centralwidget)
        self.server_label.setGeometry(QtCore.QRect(200, 210, 200, 40))
        self.server_label.setStyleSheet("font:bold;font-size: 15px;qproperty-alignment: AlignCenter;")
        
        # Continental image
        self.conti_label = QtWidgets.QLabel(self.centralwidget)
        self.conti_label.setGeometry(QtCore.QRect(110, 30, 400, 100))
        self.conti_label.setStyleSheet("qproperty-alignment: AlignCenter;")
        continental = QtGui.QImage(QtGui.QImageReader('./rsz_conti.png').read())
        self.conti_label.setPixmap(QtGui.QPixmap(continental))
        
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.show()

############################### EXERCISE 0 ###############################
    def start_server(self):
        self.set_all_dtc.setText('Set all DTC')
      
        self.dtc1 .setText("Set DTC1 active")
        self.dtc2 .setText("Set DTC2 active")
        self.dtc3 .setText("Set DTC3 active")
        self.dtc4 .setText("Set DTC4 active")

        self.led1_state.setStyleSheet('')
        self.led2_state.setStyleSheet('')
        self.led3_state.setStyleSheet('')
        self.led4_state.setStyleSheet('')
        ''' Complete with necessary code'''

############################### EXERCISE 1 ###############################
    def recv_handler(self,stop_event):
        pass
         
    def recv(self):
        self.stop_event = threading.Event()
        self.c_thread=threading.Thread(target=self.recv_handler, args=(self.stop_event,))
        self.c_thread.start()


############################### EXERCISE 2 ###############################
    # DTC1
    def set_dtc1(self,led,bright):
        pass

    # DTC2
    def set_dtc2(self,led,bright):
        pass

    # DTC3
    def set_dtc3(self,led,bright):
        pass

    # DTC4
    def set_dtc4(self,led,bright):
        pass

    def set_all(self):
        pass

############################### EXERCISE 3 ###############################          
    def read_dtc1(self,data):
        pass
        
    
    def read_dtc2(self,data):
        pass


    def read_dtc3(self,data):
        pass


    def read_dtc4(self,data):
        pass

############################### EXERCISE 4 ###############################
    def set_led0(self,data):
       pass


    def set_led1(self,data):
        pass


    def set_led2(self,data):
        pass


    def set_led3(self,data):
        pass

##########################################################################
      
            
class MyWindow(QtWidgets.QMainWindow):
    def closeEvent(self,event):
        result = QtWidgets.QMessageBox.question(self,
                      "Confirm Exit",
                      "Are you sure you want to exit ?",
                      QtWidgets.QMessageBox.Yes| QtWidgets.QMessageBox.No)        

        
        if result == QtWidgets.QMessageBox.Yes:
            event.accept()
        elif result == QtWidgets.QMessageBox.No:
            event.ignore()

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

def kill_proc_tree(pid, including_parent=True):    
    parent = psutil.Process(pid)
    if including_parent:
        parent.kill()

def main():
    global server_created_flag
    import sys
    global app
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MyWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.center()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

me = os.getpid()
kill_proc_tree(me)
    
