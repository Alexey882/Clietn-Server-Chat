import socket
import threading
import queue
import re
from datetime import datetime
class Logger:
    def __init__(self,nameLogFile):
        self.logFile = nameLogFile+'.log'
        open(self.logFile,'w').close()
    def createNewLog(self,infoMessage):
        with open(self.logFile,'a') as f:
            f.write(infoMessage+'\n')
            f.close()
    def showLogs(self):
        with open(self.logFile,'r') as f:
            for line in f:
                print(line)
            f.close()
class Censor:
    dictionaryCensor = ['fuck']
    def checkMessage(self , messageClient):
        messageWords = re.split('[,]|[ ]|[ ,]|[  ]|[ , ]|[:]|[->]|\\[\\]' , messageClient)
        negativeWord = []
        for word in messageWords:
            if word in self.dictionaryCensor:
                negativeWord.append(word)
        return negativeWord
    def changeMessageToCensor(self,messageClient):
        result = self.checkMessage(messageClient)
        if(len(result)>0):
            for word in result:
                messageClient = messageClient.replace(word, '*' * len(word))
        return messageClient
    def showCensorWord(self):
        return self.dictionaryCensor
    def addWordToCensor(self,word):
        self.dictionaryCensor.append(word)
    def deleteWordFromCensor(self,word):
        self.dictionaryCensor.remove(word)
class ServerClass:
    def __init__(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.port = 5000
        self.host = socket.gethostbyname(socket.gethostname())
        self.connecting()
    def changePort(self):
        print('input port to connection`s - ')
        self.port = int(input())
    def connecting(self):
        self.serverSocket.bind((self.host, self.port))
class Server(ServerClass):
    def __init__(self):
        super().__init__()
        self.censor = Censor()
        self.logger = Logger('Message')
        self.messageArchives = queue.Queue()
        self.server = self.serverSocket
        self.clientsInTheChat = set()
        self.blackListUser = set()
    def updateMessageWithInfo(self,messageClient,nameOfClient):
        return datetime.strftime(datetime.now(),"%A, %d. %B %Y %I:%M%p") +  ": "+ nameOfClient + " : " + messageClient
    def ReadMessagesFromClient(self):
        while True:
            messageClient, addressClient = self.server.recvfrom(1024)
            self.messageArchives.put((messageClient, addressClient))
    def addClient(self,addrClient):
        self.clientsInTheChat.add(addrClient)
    def removeClient(self ,addrClient):
        self.clientsInTheChat.remove(addrClient)
    def blackList(self,userId):
        self.blackListUser.add(userId)
    def conversation(self):
        global name
        threading.Thread(target=self.ReadMessagesFromClient).start()
        print('Server Running...')
        while True:
            while not self.messageArchives.empty():
                messageClient, addressClient = self.messageArchives.get()
                messageClient = messageClient.decode('utf-8')
                if addressClient not in self.clientsInTheChat:
                    self.addClient(addressClient)
                    continue
                if (self.censor.changeMessageToCensor(messageClient)!=messageClient):
                    self.blackList(addressClient)
                if addressClient in self.blackListUser:
                    name = ''
                    for i in range(len(messageClient)):
                        if(messageClient[i]=='['):
                            while(True):
                                name+=messageClient[i]
                                if(messageClient[i]==']'):
                                    break
                                i+=1
                    messageClient = name +' This user in the black list'
                print(self.updateMessageWithInfo(self.censor.changeMessageToCensor(messageClient), str(addressClient)))
                for client in self.clientsInTheChat:
                    if client != addressClient:
                        self.server.sendto(self.censor.changeMessageToCensor(messageClient).encode('utf-8'),client)
                self.logger.createNewLog(self.updateMessageWithInfo(self.censor.changeMessageToCensor(messageClient),str(addressClient)))
server = Server()
server.conversation()