import threading
import socket
import time
import datetime


class Network:
    def __init__(self, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('localhost',port))


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
            self.addr = addr
            self.lastRecvTime = datetime.datetime.now()
            print(data)

    def getClient(self):
        while self.addr is None:
            time.sleep(0)
        return self.addr  # ( IP, PORT )

    def getLastRecvTime(self):
        return self.lastRecvTime

    def clientIsDead(self):
        return True


def getTimeout():
    return 60


def main():
    port = 5005
    network = Network(port)
    recv = Recv(network)
    recv.start()
    client_ip, client_port = recv.getClient()
    while recv.clientIsDead() and recv.getLastRecvTime() is not None and (
        datetime.datetime.now() - recv.getLastRecvTime()).total_seconds() < getTimeout():
        command = input('Command: ')
        network.socket.sendto(command.encode('UTF-8'), (client_ip, client_port))


if __name__ == '__main__':
    main()
