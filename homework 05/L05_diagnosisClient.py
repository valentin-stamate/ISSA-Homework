#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import socket
import json
import argparse
import threading
from pathlib import Path

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
from tkinter import *


root = tk.Tk()
root.title("Diagnossis Client")

text = tk.Text(master=root)
text.pack(expand=True, fill="both")
text.tag_config('remote', foreground="blue")
text.tag_config('notification', foreground="yellow", background='black')

entry = tk.Entry(master=root)
entry.pack(expand=True, fill="x")

frame = tk.Frame(master=root)
frame.pack()

frame2 = tk.Frame(master=root)
frame2.pack(side="bottom")

frame3 = tk.Frame(master=root)
frame3.pack(side="bottom")

status = tk.Button(master=frame, text='Disconnected', bg='red')
status.pack(side="left")

displayInfo = tk.Button(master=frame3, text='Display Car Info')
displayInfo.pack(side="left")

startDiagnosis = tk.Button(master=frame3, text='Start Remote Diagnosis')
startDiagnosis.pack(side="left")


# Creating a photoimage object to use image
checkEngineImg = PhotoImage(file=r"./images/checkEngine.png")
checkOilImg = PhotoImage(file=r"./images/checkOil.png")
checkTiresImg = PhotoImage(file=r"./images/checkTires.png")
engineTemperatureWarningImg = PhotoImage(file=r"./images/engineTemperatureWarning.png")
checkBatteryImg = PhotoImage(file=r"./images/checkBattery.png")
serviceSoonImg = PhotoImage(file=r"./images/serviceSoon.png")


def buttons():
    for i in "Connect", "Send", "Clear", "Exit":
        b = tk.Button(master=frame, text=i)
        b.pack(side="left")
        yield b


b1, b2, b3, b4 = buttons()

def warningLights():
    for i in "CheckEngine", "OilPressure", "TirePressure", "EngineTmperature", "Battery", "ServiceSoon":
        b = tk.Button(master=frame2, text="", height=4, width=8, bg='black',state="disabled")
        b.pack(side="left")
        yield b


CheckEngineLight, OilPressureLight, TirePressureLight, EngineTemperatureLight, BatteryLight, ServiceSoonLight = warningLights()


def print_system_notification(message):
    data = str(message)
    now = str(datetime.now())[:-7]
    text.insert("insert", "({}) : {}\n".format(now, data), 'notification')


def turn_check_engine_light(state):
    if state:
        CheckEngineLight.config(image=checkEngineImg,height=66, width=64)
    else:
        CheckEngineLight.config(image="",height=4, width=8)


def turn_oil_pressure_light(state):
    if state:
        OilPressureLight.config(image=checkOilImg,height=66, width=64)
    else:
        OilPressureLight.config(image="",height=4, width=8)


def turn_tire_pressure_light(state):
    if state:
        TirePressureLight.config(image=checkTiresImg,height=66, width=64)
    else:
        TirePressureLight.config(image="",height=4, width=8)


def turn_engine_temperature_light(state):
    if state:
        EngineTemperatureLight.config(image=engineTemperatureWarningImg,height=66, width=64)
    else:
        EngineTemperatureLight.config(image="",height=4, width=8)


def turn_battery_light(state):
    if state:
        BatteryLight.config(image=checkBatteryImg,height=66, width=64)
    else:
        BatteryLight.config(image="",height=4, width=8)


def turn_service_soon_light(state):
    if state:
        ServiceSoonLight.config(image=serviceSoonImg,height=66, width=64)
    else:
        ServiceSoonLight.config(image="",height=4, width=8)


class Client:
    host = '127.0.0.1'
    port = 65432

    car_data=dict()
    dtc_list=list()

    def __init__(self):
        self.parse_configuration_file()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print('Ok')
        data = self.car_data

        if data['oil-pressure'] < 30 or data['oil-pressure'] > 60:
            turn_oil_pressure_light(True)
        if data['FLtire-pressure'] < 20 or data['FLtire-pressure'] > 24 or \
                data['FRtire-pressure'] < 20 or data['FRtire-pressure'] > 24:
            turn_tire_pressure_light(True)
        if data['RLtire-pressure'] < 18 or data['RLtire-pressure'] > 22 or \
                data['RRtire-pressure'] < 18 or data['RRtire-pressure'] > 22:
            turn_tire_pressure_light(True)
        if data['engine-temperature'] > 90:
            turn_engine_temperature_light(True)
        if data['battery-level'] < 15:
            turn_battery_light(True)

    def parse_configuration_file(self):
        script_location = Path(__file__).absolute().parent
        file_location = script_location / 'L05_carData.json'
        with open(file_location, 'r') as content_file:
            content = content_file.read()
            print('content = ', content)
            self.parse_json(content)

    def parse_json(self, json_to_be_parsed):
        print_system_notification('Parsing Json File...')
        json_array_of_clients = json.loads(json_to_be_parsed)
        for key in json_array_of_clients:
            print_system_notification('key=' + key)
            print_system_notification("[" + key + "] = " + str(json_array_of_clients[key]))
            for val in json_array_of_clients[key]:
                if key == "carinfo":
                    self.car_data[val] = json_array_of_clients[key][val]
                if key == "dtc":
                    self.dtc_list.append(val)

    def print_popup(self, message):
        message = message.replace('display-popup', '')
        popup = tk.Toplevel()
        popup.geometry("%dx%d%+d%+d" % (850, 100, 250, 125))
        popup.title = "Warning"
        warning_label = tk.Label(master=popup, text=str(message))
        warning_label.pack(side="top")
        exit_button = tk.Button(master=popup, text="Exit")
        exit_button.pack(side="bottom")

        def close_info():
            popup.destroy()

        exit_button.configure(command=close_info)

    def set_address(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        now = str(datetime.now())[:-7]
        try:
            self.s.connect((self.host, self.port))
            text.insert("insert", "({}) : Connected.\n".format(now))
            msg = "connection ready"
            self.s.sendall(bytes(msg.encode("utf-8")))
            self.receive()
        except ConnectionRefusedError:
            text.insert("insert", "({}) : The server is not online.\n".format(now))

    def handle_message(self, command):
        if command.startswith('display-popup'):
            print_system_notification("display-popup")
            self.print_popup(command)

        if 'service-soon' in command:
            print_system_notification("service-soon")
            turn_service_soon_light(True)

    def receive(self):
        status.configure(bg='green', text='Connected')
        while True:
            data = str(self.s.recv(1024))[2:-1]
            now = str(datetime.now())[:-7]
            if len(data) == 0:
                pass
            else:
                text.insert("insert", "({}) : {}\n".format(now, data), 'remote')
                self.handle_message(data)

    def do_nothing(self):
        pass

    def send(self):
        respond = str(entry.get())
        self.send_bytes_to_server(respond)

    def send_bytes_to_server(self, respond):
        now = str(datetime.now())[:-7]
        entry.delete("0", "end")
        try:
            self.s.sendall(bytes(respond.encode("utf-8")))
            text.insert("insert", "({}) : sent msg ({})\n".format(now, respond))
        except BrokenPipeError:
            text.insert("insert", "\nDate: {}\Server has been disconnected.\n".format(now))
            self.s.close()


c1 = Client()


def connect():
    t1 = threading.Thread(target=c1.connect)
    t1.start()



def send():
    t2 = threading.Thread(target=c1.send)
    t2.start()


def clear():
    text.delete("1.0", "end")


def destroy():
    root.destroy()
    status.configure(bg='red', text='Disconnected')

def displayCarInfo():
    popup = tk.Toplevel()
    popup.geometry("%dx%d%+d%+d" % (300, 200, 250, 125))
    popup.title = "Car Info"

    oil_level = tk.Label(master=popup,text="Oil Level:")
    oil_level.grid(row=0, column=0)
    oil_level_value = tk.Label(master=popup)
    oil_level_value.grid(row=0, column=1)
    oil_level_value.config(text=str(c1.car_data["oil-pressure"]))

    oil_level = tk.Label(master=popup,text="Rear Left tire-pressure:")
    oil_level.grid(row=1, column=0)
    oil_level_value = tk.Label(master=popup)
    oil_level_value.grid(row=1, column=1)
    oil_level_value.config(text=str(c1.car_data["RLtire-pressure"]))

    oil_level = tk.Label(master=popup,text="Rear Right tire-pressure:")
    oil_level.grid(row=2, column=0)
    oil_level_value = tk.Label(master=popup)
    oil_level_value.grid(row=2, column=1)
    oil_level_value.config(text=str(c1.car_data["RRtire-pressure"]))

    oil_level = tk.Label(master=popup,text="Front Left tire-pressure:")
    oil_level.grid(row=3, column=0)
    oil_level_value = tk.Label(master=popup)
    oil_level_value.grid(row=3, column=1)
    oil_level_value.config(text=str(c1.car_data["FLtire-pressure"]))

    oil_level = tk.Label(master=popup,text="Front Right tire-pressure")
    oil_level.grid(row=3, column=0)
    oil_level_value = tk.Label(master=popup)
    oil_level_value.grid(row=3, column=1)
    oil_level_value.config(text=str(c1.car_data["FRtire-pressure"]))

    oil_level = tk.Label(master=popup,text="Engine Temperature:")
    oil_level.grid(row=4, column=0)
    oil_level_value = tk.Label(master=popup)
    oil_level_value.grid(row=4, column=1)
    oil_level_value.config(text=str(c1.car_data["engine-temperature"]))

    oil_level = tk.Label(master=popup,text="Battery Level:")
    oil_level.grid(row=5, column=0)
    oil_level_value = tk.Label(master=popup)
    oil_level_value.grid(row=5, column=1)
    oil_level_value.config(text=str(c1.car_data["battery-level"]))

    exit_button = tk.Button(master=popup, text="Exit")
    exit_button.grid(row=6, column=0)

    def close_info():
        popup.destroy()

    exit_button.configure(command=close_info)

def startRemoteDiagnosis():
    for element in c1.dtc_list:
        c1.send_bytes_to_server("dtc-"+str(element))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Carsharing Client')
    parser.add_argument('host', help='Interface the server listens at')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    c1.set_address(args.host, args.p)
    b1.configure(command=connect)
    b2.configure(command=send)
    b3.configure(command=clear)
    b4.configure(command=destroy)
    displayInfo.configure(command=displayCarInfo)
    startDiagnosis.configure(command=startRemoteDiagnosis)
    t0 = threading.Thread(target=root.mainloop)
    t0.run()