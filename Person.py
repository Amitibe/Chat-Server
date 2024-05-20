import threading
import tkinter
import time
import socket
from Client import Client as client
class person:
    def __init__(self, name = 'amit', port = 5555):
        self.name = name
        self.port = port
        self.chats = []
        self.thread = threading.Thread(target=self.main_loop)
        self.thread.start()
        self.ip =0

    def on_closing(self):
        """This function is called when the tkinter window is closed. It simply exits the program."""
        exit()
    def check_ip(self,ip):
        """This function checks if a given IP address is active on a specific port.
        It creates a socket and tries to connect to the IP address and port within a specified timeout.
        If the connection is successful, it returns True, otherwise, it returns False."""
        self.testip = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.testip.settimeout(1)
        try:
            self.testip.connect((ip, self.port))
        except:
            return False
        self.testip.close()
        return True


    def main_loop(self):
        """ This function is the main loop of the person class. It creates a tkinter window and sets up the user interface."""
        self.win = tkinter.Tk()
        self.win.configure(bg="#d8fefc")
        self.win.geometry('800x600')
        self.win.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.Main_label = tkinter.Label(self.win, text ="Hello, and welcome to AmitChats!", background= "#d8fefc")
        self.Main_label.config(font= ('Arial', 20))
        self.Main_label.pack(padx=20, pady=5)

        self.main_Frame = tkinter.Frame(self.win,width=100 ,height= 500, background="#d8fefc")
        self.main_Frame.pack(pady=100)



        self.NameFrame = tkinter.Frame(self.main_Frame, width=100 ,height= 500, bg = "#2158d3")
        self.NameFrame.pack(padx=20, pady=1)

        self.name_label = tkinter.Label(self.NameFrame, text="Name: ", bg="lightgray")
        self.name_label.config(font=('Arial', 18))
        self.name_label.grid(row=0, column=1)

        self.name_input_area = tkinter.Text(self.NameFrame, height=2)
        self.name_input_area.config(font=('Arial', 12))
        self.name_input_area.grid(row=1, column=1)


        self.Pass_label = tkinter.Label(self.NameFrame,text= "password:",bg="lightgray")
        self.Pass_label.config(font=('Arial', 18))
        self.Pass_label.grid(row= 4,column=1)

        self.pass_input_area = tkinter.Text(self.NameFrame, height=2)
        self.pass_input_area.config(font=('Arial', 12))
        self.pass_input_area.grid(row=5,column=1)

        self.ip_label = tkinter.Label(self.NameFrame, text="Host Ip:", bg="lightgray")
        self.ip_label.config(font=('Arial', 18))
        self.ip_label.grid(row=6, column=1)

        self.ip_input_area = tkinter.Text(self.NameFrame, height=2)
        self.ip_input_area.config(font=('Arial', 12))
        self.ip_input_area.grid(row=7, column=1)

        self.send_button = tkinter.Button(self.NameFrame, text="SEND",command=self.on_send)
        self.send_button.config(font=('Arial', 12))
        self.send_button.grid(row=8, column=1)




        self.win.mainloop()


    def on_send(self):
        """This function is called when the send button is clicked.
        It retrieves the entered name, password, and host IP address from the input areas.
        It validates the inputs, checks the host IP address,"""
        self.name = self.name_input_area.get('1.0','end')
        self.name = self.name.lower()
        self.name_input_area.delete('1.0','end')
        self.password = self.pass_input_area.get('1.0','end')
        self.pass_input_area.delete('1.0','end')
        self.ip = self.ip_input_area.get('1.0','end')
        self.ip_input_area.delete('1.0', 'end')
        self.ip = self.ip[0:-1]
        if self.ip =="1":
            self.ip = "127.0.0.1"
        open_host = self.check_ip(self.ip)
        self.newName = ""
        self.newPassword = ""
        self.name = self.name.lower()
        for letter in self.name:
            if letter.isalpha() and letter in "abcdefghijklmnopqrstuvwxyz":
                self.newName +=letter
        for number in self.password:
            if number.isdigit():
                self.newPassword +=number
        self.name = self.newName
        self.Password = self.newPassword
        if len(self.name)== 0 or len(self.password)== 0 or not open_host:
            self.No_name_given = tkinter.Label(self.NameFrame,text = "Please enter valid name, password or host!",bg= "lightgray")
            self.No_name_given.config(font=('Arial', 18))
            self.No_name_given.grid(row=9,column=1)
        else:
            try:
                a = client(self.ip,int(self.password),self.port,self.name)
                a.begin()
                self.win.destroy()
            except:
                self.wrong_port = tkinter.Label(self.NameFrame, text= "Please enter a correct password!", bg = "lightgray")
                self.wrong_port.config(font=('Arial', 18))
                self.wrong_port.grid(row=9,column=1)







