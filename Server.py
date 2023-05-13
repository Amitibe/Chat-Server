import socket
import threading
import os
import time
class server:
    def __init__(self,port =5555):
        self.HOST = '0.0.0.0'
        self.PORT =port
        self.passwords = []
        self.rooms = []
        self.name_rooms = []
        self.ipv6 = False
        if self.ipv6:
            self.server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            self.server.bind((self.HOST, self.PORT,0,0))
        else:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((self.HOST,self.PORT))
        self.server.listen()
        self.clients = []
        self.names = []
        print("server_running")
        self.receive()


    def sendMessege(self,name, messege, server_messege= "NOTHING"):
        sendmsg = f"{name} says: {messege}"
        if name == "SERVER":
            try:
                room_password = ''
                for room in self.name_rooms:
                    if server_messege in room:
                        room_password = room[0]
                        print(room_password)
                        break

                for client in self.rooms[self.check_room_number_by_password(room_password)][1:]:
                    client.send(sendmsg.encode())
            except:
                print("first or last person to join")
        else:
            room_password = ''
            for room in self.name_rooms:
                if name in room:
                    room_password = room[0]
                    break

            for client in self.rooms[self.check_room_number_by_password(room_password)][1:]:
                client.send(sendmsg.encode())

    def check_room_number_by_password(self,password):
        for i in range(len(self.rooms)):
            if self.rooms[i][0] == password:
                return i
    def check_room_by_password(self,password):
        for room in self.rooms:
            if room[0] == password:
                return True
        return False

    def add_to_room(self,password,client,name):
        for room in self.rooms:
            if room[0] == password:
                print("trying to add client in room: ", password)
                room.append(client)
        for room in self.name_rooms:
            if room[0] == password:
                room.append(name)

    def remove_from_room(self,client,name):
        for room in self.rooms:
            if client in room:
                room.remove(client)
                break
        for room in self.name_rooms:
            if name in room:
                room.remove(name)
                break
    def check_which_room(self,client):
        for room in self.rooms:
            if client in room:
                return room

    def private(self,messenger ,name, messege):
        try:
            index = self.names.index(name.lower())
            p_client = self.clients[index]
            p_client.send(f"PRIVATE! {messenger} says to you: {messege}".encode())
        except:
            print("Private Error")

    def receive(self):
        while True:
            try:
                self.client, self.client_add = self.server.accept()
                print(f"{self.client_add} connected")
                self.client.send("NAME".encode())
                self.name = self.client.recv(1024).decode()
                self.client.send("PASSWORD".encode())
                self.password = self.client.recv(1024).decode()
                print(f'name: {self.name} password: {self.password}')
                self.clients.append(self.client)
                if len(self.rooms) == 0 or not self.check_room_by_password(self.password):
                    self.rooms.append([self.password,self.client])
                    self.name_rooms.append([self.password,self.name])
                    with open(f'{self.password}','a') as file:
                        file.write("")
                        #self.send_history = self.client.recv(1024).decode()
                else:
                    self.add_to_room(self.password, self.client,self.name)
                    self.client.send("is_done".encode())
                    self.send_history = self.client.recv(1024).decode()
                    with open(f'{self.password}', 'r') as file:
                        history = file.read()
                    print("")
                    self.client.send(history.encode())
                    time.sleep(0.2)
                    self.client.send("DONE".encode())
                print(self.name_rooms)
                self.names.append(self.name.lower())
                self.sendMessege("SERVER",f"{self.name} is now connected. Welcome! :) \n",self.name)
                thread = threading.Thread(target=self.handle, args=(self.client,))
                thread.start()
            except:
                print("no name given, closed connection")
    def handle(self,client):
        while True:
            try:
                self.messege = client.recv(1024).decode()
                room = self.check_which_room(client)
                room_password = room[0]
                with open(f'{room_password}','a') as file:
                    file.write(f'{self.names[self.clients.index(client)]} said: {self.messege} \n')
                print(f"{self.names[self.clients.index(client)]} says: {self.messege}")
                if self.messege[0:3] == "PR ":
                    print("PR has worked")
                    if len(self.clients)>1:
                        try:
                            new_msg = self.messege[3:]
                            splitmsg = new_msg.split(":")
                            name = splitmsg[0]
                            prvt_msg = splitmsg[1]
                            self.private(self.names[self.clients.index(client)], name, prvt_msg)
                        except:
                            print("Error code 1003")
                            client.send(f"SERVER: did not send {self.messege}".encode())
                    else:
                        print("couldnt send msg because you are the only person connected")
                        client.send(f"SERVER: did not send {self.messege} because you are the only person connected".encode())
                else:
                    self.sendMessege(self.names[self.clients.index(client)],self.messege)
            except:
                room = self.check_which_room(self.client)
                self.remove_from_room(client,self.names[self.clients.index(client)]) # currently removing the first person with the name in the first room that it finds them on.
                print("Room:", room)
                try:
                    if len(room) <= 1:
                        os.remove(f'{room[0]}')
                        # with open(f'{room[0]}','w') as file:
                        #    file.write("")
                except:
                    pass
                print(self.name_rooms)
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                name = self.names[index]
                self.names.remove(name)

                self.sendMessege("SERVER",f"{name} has left the chat",name)
                print(self.name_rooms)
                print("client aborted!!!")
                break

