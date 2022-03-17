# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import socket
import threading
import sys, time
import _pickle as pk

HOST = 'localhost'
PORT = 5005
client = 0



led0_flag = False
led1_flag = False
led2_flag = False
led3_flag = False

class Ui_MainWindow(object):
    server = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(658, 500)
        MainWindow.setMinimumSize(QtCore.QSize(658, 500))
        MainWindow.setMaximumSize(QtCore.QSize(658, 500))
        self.logo_img = QtGui.QPixmap('./rsz_conti.png')
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setWindowTitle('Client')
        self.centralwidget.setObjectName("centralwidget")
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(150, 20, 400, 100))
        self.logo.setObjectName("logo")
        self.connected_msg = QtWidgets.QLabel(self.centralwidget)
        self.connected_msg.setGeometry(QtCore.QRect(292, 175, 85, 30))
        self.connected_msg.setObjectName("connected_msg")
        self.connected_msg.setStyleSheet("font: bold; color: green")
        self.not_diag_mode = QtWidgets.QLabel(self.centralwidget)
        self.not_diag_mode.setGeometry(QtCore.QRect(272, 187, 120, 30))
        self.not_diag_mode.setObjectName("not_diag_mode")
        self.not_diag_mode.setStyleSheet("font: bold; color: red")
        self.not_diag_mode.setVisible(False)
        self.diagMode = QtWidgets.QPushButton(self.centralwidget)
        self.diagMode.setGeometry(QtCore.QRect(185, 210, 131, 41))
        self.diagMode.setObjectName("diagMode")
        self.diagMode.clicked.connect(self.diag)
        self.diagMode.setEnabled(False)
        self.diagMode_off = QtWidgets.QPushButton(self.centralwidget)
        self.diagMode_off.setGeometry(QtCore.QRect(325, 210, 131, 41))
        self.diagMode_off.setObjectName("diagMode")
        self.diagMode_off.setEnabled(False)
        self.diagMode_off.clicked.connect(self.stop_diag)

        self.set_led0 = QtWidgets.QPushButton(self.centralwidget)
        self.set_led0.setGeometry(QtCore.QRect(30, 310, 81, 31))
        self.set_led0.clicked.connect(self.set_led0_flags)

        self.set_led1 = QtWidgets.QPushButton(self.centralwidget)
        self.set_led1.setGeometry(QtCore.QRect(30, 350, 81, 31))
        self.set_led1.clicked.connect(self.set_led1_flags)

        self.set_led2 = QtWidgets.QPushButton(self.centralwidget)
        self.set_led2.setGeometry(QtCore.QRect(30, 390, 81, 31))
        self.set_led2.clicked.connect(self.set_led2_flags)


        self.set_led3 = QtWidgets.QPushButton(self.centralwidget)
        self.set_led3.setGeometry(QtCore.QRect(30, 430, 81, 31))
        self.set_led3.clicked.connect(self.set_led3_flags)


        self.led0_state = QtWidgets.QLabel(self.centralwidget)
        self.led0_state.setGeometry(QtCore.QRect(140, 313, 25, 25))
        self.led0_state.setVisible(False)

        self.led1_state = QtWidgets.QLabel(self.centralwidget)
        self.led1_state.setGeometry(QtCore.QRect(140, 353, 25, 25))
        self.led1_state.setVisible(False)

        self.led2_state = QtWidgets.QLabel(self.centralwidget)
        self.led2_state.setGeometry(QtCore.QRect(140, 393, 25, 25))
        self.led2_state.setVisible(False)
        
        self.led3_state = QtWidgets.QLabel(self.centralwidget)
        self.led3_state.setGeometry(QtCore.QRect(140, 433, 25, 25))
        self.led3_state.setVisible(False)

        self.set_led_title = QtWidgets.QLabel(self.centralwidget)
        self.set_led_title.setGeometry(QtCore.QRect(75, 270, 92, 21))
        self.set_led_title.setObjectName("set_led_title")
        self.set_led_title.setStyleSheet("font:bold; font-size:11px;")
        self.read_dtc_title = QtWidgets.QLabel(self.centralwidget)
        self.read_dtc_title.setGeometry(QtCore.QRect(470, 270, 101, 20))
        self.read_dtc_title.setObjectName("read_dtc_title")
        self.read_dtc_title.setStyleSheet("font:bold; font-size:11px;")

        self.dtc1 = QtWidgets.QPushButton(self.centralwidget)
        self.dtc1.setGeometry(QtCore.QRect(460, 310, 81, 31))
        self.dtc1.clicked.connect(lambda : self.get_dtc_state('01'))

        self.dtc2 = QtWidgets.QPushButton(self.centralwidget)
        self.dtc2.setGeometry(QtCore.QRect(460, 350, 81, 31))
        self.dtc2.clicked.connect(lambda : self.get_dtc_state('02'))

        self.dtc3 = QtWidgets.QPushButton(self.centralwidget)
        self.dtc3.setGeometry(QtCore.QRect(460, 390, 81, 31))
        self.dtc3.clicked.connect(lambda : self.get_dtc_state('03'))

        self.dtc4 = QtWidgets.QPushButton(self.centralwidget)
        self.dtc4.setGeometry(QtCore.QRect(460, 430, 81, 31))
        self.dtc4.clicked.connect(lambda : self.get_dtc_state('04'))
        

        self.dtc1_state = QtWidgets.QLabel(self.centralwidget)
        self.dtc1_state.setGeometry(QtCore.QRect(570, 315, 65, 20))
        self.dtc1_state.setText('Unknown')
        self.dtc1_state.setStyleSheet('font:bold; color: blue')

        self.dtc2_state = QtWidgets.QLabel(self.centralwidget)
        self.dtc2_state.setGeometry(QtCore.QRect(570, 355, 65, 20))
        self.dtc2_state.setText('Unknown')
        self.dtc2_state.setStyleSheet('font:bold; color: blue')

        self.dtc3_state = QtWidgets.QLabel(self.centralwidget)
        self.dtc3_state.setGeometry(QtCore.QRect(570, 395, 65, 20))
        self.dtc3_state.setText('Unknown')
        self.dtc3_state.setStyleSheet('font:bold; color: blue')

        self.dtc4_state = QtWidgets.QLabel(self.centralwidget)
        self.dtc4_state.setGeometry(QtCore.QRect(570, 435, 65, 20))
        self.dtc4_state.setText('Unknown')
        self.dtc4_state.setStyleSheet('font:bold; color: blue')

        self.connect = QtWidgets.QPushButton(self.centralwidget)
        self.connect.setGeometry(QtCore.QRect(260, 130, 131, 51))
        self.connect.setObjectName("connect")
        self.connect.clicked.connect(self.start_client)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 658, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.set_led0.setEnabled(False)
        self.set_led1.setEnabled(False)
        self.set_led2.setEnabled(False)
        self.set_led3.setEnabled(False)

        self.dtc3.setEnabled(False)
        self.dtc2.setEnabled(False)
        self.dtc1.setEnabled(False)
        self.dtc4.setEnabled(False)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.logo.setPixmap(self.logo_img)
        self.connected_msg.setText(_translate("MainWindow", ""))
        self.not_diag_mode.setText(_translate("MainWindow", "NOT IN DIAG MODE"))
        self.diagMode.setText(_translate("MainWindow", "Enter Diag Mode"))
        self.diagMode_off.setText(_translate("MainWindow", "Stop Diag Mode"))
        self.set_led0.setText(_translate("MainWindow", "Set LED0"))
        self.set_led1.setText(_translate("MainWindow", "Set LED1"))
        self.set_led2.setText(_translate("MainWindow", "Set LED2"))
        self.set_led3.setText(_translate("MainWindow", "Set LED3"))

        self.set_led_title.setText(_translate("MainWindow", "SET LED STATES"))
        self.read_dtc_title.setText(_translate("MainWindow", "READ DTC STATES"))
        self.dtc3.setText(_translate("MainWindow", "Read DTC3"))
        self.dtc2.setText(_translate("MainWindow", "Read DTC2"))
        self.dtc1.setText(_translate("MainWindow", "Read DTC1"))
        self.dtc4.setText(_translate("MainWindow", "Read DTC4"))
        self.led0_state.setText(_translate("MainWindow", ""))
        self.led1_state.setText(_translate("MainWindow", ""))
        self.led2_state.setText(_translate("MainWindow", ""))
        self.led3_state.setText(_translate("MainWindow", ""))
        self.connect.setText(_translate("MainWindow", "CONNECT"))

############################### EXERCISE 0 ###############################
    diag_mode = False

    def refresh_diag(self):
        self.set_led0.setEnabled(self.diag_mode)
        self.set_led1.setEnabled(self.diag_mode)
        self.set_led2.setEnabled(self.diag_mode)
        self.set_led3.setEnabled(self.diag_mode)

        self.dtc3.setEnabled(self.diag_mode)
        self.dtc2.setEnabled(self.diag_mode)
        self.dtc1.setEnabled(self.diag_mode)
        self.dtc4.setEnabled(self.diag_mode)

        self.diagMode.setEnabled(not self.diag_mode)
        self.diagMode_off.setEnabled(self.diag_mode)

    def start_client(self):
        self.diagMode.setEnabled(True)
        self.diagMode_off.setEnabled(False)

        self.dtc1.setEnabled(True)
        self.dtc2.setEnabled(True)
        self.dtc3.setEnabled(True)
        self.dtc4.setEnabled(True)


        self.set_led0.setText('Set LED0')
        self.set_led1.setText('Set LED1')
        self.set_led2.setText('Set LED1')
        self.set_led3.setText('Set LED3')

    
        self.dtc1_state.setText('Unknown')
        self.dtc1_state.setStyleSheet('font:bold; color: blue;')
        self.dtc2_state.setText('Unknown')
        self.dtc2_state.setStyleSheet('font:bold; color: blue;')
        self.dtc3_state.setText('Unknown')
        self.dtc3_state.setStyleSheet('font:bold; color: blue;')
        self.dtc4_state.setText('Unknown')
        self.dtc4_state.setStyleSheet('font:bold; color: blue;')
        
        self.set_led0.setText('Set LED0')
        self.set_led1.setText('Set LED1')
        self.set_led2.setText('Set LED2')
        self.set_led3.setText('Set LED3')

        self.led0_state.setVisible(False)
        self.led1_state.setVisible(False)
        self.led2_state.setVisible(False)
        self.led3_state.setVisible(False)

        print('Starting client')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        self.server = s

        self.refresh_diag()

        self.recv_messages()


############################### EXERCISE 1 ###############################
    def recv_handler(self,stop_event):
        while True:
            msg = pk.loads(self.server.recv(1024))
            print(f'Received {msg}')

            if msg.startswith('0x6201'):
                color = str(msg)[6:]

                if color == '00000':
                    self.set_dtc1_state(0)
                elif color == '25500':
                    self.set_dtc1_state(1)
                elif color == '02550':
                    self.set_dtc1_state(2)
            elif msg.startswith('0x6202'):
                color = str(msg)[6:]

                if color == '00000':
                    self.set_dtc2_state(0)
                elif color == '25500':
                    self.set_dtc2_state(1)
                elif color == '02550':
                    self.set_dtc2_state(2)
            elif msg.startswith('0x6203'):
                color = str(msg)[6:]

                if color == '00000':
                    self.set_dtc3_state(0)
                elif color == '25500':
                    self.set_dtc3_state(1)
                elif color == '02550':
                    self.set_dtc3_state(2)

            elif msg.startswith('0x6204'):
                color = str(msg)[6:]

                if color == '00000':
                    self.set_dtc4_state(0)
                elif color == '25500':
                    self.set_dtc4_state(1)
                elif color == '02550':
                    self.set_dtc4_state(2)
            elif msg.startswith('0x2E'):
                led = msg[5:6]
                label = msg[6:]

                if led == '1':
                    self.set_led0_label(int(label))

                if led == '2':
                    self.set_led1_label(int(label))

                if led == '3':
                    self.set_led2_label(int(label))

                if led == '4':
                    self.set_led3_label(int(label))


    def send_to_server(self, msg):
        print(f'Sending {msg}')
        self.server.sendall(pk.dumps(msg))

    def recv_messages(self):
        self.stop_event = threading.Event()
        self.c_thread=threading.Thread(target=self.recv_handler, args=(self.stop_event,))
        self.c_thread.start()

    def diag(self):
        self.diag_mode = True
        self.refresh_diag()

    def stop_diag(self):
        self.diag_mode = False
        self.refresh_diag()


############################### EXERCISE 3 ###############################        
    # READ DTC's
    def get_dtc_state(self,dtc_string):
        msg = f'0x22{dtc_string}'
        self.send_to_server(msg)


    # SET DTC1 State
    def set_dtc1_state(self, data_recv):
        if data_recv == 0:
            self.dtc1_state.setText('Unknown')
            self.dtc1_state.setStyleSheet('font:bold; color: blue')

        elif data_recv == 1:
            self.dtc1_state.setText('Inactive')
            self.dtc1_state.setStyleSheet('font:bold; color: red')

        elif data_recv == 2:
            self.dtc1_state.setText('Active')
            self.dtc1_state.setStyleSheet('font:bold; color: green')

    # SET DTC2 State
    def set_dtc2_state(self,data_recv):
        if data_recv == 0:
            self.dtc2_state.setText('Unknown')
            self.dtc2_state.setStyleSheet('font:bold; color: blue')

        elif data_recv == 1:
            self.dtc2_state.setText('Inactive')
            self.dtc2_state.setStyleSheet('font:bold; color: red')

        elif data_recv == 2:
            self.dtc2_state.setText('Active')
            self.dtc2_state.setStyleSheet('font:bold; color: green')

    # SET DTC3 State
    def set_dtc3_state(self,data_recv):
        if data_recv == 0:
            self.dtc3_state.setText('Unknown')
            self.dtc3_state.setStyleSheet('font:bold; color: blue')

        elif data_recv == 1:
            self.dtc3_state.setText('Inactive')
            self.dtc3_state.setStyleSheet('font:bold; color: red')

        elif data_recv == 2:
            self.dtc3_state.setText('Active')
            self.dtc3_state.setStyleSheet('font:bold; color: green')

    # SET DTC4 State
    def set_dtc4_state(self,data_recv):
        if data_recv == 0:
            self.dtc4_state.setText('Unknown')
            self.dtc4_state.setStyleSheet('font:bold; color: blue')

        elif data_recv == 1:
            self.dtc4_state.setText('Inactive')
            self.dtc4_state.setStyleSheet('font:bold; color: red')

        elif data_recv == 2:
            self.dtc4_state.setText('Active')
            self.dtc4_state.setStyleSheet('font:bold; color: green')

############################### EXERCISE 4 ###############################

    # SET LED0
    def set_led0_label(self, data_recv):
        self.led0_state.setVisible(True)

        if data_recv == 0:
            self.led0_state.setVisible(False)
        elif data_recv == 1:
            self.led0_state.setStyleSheet(f'border-radius:12; background-color: red')
        elif data_recv == 2:
            self.led0_state.setStyleSheet(f'border-radius:12; background-color: green')

    led0_flag = 0
    def set_led0_flags(self):
        self.led0_flag += 1
        self.send_to_server(f'0x2E01{self.led0_flag % 3}')

    # SET LED1
    def set_led1_label(self,data_recv):
        self.led1_state.setVisible(True)

        if data_recv == 0:
            self.led1_state.setVisible(False)
        elif data_recv == 1:
            self.led1_state.setStyleSheet(f'border-radius:12; background-color: red')
        elif data_recv == 2:
            self.led1_state.setStyleSheet(f'border-radius:12; background-color: green')

    led1_flag = 0
    def set_led1_flags(self):
        self.led1_flag += 1
        self.send_to_server(f'0x2E02{self.led1_flag % 3}')


    # SET LED2
    def set_led2_label(self,data_recv):
        self.led2_state.setVisible(True)

        if data_recv == 0:
            self.led2_state.setVisible(False)
        elif data_recv == 1:
            self.led2_state.setStyleSheet(f'border-radius:12; background-color: red')
        elif data_recv == 2:
            self.led2_state.setStyleSheet(f'border-radius:12; background-color: green')


    led2_flag = 0
    def set_led2_flags(self):
        self.led2_flag += 1
        self.send_to_server(f'0x2E03{self.led2_flag % 3}')


    # SET LED3
    def set_led3_label(self,data_recv):
        self.led3_state.setVisible(True)

        if data_recv == 0:
            self.led3_state.setVisible(False)
        elif data_recv == 1:
            self.led3_state.setStyleSheet(f'border-radius:12; background-color: red')
        elif data_recv == 2:
            self.led3_state.setStyleSheet(f'border-radius:12; background-color: green')

    led3_flag = 0
    def set_led3_flags(self):
        self.led3_flag += 1
        self.send_to_server(f'0x2E04{self.led3_flag % 3}')

##########################################################################

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

