import threading
import socket
import time
import datetime
import zlib
import json
#import sys
#import io
# for the text file part
#name = input('Enter name of text file: ')+'.txt'
#open(name, 'a')
# here is for create the file

# with io.FileIO("name", "w") as file:
#        file.write("data")
# here is for write the file 
__author__ = 'Nathaniel Cotton, Zhao Hongyu'

cache = {}

class Network:
    def __init__(self, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        self.socket.bind((socket.gethostbyname('0.0.0.0'),port))


class Recv(threading.Thread):
    def __init__(self, network):
        super().__init__()
        self.setDaemon(False)
        self.network = network
        self.addr = None
        self.lastRecvTime = None

    def run(self):
        while True:
            data, addr = self.network.socket.recvfrom(1024)
            data = zlib.decompress(data)
            data = data.decode('UTF-8')
            data = json.loads(data)
            print(data)
            if addr not in cache:
                cache[addr] = {
                    "lastRecv": datetime.datetime.now(),
                    "messageQueue": []
                }
            else:
                cache[addr]["lastRecv"] = datetime.datetime.now()
                cache[addr]["messageQueue"].append(data)
            #self.addr = addr
            #data = zlib.decompress(data)
            #self.lastRecvTime = datetime.datetime.now()
            #print(data)

    def getClients(self):
        self.purge()
        ret = []
        for key, item in cache.items():
            ret.append(key)
        return ret

    def purge(self):
        currentTime = datetime.datetime.now()
        toPurge = []
        for key, value in cache.items():
            lastRecv = value["lastRecv"]
            if (currentTime - lastRecv).total_seconds() > getTimeout():
                toPurge.append(key)
        for key in toPurge:
            cache.pop(key)




def getTimeout():
    return 60


def printClients(clientList):
    for index in range(len(clientList)):
        print('{} : {}'.format(index+1,clientList[index]))


def main():
    port = 5005
    network = Network(port)
    recv = Recv(network)
    recv.start()
    while True:
        clientList = recv.getClients()
        if len(clientList) == 0:
            print('No Clients')
            time.sleep(5)
        else:
            printClients(clientList)
            clientId = int(input("Client: "))
            command = input("Command: ")
            network.socket.sendto(command.encode('UTF-8'),clientList[clientId-1])



if __name__ == '__main__':
    main()
