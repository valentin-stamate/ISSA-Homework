#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import socket
import json
import argparse
import threading
from pathlib import Path
import uuid

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

root = tk.Tk()
root.title("Car [Client]")

text = tk.Text(master=root)
text.pack(expand=True, fill="both")
text.tag_config('remote', foreground="blue")
text.tag_config('notification', foreground="yellow", background='black')

entry = tk.Entry(master=root)
entry.pack(expand=True, fill="x")

frame = tk.Frame(master=root)
frame.pack()

status = tk.Button(master=frame, text='Disconnected', bg='red')
status.pack(side="left")

def buttons():
    for i in "Connect", "Register", "Send", "Clear", "Exit":
        b = tk.Button(master=frame, text=i)
        b.pack(side="left")
        yield b


b1, b2, b3, b4, b5 = buttons()

def print_system_notification(message):
    data = str(message)
    now = str(datetime.now())[:-7]
    text.insert("insert", "({}) : {}\n".format(now, data), 'notification')


class Client:
    host = '127.0.0.1'
    port = 65432
    info = dict()

    userId = ""
    userAge = ""
    userDriverLicense = ""
    userEmail = ""
    userPhone = ""
    isFilled = False # Flag for user details.

    # Unique car identifier.
    # For didactic purposes, car number is used.
    # In real applications, Vehicle Identification Number (VIN) will be used.
    car_number = "IS21KSM"

    # Unique identifier for each client.
    uuid = uuid.uuid1()

    # Dictionary containing car information.
    # Will be used to send info to server.
    car_info = {}

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.userId = ""
        self.userAge = ""
        self.userDriverLicense = ""
        self.userEmail = ""
        self.userPhone = ""

        self.parse_configuration_file("L07_car_info.json")

    def register_client(self):
        self.send_bytes_to_server("register-client " + self.car_number)

    def set_address(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        now = str(datetime.now())[:-7]
        try:
            self.s.connect((self.host, self.port))
            text.insert("insert", "({}) : Connected.\n".format(now))
            msg = str(self.uuid)
            self.s.sendall(bytes(msg.encode("utf-8")))
            self.receive()
        except ConnectionRefusedError:
            text.insert("insert", "({}) : The server is not online.\n".format(now))

    def handle_message(self, command):
        print_system_notification("received command from server =" + command)

        toks = command.split()
        command_id = toks[0]
        print_system_notification('command_id=' + command_id)

        if command_id == 'acknowledge-register':
            print_system_notification("registration was successful")

        if command_id == 'request-info':
            print_system_notification('request-info')

            # Exercise 1
            # Send the requested car info to server.
            # Example:
            # For request from server: "IS21KSM#request-info latitude"
            # response must be: "car-info latitude <latitude-value>".
            # # The needed information are available in self.car_info.
            info_type = toks[1]
            self.send_bytes_to_server(f"car info {info_type} {self.car_info[info_type]}")

        if command_id == 'car-end-rental':
            print_system_notification('car-end-rental')

            # Exercise 3
            # Eg (received): car-end-rental
            # Check whether the doors are closed and the lights are off.
            # Depending on this check, return "response-end-rental success <car_number>"
            # or "response-end-rental error <car_number>".
            # The needed information are available in self.car_info, self.car_number.
            if self.car_info['doors'] == 'closed' and self.car_info['lights'] == 'off':
                self.send_bytes_to_server(f'response-end-rental success {self.car_number}')
            else:
                self.send_bytes_to_server(f'response-end-rental error {self.car_number}')

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

    def parse_configuration_file(self, filename):
        script_location = Path(__file__).absolute().parent
        file_location = script_location / filename
        with open(file_location, 'r') as content_file:
            content = content_file.read()
            print('content = ', content)
            self.parse_json(content)

    # Parses jason file.
    # @param self: Self object.
    # @param json_to_be_parsed: Full path to the json file to be parsed.
    def parse_json(self, json_to_be_parsed):
        print_system_notification('[parse_json] starting to parse JSON file')
        json_array_of_clients = json.loads(json_to_be_parsed)
        for key in json_array_of_clients:
            print_system_notification('key=' + key)
            print_system_notification("[" + key + "] = " + str(json_array_of_clients[key]))
            self.car_info[key] = str(json_array_of_clients[key])
        print_system_notification('[parse_json] ended parsing JSON file')

    # Retrieves the command written in the text and sends it to Server.
    def send(self):
        self.send_bytes_to_server(entry.get())

    # Sends response to server.
    # It adds the client uuid based on which the server replies to client.
    # @Param response String to send to server.
    def send_bytes_to_server(self, response):
        full_response = "{} {}".format(str(self.uuid), response)

        now = str(datetime.now())[:-7]
        entry.delete("0", "end")
        try:
            self.s.sendall(bytes(full_response.encode("utf-8")))
            text.insert("insert", "({}) : sent msg ({})\n".format(now, full_response))
        except BrokenPipeError:
            text.insert("insert", "\nDate: {}\Server has been disconnected.\n".format(now))
            self.s.close()


c1 = Client()


def connect():
    t1 = threading.Thread(target=c1.connect)
    t1.start()


def register():
    c1.register_client()


def send():
    t2 = threading.Thread(target=c1.send)
    t2.start()


def clear():
    text.delete("1.0", "end")


def destroy():
    root.destroy()
    status.configure(bg='red', text='Disconnected')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Carsharing Client')
    parser.add_argument('host', help='Interface the server listens at')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    c1.set_address(args.host, args.p)
    b1.configure(command=connect)
    b2.configure(command=register)
    b3.configure(command=send)
    b4.configure(command=clear)
    b5.configure(command=destroy)

    t0 = threading.Thread(target=root.mainloop)
    t0.run()