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

root = tk.Tk()
root.title("Carsharing Client")

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
    for i in "Connect", "Send", "Clear", "Exit":
        b = tk.Button(master=frame, text=i)
        b.pack(side="left")
        yield b


b1, b2, b3, b4 = buttons()


def print_system_notification(message):
    data = str(message)
    now = str(datetime.now())[:-7]
    text.insert("insert", "({}) : {}\n".format(now, data), 'notification')


class Client:
    host = '127.0.0.1'
    port = 65432
    info = dict()

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
        if command == 'authorized':
            print_system_notification('authorized')

        if command == 'not-authorized':
            print_system_notification('not-authorized')

        if command.startswith('end-rental'):
            print_system_notification(command)

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
    t0 = threading.Thread(target=root.mainloop)
    t0.run()