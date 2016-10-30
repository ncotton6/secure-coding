import threading
import socket
import time
import datetime
import zlib
import json

__author__ = 'Nathaniel Cotton, Zhao Hongyu'

cache = {}


class Network:
    def __init__(self, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.socket.bind((socket.gethostbyname('0.0.0.0'), port))


class ProcessingThread(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            for key, value in cache.items():
                print('here is the message comes from ' + str(key))
                messagetem = {}
                for i in range(len(value['messageQueue'])):
                    msgId = value['messageQueue'][i]['message_id']
                    if msgId not in messagetem:
                        messagetem[msgId] = []
                    messagetem[value['messageQueue'][i]['message_id']].append({
                        "index": value['messageQueue'][i]['index'],
                        "data": value['messageQueue'][i]['data']
                    })
                for key, value in messagetem.items():
                    indexMax = 0git
                    for i in range(len(value)):
                        indexMax = max(value['index'], indexMax)
                    messStr = [None for x in range(indexMax)]
                    for i in range(len(value)):
                        messStr[value['index']] = value['data']
                    for i in range(len(messStr)):
                        if (messStr[i]):
                            print(messStr[i])
                        else:
                            print('we lost this message')
            time.sleep(1)


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
            # print(data)
            if addr not in cache:
                cache[addr] = {
                    "lastRecv": datetime.datetime.now(),
                    "messageQueue": [data]
                }
            else:
                cache[addr]["lastRecv"] = datetime.datetime.now()
                cache[addr]["messageQueue"].append(data)
                # self.addr = addr
                # data = zlib.decompress(data)
                # self.lastRecvTime = datetime.datetime.now()
                # print(data)

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
        print('{} : {}'.format(index + 1, clientList[index]))


def main():
    port = 5005
    network = Network(port)
    recv = Recv(network)
    recv.start()
    proc = ProcessingThread()
    proc.start()
    while True:
        try:
            clientList = recv.getClients()
            if len(clientList) == 0:
                print('No Clients')
                time.sleep(5)
            else:
                clientId = 0
                if len(clientList) != 1:
                    printClients(clientList)
                    clientId = int(input("Client: "))
                command = input("Command: ")
                network.socket.sendto(command.encode('UTF-8'), clientList[clientId - 1])
        except Exception as e:
            pass


if __name__ == '__main__':
    main()
