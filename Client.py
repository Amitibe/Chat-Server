import socket
import threading
import tkinter
import tkinter.scrolledtext
import os
from tkinter import simpledialog
import EncodingProtocol
import sys

class Client():
    def __init__(self,host,password,port=5555,name = "NO_NAME",running = False):
        self.stop = False
        self.password = str(password)
        self.running = running
        self.host = host
        self.port = port
        self.name = name
        self.key = ""
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
        """: This method is responsible for setting up the client connection.
         It creates a socket and connects to the specified host and port"""
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
        """This method creates the tkinter window and sets up the user interface for the chat application"""
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
        """ This method is called when the tkinter window is closed.
         It sets the running status to False, stops the client, destroys the window, closes the socket, and exits the program."""
        print("worked")
        self.running = False
        self.stop = True
        self.window.destroy()
        self.socket.close()
        sys.exit()

    def send(self):
        """ This method is called when the send button is clicked. It retrieves the message entered in the input area, and sends it
         if the msg is play runner, plays runner"""
        should_play = False
        msg = self.input_area.get('1.0','end')
        if msg[0:-1] == "play runner":
            should_play = True
        msg = msg.lower()
        new_msg = ""
        for i in msg:
            if (i.isalpha() and i in "abcdefghijklmnopqrstuvwxyz") or i.isdigit() or i == " " or i == ":":
                new_msg += i
        if new_msg != "":
            encodedmsg = EncodingProtocol.encode(new_msg,self.key)
            try:
                self.socket.send(encodedmsg.encode())
            except:
                print("lost connection error")
                self.window.destroy()
                return
        if should_play:
            os.system('python Game.py')

        self.input_area.delete('1.0','end')
    def recv_msg(self):
        """. It receives data from the socket and processes it accordingly."""
        while self.running:
            print('rcv data')
            try:
                if self.stop or not self.running:
                    break
                self.data= self.socket.recv(1024).decode()

                print(self.data)
                if self.data == "NAME":
                    self.socket.send(self.name.encode())
                elif self.data == "PASSWORD":
                    self.socket.send(self.password.encode())
                elif self.data[0:3] == "KEY":
                    self.key = self.data[4:]
                    print(self.key)
                elif self.data == "is_done":
                    while True:
                        if self.ui_done:
                            self.socket.send("YES".encode())
                            print("reciving history")
                            break
                    while True:
                        History = self.socket.recv(1024).decode()
                        if History == "DONE":
                            break
                        if self.data[0:6] != "SERVER":
                            decodedHistory = ''
                            hList = History.split("___")
                            print(hList)
                            for i in hList:
                                print(EncodingProtocol.decode(i,self.key))
                                decodedHistory = decodedHistory + EncodingProtocol.decode(i,self.key) + "\n"
                        else:
                            decodedHistory= History
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', f'{decodedHistory}\n')
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
                else:
                    while True:
                        if self.ui_done:
                            if self.data[0:6] != "SERVER":
                                messageList = self.data.split(": ")
                                if len(messageList) == 2:
                                    messagePart = messageList[1]
                                    decoded_message = EncodingProtocol.decode(messagePart,self.key)
                                    decoded_data = ""+ messageList[0] + ": " + decoded_message
                                else:
                                    decoded_data = EncodingProtocol.decode(messageList[0],self.key)
                            else:
                                decoded_data = self.data
                            self.text_area.config(state = 'normal')
                            self.text_area.insert('end',f'{decoded_data}\n')
                            self.text_area.yview('end')
                            self.text_area.config(state = 'disabled')
                            break

            except ConnectionError:
                break
            #except:
            #    print("ERror")
            #    self.socket.close()
            #    break