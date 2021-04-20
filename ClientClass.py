import socket
import threading
import random
import sys
class Commands:
    commandDictionary = ['break connection','change connection','change name']
    def addCommand(self,command):
        self.commandDictionary.append(command)
    def removeCommand(self,command):
        self.commandDictionary.remove(command)
    def showCommands(self):
        print(self.commandDictionary)
class ClientClass:
    def __init__(self):
        self.socketClient = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    def connect(self , host, port = random.randint(6000, 10000)):
        self.socketClient.bind((host,port))
        self.server = (socket.gethostbyname(socket.gethostname()) ,5000)
class Client(ClientClass):
    def __init__(self):
        super().__init__()
        self.name = ''
        self.connect(socket.gethostbyname(socket.gethostname()))
        self.commads = Commands()
    def createName(self):
        print('write you name - ')
        self.name = input()
    def changeName(self,newName):
        self.name = newName
    def breakConnections(self):
        sys.exit(0)
    def changeConnections(self, host , port):
        self.connect(host,port)
    def ReadMessageFromServer(self):
        while True:
            try:
                messageServer, addresses = self.socketClient.recvfrom(1024)
                print(messageServer.decode('utf-8'))
            except:
                pass
    def conversations(self):
        print('INFO FOR CLIENTS :\n'
              'PLEASE WRITE BREAK CONNECTIONS IF U WANT COME OUT , \nWRITE CHANGE CONNECTION IF U WANT RECONNECT TO ANOTHER ADDRESS\n AND WRITE CHANGE NAME IF U WANT CGANGE YOUR NAME')
        self.createName()
        self.socketClient.sendto(self.name.encode('utf-8'),self.server)
        threading.Thread(target = self.ReadMessageFromServer).start()
        while True:
            message = input()
            if message == '':
                continue
            if message in self.commads.commandDictionary:
                if message == self.commads.commandDictionary[0]:
                    self.breakConnections()
                elif message == self.commads.commandDictionary[1]:
                    print('write new IPAddress')
                    host = input()
                    print('write new Port ')
                    port = int(input())
                    self.connect(host,port)
                else:
                    print('write new name' )
                    self.changeName(input())
                continue
            messageFromClient = '[' + self.name + ']' + '->' + message
            self.socketClient.sendto(messageFromClient.encode('utf-8'), self.server)
client = Client()
client.conversations()
