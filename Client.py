import socket
import threading
import tkinter
import tkinter.scrolledtext
#import os
#os.system("pip install keyboard")
import keyboard
from tkinter import simpledialog
import sys

class Client():
    def __init__(self,host,password,port=5555,name = "NO_NAME",running = False):
        self.password = str(password)
        self.running = running
        self.host = host
        self.port = port
        self.name = name
        if self.name == "NO_NAME":
            msg = tkinter.Tk()
            msg.withdraw()
            self.name = simpledialog.askstring("Name","Please enter name",parent = msg)
        if self.name is None:
            self.socket.close()
            exit(0)
        if self.running:
            self.begin()
        self.ui_done = False


    def begin(self):
        self.running = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.main_thread = threading.Thread(target=self.main_loop)
        self.recv_thread = threading.Thread(target=self.recv_msg)
        #self.is_pressing = threading.Thread(target=self.pressing)
        #self.is_pressing.start()
        self.main_thread.start()
        self.recv_thread.start()

    def main_loop(self):
        self.window = tkinter.Tk()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.configure(bg ="lightgray")

        self.chat_label = tkinter.Label(self.window, text = "Chat:", bg= "lightgray")
        self.chat_label.config(font= ('Arial',16))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area= tkinter.scrolledtext.ScrolledText(self.window)
        self.text_area.config(font=('Arial',12))
        self.text_area.pack(pady=5,padx=20)
        self.text_area.config(state = 'disabled')

        self.messege_label = tkinter.Label(self.window, text="Messege:", bg="lightgray")
        self.messege_label.config(font=('Arial', 12))
        self.messege_label.pack(padx=20, pady=5)

        self.input_area = tkinter.Text(self.window,height = 5)
        self.input_area.pack(padx=20,pady=5)

        self.send_button = tkinter.Button(self.window,text = "SEND", command= self.send)
        self.send_button.config(font = ('Arial',12))
        self.send_button.pack(padx=20,pady=5)
        self.ui_done = True
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()

    def on_closing(self):
        print("worked")
        self.running = False
        self.window.destroy()
        self.socket.close()
        sys.exit()
    #def pressing(self):
    #    while True:
    #        if keyboard.is_pressed("ctrl"):
    #            self.send()

    def send(self):
        msg = self.input_area.get('1.0','end')
        new_msg =""
        for i in msg:
            if i.isalpha() or i.isdigit() or i == " " or i == ":":
                new_msg += i
        msg = new_msg
        self.socket.send(msg.encode())
        self.input_area.delete('1.0','end')
    def recv_msg(self):
        try:
            self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        except:
            while self.running:
                print('rcv data')

                try:
                    self.data= self.socket.recv(1024).decode()
                    print(self.data)
                    if self.data == "NAME":
                        self.socket.send(self.name.encode())
                    elif self.data == "PASSWORD":
                        self.socket.send(self.password.encode())
                    elif self.data == "is_done":
                        while True:
                            if self.ui_done:
                                self.socket.send("YES".encode())
                                print("reciving history")
                                break
                        while True:
                            History = self.socket.recv(1024).decode()
                            print(History," is history")
                            if History == "DONE":
                                break
                            self.text_area.config(state='normal')
                            self.text_area.insert('end', f'{History}\n')
                            self.text_area.yview('end')
                            self.text_area.config(state='disabled')
                    else:
                        #for i in self.data:
                        #    if not i.isalpha() or not i.isdigit() or i != " " or i != ":":
                        #        self.on_closing()
                        #        exit()
                        while True:
                            if self.ui_done:
                                self.text_area.config(state = 'normal')
                                self.text_area.insert('end',f'{self.data}\n')
                                self.text_area.yview('end')
                                self.text_area.config(state = 'disabled')
                                break

                except ConnectionError:
                    break
                except:
                    print("ERror")
                    self.socket.close()
                    break
