#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from tkinter import ttk
import socket
import json
import argparse
import threading
import os
import sys
from pathlib import Path

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

root = tk.Tk()
root.title("Carsharing Server")

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
    for i in "Start", "Send", "Clear", "Exit":
        b = tk.Button(master=frame, text=i)
        b.pack(side="left")
        yield b


b1, b2, b3, b4, = buttons()


def print_system_notification(message):
    data = str(message)
    now = str(datetime.now())[:-7]
    text.insert("insert", "({}) : {}\n".format(now, data), 'notification')


class Server:
    clients = list()

    auth_clients = list()
    restricted_customers = list()

    host = '127.0.0.1'
    port = 65432

    # Dictionary containing registered clients (phone or car).
    # It contains pairs of (unique identifier - phone IMEI or car number, client uuid).
    registered_clients = {}

    # Dictionary containing rentals in progress.
    # It contains pairs of (car number, phone app client uuid).
    rentals_in_progress = {}

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.rental = []

    @staticmethod
    def parse_json(json_to_be_parsed, destination):
        print_system_notification('Parsing Json File...')
        json_array_of_clients = json.loads(json_to_be_parsed)
        for key in json_array_of_clients:
            print_system_notification('key=' + key)
            print_system_notification("[" + key + "] = " + str(json_array_of_clients[key]))
            for auth_client in json_array_of_clients[key]:
                destination.append(auth_client)

    def set_address(self, host, port):
        self.host = host
        self.port = port

    def start(self):
        self.s.bind((self.host, self.port))
        self.s.listen(10)
        now = str(datetime.now())[:-7]
        text.insert("insert", "({}) : Started.\n".format(now))
        self.condition()

    def accept(self):
        c, addr = self.s.accept()
        data = c.recv(1024)
        tup = (c, data)
        self.clients.append(tup)
        status.configure(bg='green', text='Connected')
        # text.insert("insert", "({}) : {} connected.\n".format(str(datetime.now())[:-7], str(data)[1:]))

    # Parses messages received from clients.
    # @Param command Message received from client (phone app / car).
    def handle_message(self, command):
        print_system_notification("received command from client =" + command)

        toks = command.split()
        command_id = toks[1]

        if command_id == 'register-client':
            print_system_notification('register-client')

            # Eg (received): <phone_uuid> register-client
            # Eg (received): <client_uuid> register-client
            client_uuid = toks[0]
            car_number_or_phone_id = toks[2]
            if not self.registered_clients.__contains__(car_number_or_phone_id):
                # print_system_notification("acknowledge-register \"" + car_or_phone_id + "\"")
                self.send_bytes_to_client(client_uuid, "acknowledge-register \"" + car_number_or_phone_id + "\"")
                self.registered_clients[car_number_or_phone_id] = client_uuid
            else:
                self.send_bytes_to_client(client_uuid, "acknowledge-register error -> \"" + car_number_or_phone_id + "\" is already registered")

        if command_id == 'server-end-rental':
            print_system_notification('server-end-rental')

            # Eg (received): <phone_app_uuid> server-end-rental IS21KSM
            phone_app_uuid = toks[0]
            car_number = toks[2]
            self.rentals_in_progress[car_number] = phone_app_uuid
            car_uuid = self.registered_clients[car_number]
            self.send_bytes_to_client(car_uuid, "car-end-rental")

        if command_id == 'car-info':
            print_system_notification('car-info')

            # Eg (received): <car_uuid> car-info latitude 47.1585
            print_system_notification("car-info " + toks[2] + " " + toks[3])

        if command_id == 'response-end-rental':
            print_system_notification('response-end-rental')

            # Eg (received): <car_uuid> response-end-rental success IS21KSM
            rental_status = toks[2]
            car_number = toks[3]
            phone_uuid = self.rentals_in_progress[car_number]
            if rental_status == 'success':
                self.rentals_in_progress.pop(car_number)
            self.send_bytes_to_client(phone_uuid, "response-end-rental " + car_number + " " + rental_status)

        print_system_notification('handle_message end')

    def receive(self):
        for c in self.clients:

            def f():
                data = str(c[0].recv(1024))[2:-1]
                now = str(datetime.now())[:-7]
                if len(data) == 0:
                    pass
                else:
                    text.insert("insert", "({}) : {}\n".format(now, data), 'remote')
                    self.handle_message(data)

            t1_2_1 = threading.Thread(target=f)
            t1_2_1.start()

    def condition(self):
        while True:
            t1_1 = threading.Thread(target=self.accept)
            t1_1.daemon = True
            t1_1.start()
            t1_1.join(1)
            t1_2 = threading.Thread(target=self.receive)
            t1_2.daemon = True
            t1_2.start()
            t1_2.join(1)

    # Retrieves input from text box and sends request to client.
    # Format: car_or_phone_id#<request details>
    # Eg: IS21KSM#request-info latitude
    #       where IS21KSM is car_number
    def send(self):
        response = str(entry.get())
        toks = response.split("#")
        car_or_phone_id = toks[0]
        client_id = self.registered_clients[car_or_phone_id]
        self.send_bytes_to_client(client_id, toks[1])

    def send_bytes_to_client(self, client_id, response):
        now = str(datetime.now())[:-7]
        entry.delete("0", "end")
        try:
            msg_sent = False
            for c in self.clients:
                if c[1] == client_id.encode('utf-8'):
                    c[0].sendall(bytes(response.encode("utf-8")))
                    text.insert("insert", "({}) : {}\n".format(now, response))
                    msg_sent = True
            if not msg_sent:
                print_system_notification("msg was NOT sent to client \"" + client_id + "\"")
        except BrokenPipeError:
            text.insert("insert", "({}) : Client has been disconnected.\n".format(now))
            status.configure(bg='red', text='Disconnected')


s1 = Server()


def start():
    t1 = threading.Thread(target=s1.start)
    t1.start()


def send():
    t2 = threading.Thread(target=s1.send)
    t2.start()


def clear():
    text.delete("1.0", "end")


def destroy():
    root.destroy()
    exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Carsharing Server')
    parser.add_argument('host', help='Interface the server listens at')
    parser.add_argument('-port', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    s1.set_address(args.host, args.port)
    b1.configure(command=start)
    b2.configure(command=send)
    b3.configure(command=clear)
    b4.configure(command=destroy)
    t0 = threading.Thread(target=root.mainloop)
    t0.run()
