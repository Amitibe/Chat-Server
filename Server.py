import socket
import threading
import os
import time
import EncodingProtocol

class server:
    def __init__(self,port =5555):
        self.HOST = '0.0.0.0'
        self.PORT = port
        self.passwords = []
        self.rooms = []
        self.name_rooms = []
        self.clientKeys =[]
        self.ipv6 = False
        if self.ipv6:
            self.server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            self.server.bind((self.HOST, self.PORT, 0, 0))
        else:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((self.HOST,self.PORT))
        self.server.listen()
        self.clients = []
        self.names = []
        self.key = EncodingProtocol.getRandomKey()
        EncodingProtocol.setKeyword(self.key)
        print("server_running")

        self.receive()


    def sendMessege(self,name, messege, server_messege= "NOTHING", removing = False):
        """This function is responsible for sending messages to clients.
         It takes the name of the sender, the message to be sent, an optional server message,
         and a flag to indicate whether the sender is being removed. It sends the message to all clients in a specific room."""
        sendmsg = f"{name} says: {messege}"
        if name == "SERVER":
            room_password = ''
            for room in self.name_rooms:
                if server_messege in room:
                    room_password = room[0]
                    print(room_password)
                    break
            if not removing:
                for client in self.rooms[self.check_room_number_by_password(room_password)][1:]:
                    client.send(sendmsg.encode())
            else:
                for client in self.rooms[self.check_room_number_by_password(room_password)][1:]:
                    if client is not None:
                        client.send(sendmsg.encode())
        else:
            room_password = ''
            for room in self.name_rooms:
                if name in room:
                    room_password = room[0]
                    break

            for client in self.rooms[self.check_room_number_by_password(room_password)][1:]:
                encodedmsg = self.encode(client, messege)
                final_message = f"{name} says: {encodedmsg}"
                client.send(final_message.encode())

    def send_to_room(self,name,messege,room):
        """: This function sends a message to all clients in a specific room.
        It takes the name of the sender, the message to be sent, and the room to which the message should be sent."""
        try:
            if len(room) >1:
                sendmsg = f"{name} says: {messege}"
                for client in room[1:]:
                        encodedmsg = self.encode(client,sendmsg)
                        client.send((encodedmsg).encode())
        except:
            pass
    def check_room_number_by_password(self,password):
        """returns the index of the room from its password"""
        for i in range(len(self.rooms)):
            if self.rooms[i][0] == password:
                return i
    def check_room_by_password(self,password):
        """it returns whether a room exists with the password given"""
        for room in self.rooms:
            if room[0] == password:
                return True
        return False

    def add_to_room(self,password,client,name):
        """ This function adds a client and its associated name to a specific room identified by the password. """
        for room in self.rooms:
            if room[0] == password:
                print("trying to add client in room: ", password)
                room.append(client)
        for room in self.name_rooms:
            if room[0] == password:
                room.append(name)

    def remove_from_room(self,client,name):
        """This function removes a client and its associated name from their respective room."""
        for room in self.rooms:
            if client in room:
                room.remove(client)
                break
        for room in self.name_rooms:
            if name in room:
                room.remove(name)
                break
    def check_which_room(self,client):
        """This function checks which room a specific client belongs to"""
        for room in self.rooms:
            if client in room:
                return room

    def private(self,messenger ,name, messege):
        """This function sends a private message from one client to another."""
        try:
            index = self.names.index(name.lower())
            p_client = self.clients[index]
            encodedmsg = self.encode(p_client,f"PRIVATE! {messenger} says to you: {messege}" )
            p_client.send(encodedmsg.encode())
        except:
            print("Private Error")


    def makeHistory(self, history : list, client):
        truelist = history[:-1]
        for i in range(len(truelist)):
            truelist[i] = self.encode(client, truelist[i]) + '___'
        return truelist

    def handleHistory(self, history: list, client):
        for msg in history:
            print(msg, "THIS IS THE MSG")
            client.send(msg.encode())


    def decode(self, client, msg):
        for c in self.clientKeys:
            if client in c:
                return EncodingProtocol.decode(msg, c[1])

        return "----"

    def encode(self, client, msg):
        for c in self.clientKeys:
            if client in c:
                return EncodingProtocol.encode(msg, c[1])
        return "----"
    def receive(self):
        """This function runs in an infinite loop and handles the reception of incoming client connections.
         It accepts a client's connection, receives the client's name and password,
         adds the client to the appropriate room or creates a new room if necessary.
         It also handles the sending of previous chat history to the connected client
         and starts a new thread to handle the client's messages."""
        while True:
            try:
                self.client, self.client_add = self.server.accept()
                print(f"{self.client_add} connected")
                self.client.send("NAME".encode())
                self.name = self.client.recv(1024).decode()
                self.client.send("PASSWORD".encode())
                self.password = self.client.recv(1024).decode()
                randomkey = EncodingProtocol.getRandomKey()
                self.clientKeys.append([self.client, randomkey])
                self.client.send(f"KEY-{randomkey}".encode())
                print(f'name: {self.name} password: {self.password}')
                self.clients.append(self.client)
                if len(self.rooms) == 0 or not self.check_room_by_password(self.password):
                    self.rooms.append([self.password,self.client])
                    self.name_rooms.append([self.password,self.name])
                    with open(f'{self.password}','a') as file:
                        file.write("")
                else:
                    self.add_to_room(self.password, self.client,self.name)
                    self.client.send("is_done".encode())
                    self.send_history = self.client.recv(1024).decode()
                    with open(f'{self.password}', 'r') as file:
                        history = file.read()

                    historyList = history.split("\n")
                    encodedHistory = self.makeHistory(historyList, self.client)

                    self.handleHistory(encodedHistory,self.client)

                    time.sleep(0.2)
                    self.client.send("DONE".encode())
                print(self.name_rooms)
                self.names.append(self.name.lower())
                with open(f'{self.password}', 'a') as file:
                    file.write(f"SERVER says {self.name} is now connected. Welcome! :) \n")
                self.sendMessege("SERVER",f"{self.name} is now connected. Welcome! :) \n",self.name)
                thread = threading.Thread(target=self.handle, args=(self.client,))
                thread.start()
            except:
                print("Connection lost")
    def handle(self,client):
        """This function handles the messages received from a specific client.
         It runs in an infinite loop, receiving messages from the client, processing them,
         and sending them to other clients in the same room.
        It also handles special commands such as private messages and playing a game."""
        while True:
            try:
                self.messege = client.recv(1024).decode()
                newmessege = self.decode(client, self.messege)
                self.messege = newmessege
                print(self.messege)
                room = self.check_which_room(client)
                room_password = room[0]
                if not self.messege[0:3] == "pr ":
                    with open(f'{room_password}','a') as file:
                        file.write(f'{self.names[self.clients.index(client)]} said: {self.messege} \n')
                print(f"{self.names[self.clients.index(client)]} says: {self.messege}")
                if self.messege[0:3] == "pr ":
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
                            encodedmsg = self.encode(client, f"SERVER: did not send {self.messege}")
                            client.send(encodedmsg.encode())
                    else:
                        print("couldnt send msg because you are the only person connected")
                        client.send(f"SERVER: did not send {self.messege} because you are the only person connected".encode())
                elif self.messege == "play runner":
                    self.sendMessege(self.names[self.clients.index(client)],"I am playing runner!")
                else:
                    self.sendMessege(self.names[self.clients.index(client)],self.messege)
            except:

                nameroom = []
                print("client left")
                index = self.clients.index(client)
                print(index , '1')
                print(len(self.names),'2')
                name = self.names[index]
                room = self.check_which_room(client)
                for i in self.name_rooms:
                    if name in i:
                        nameroom =i
                        break

                self.remove_from_room(client, self.names[self.clients.index(client)])
                print(len(room))
                print(room)
                if len(room) <= 1:
                    os.remove(f'{room[0]}')
                    self.rooms.remove(room)
                    self.name_rooms.remove(nameroom)
                self.names.remove(name)
                self.clients.remove(client)
                self.send_to_room("SERVER",f'{name} has left the chat',room)
                client.close()
                break

