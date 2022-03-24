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
root.title("Diagnosis Server")


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
    clients = []

    host = '127.0.0.1'
    port = 65432

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

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
        self.clients.append(c)
        data = c.recv(1024)
        status.configure(bg='green', text='Connected')
        # text.insert("insert", "({}) : {} connected.\n".format(str(datetime.now())[:-7], str(data)[1:]))

    def handle_message(self, command):
        if command.startswith('dtc-P0138'):
            print_system_notification('start-rental')
            self.send_bytes_to_client("display-popup#Oxygen Sensor malfunction. Your can still drive your car for a short time but your vehicle fuel economy will suffer. Serice your car as soon as possible.")

        if command.startswith('dtc-P0300'):
            self.send_bytes_to_client("display-popup#Random, Multiple Misfire Detected. This is a critical issue. You need to stop driving immediately and tow your car to the nearest authorized service.")
            self.send_bytes_to_client("service-soon")

        if command.startswith('dtc-P0700'):
            self.send_bytes_to_client("display-popup#Transmission Control System Malfunction. Please stop driving the vehicle immediately.")
            self.send_bytes_to_client("service-soon")

    def receive(self):
        for i in self.clients:

            def f():
                data = str(i.recv(1024))[2:-1]
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

    def send(self):
        response = str(entry.get())
        self.send_bytes_to_client(response)

    def send_bytes_to_client(self, response):
        now = str(datetime.now())[:-7]
        entry.delete("0", "end")
        try:
            for i in self.clients:
                i.sendall(bytes(response.encode("utf-8")))
            text.insert("insert", "({}) : {}\n".format(now, response))
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
