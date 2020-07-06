#File name: network.py
#When you need to send information to the server, network.py is used.
#Author Thorbjoern Jonsson
import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        #Open command prompt, type in ipconfig and take the number for IPv4 Address and type it for the server variable.
        #The port is 5555 it is normally not used on a router.
        self.server = "xxx.xxx.x.xx"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048*2))
        except socket.error as e:
            print(e)
