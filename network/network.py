import socket

"""

"""

__author__ = "Nathaniel Cotton"
__email__ = "nec2887@rit.edu"


class NetUtil:
    __slots__ = ['netutil']

    class __NetUtil:
        __slots__ = ['socket']

        def __init__(self):
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    instance = None

    def __new__(cls, *args, **kwargs):
        if NetUtil.instance is not None:
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
    NetUtil().socket.sendto(info,getSendTo())


def recv():
    """
    Receives data
    :return:
    """
    reply, addr = NetUtil().socket.recvfrom(1024)
    return reply


def getSendTo():
    return ('localhost', 5055)
