import threading
import tkinter
import time
from Client import Client as client
class person:
    def __init__(self, name = 'amit', port = 5555):
        self.name = name
        self.port = port
        self.chats = []
        self.thread = threading.Thread(target=self.main_loop)
        self.thread.start()

    def on_closing(self):
        exit()

    def main_loop(self):
        self.win = tkinter.Tk()
        self.win.configure(bg="#F6E1C3")
        self.win.geometry('800x500')
        self.win.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.Main_label = tkinter.Label(self.win, text ="Hello, and welcome to AmitChats!", background= "#E9A178")
        self.Main_label.config(font= ('Arial', 20))
        self.Main_label.pack(padx=20, pady=5)

        self.main_Frame = tkinter.Frame(self.win,width=100 ,height= 500, background="#A84448")
        self.main_Frame.pack(pady=100)



        self.NameFrame = tkinter.Frame(self.main_Frame, width=100 ,height= 500, bg = "#A84448")
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
        self.send_button = tkinter.Button(self.NameFrame, text="SEND",command=self.on_send)
        self.send_button.config(font=('Arial', 12))
        self.send_button.grid(row=6, column=1)


        self.win.mainloop()

    def on_send(self):
        self.name = self.name_input_area.get('1.0','end')
        self.name = self.name.lower()
        self.name_input_area.delete('1.0','end')
        self.password = self.pass_input_area.get('1.0','end')
        self.pass_input_area.delete('1.0','end')
        self.newName = ""
        self.newPassword = ""
        for letter in self.name:
            if letter.isalpha():
                self.newName +=letter
        for number in self.password:
            if number.isdigit():
                self.newPassword +=number
        self.name = self.newName
        self.Password = self.newPassword
        if len(self.name)== 0 or len(self.password)== 0:
            self.No_name_given = tkinter.Label(self.NameFrame,text = "Please enter valid name and password!",bg= "lightgray")
            self.No_name_given.config(font=('Arial', 18))
            self.No_name_given.grid(row=7,column=1)
        else:
            try:
                a= client('10.0.0.18',int(self.password),self.port,self.name)
                a.begin()
                self.win.destroy()
            except:
                self.wrong_port = tkinter.Label(self.NameFrame, text= "Please enter a correct password!", bg = "lightgray")
                self.wrong_port.config(font=('Arial', 18))
                self.wrong_port.grid(row=8,column=1)



a = person()
time.sleep(0.5)
b = person()



