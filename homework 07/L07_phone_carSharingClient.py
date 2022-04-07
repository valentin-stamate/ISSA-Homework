#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import socket
import argparse
import threading
import uuid

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

root = tk.Tk()
root.title("Phone App [Client]")

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
    for i in "Connect", "Register", "Send", "Clear", "Exit", "Register user":
        b = tk.Button(master=frame, text=i)
        b.pack(side="left")
        yield b


b1, b2, b3, b4, b5, b6 = buttons()

def print_system_notification(message):
    data = str(message)
    now = str(datetime.now())[:-7]
    text.insert("insert", "({}) : {}\n".format(now, data), 'notification')


class Client:
    host = '127.0.0.1'
    port = 65432
    info = dict()

    # Information required for registration of a new user (exercise 2).
    userId = ""
    userAge = ""
    userDriverLicense = ""
    userEmail = ""
    userPhone = ""

    # Flag stating whether all user details have been introduced or not.
    isFilled = False

    # Unique identifier for each client.
    uuid = uuid.uuid1()

    # Dictionary containing car information.
    # Will be used to send info to server.
    car_info = {}

    # Unique identifier for phone (EMEI).
    phone_id = "6533"

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.userId = ""
        self.userAge = ""
        self.userDriverLicense = ""
        self.userEmail = ""
        self.userPhone = ""

    def register_client(self):
        print_system_notification("[dbg] register_client")

        # Exercise 2
        # Add the needed checks to verify that all the user info have been introduced.
        # If they were, send a message to server "register-client <phone_id>".
        if self.isFilled:
            self.send_bytes_to_server(f'register-user {self.phone_id}')


    def register_user(self):
        popup = tk.Toplevel()
        popup.title = "Form"
        user_id_entry = tk.Entry(master=popup)
        user_id_entry.grid(row=0, column=0)
        user_id_label = tk.Label(popup, text="user id:")
        user_id_label.grid(row=0, column=1)

        user_age_entry = tk.Entry(master=popup)
        user_age_entry.grid(row=1, column=0)
        user_age_label = tk.Label(popup, text="user age:")
        user_age_label.grid(row=1, column=1)

        user_drivers_license_entry = tk.Entry(master=popup)
        user_drivers_license_entry.grid(row=2, column=0)
        user_drivers_license_label = tk.Label(popup, text="user drivers license:")
        user_drivers_license_label.grid(row=2, column=1)

        user_email_entry = tk.Entry(master=popup)
        user_email_entry.grid(row=3, column=0)
        user_email_label = tk.Label(popup, text="user email:")
        user_email_label.grid(row=3, column=1)

        user_phone_entry = tk.Entry(master=popup)
        user_phone_entry.grid(row=4, column=0)
        user_phone_label = tk.Label(popup, text="user phone:")
        user_phone_label.grid(row=4, column=1)

        var1 = tk.IntVar()
        check = tk.Checkbutton(popup, text="Agree to terms", variable=var1).grid(row=5, column =0)

        new_button = tk.Button(master=popup, text="Enter")
        new_button.grid(row=6, column=0)

        def register_command():
            now = str(datetime.now())[:-7]
            print_system_notification(var1)
            if user_id_entry.get() == "" or user_age_entry.get() == "" or user_drivers_license_entry.get() == "" or var1.get() == 0:
                print_system_notification('Data is incomplete. Please complete all fields')
            else:
                self.userId = user_id_entry.get()
                self.userAge = user_age_entry.get()
                self.userDriverLicense = user_drivers_license_entry.get()
                self.userEmail = user_email_entry.get()
                self.userPhone = user_phone_entry.get()
                print_system_notification('Succesfully registered client data: user id:' + self.userId + ' user age:' + self.userAge + ' user drivers license:' + self.userDriverLicense
                                          + 'user email:' + self.userEmail + ' user phone:' + self.userPhone)
                self.isFilled = True
                popup.destroy()

        new_button.configure(command=register_command)

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

    # Parses messages received from server.
    # @Param command Message received from server.
    def handle_message(self, command):
        print_system_notification("received command from server =" + command)

        toks = command.split()
        command_id = toks[0]
        print_system_notification('command_id=' + command_id)

        if command_id == 'acknowledge-register':
            # Eg (received): acknowledge-register
            print_system_notification("registration was successful")

        if command_id == 'response-end-rental':
            # Eg (received): response-end-rental IS21KSM success
            car_number = toks[1]
            rental_status = toks[2]
            print_system_notification("end-rental " + car_number + " " + rental_status)

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

    # Retrieves the command written in the text and sends it to Server.
    def send(self):
        self.send_bytes_to_server(entry.get())

    # Sends response to server.
    # It adds the client uuid based on which the server replies to client.
    # @Param response Message to send to server.
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

def register_user():
    c1.register_user()


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
    b6.configure(command=register_user)

    t0 = threading.Thread(target=root.mainloop)
    t0.run()