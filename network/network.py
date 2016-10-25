import socket
import zlib
from network.network_new import prepare

"""

"""

__author__ = "Nathaniel Cotton, Hongyu Zhao"
__email__ = "nec2887@rit.edu, hz1242@g.rit.edu"


class NetUtil:
    __slots__ = ['netutil']

    class __NetUtil:
        __slots__ = ['socket','messageCounter']

        def __init__(self):
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.messageCounter = 0

    instance = None

    def __new__(cls, *args, **kwargs):
        if NetUtil.instance is None:
            NetUtil.instance = NetUtil.__NetUtil()
        return NetUtil.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)


def send(info):
    """
    Sends data
    :param info:
    :return:
    """
    # TODO add sync
    message_id = NetUtil().messageCounter
    NetUtil().messageCounter = (NetUtil().messageCounter + 1) % 10000
    index = 0
    while len(info) > getMessageLimit():
        tem = info[:getMessageLimit()]
        info = info[getMessageLimit():]
        #tem = zlib.compress(tem)
        message = prepare(index,message_id,tem)
        NetUtil().socket.sendto(message, getSendTo())
        index += 1
    #info = zlib.compress(info.encode('UTF-8'))
    info = prepare(index,message_id,info,True)
    NetUtil().socket.sendto(info, getSendTo())


def recv():
    """
    Receives data
    :return:
    """
    reply, addr = NetUtil().socket.recvfrom(1024)
    return reply


def getSendTo():
    return ('localhost', 5005) #use ifconfig to get the current ipv4 address then use that for our target address no localhost

def getMessageLimit():
    return 500
