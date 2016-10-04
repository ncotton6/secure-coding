"""
This model file contains general utility functions along with model objects to be used
with the keylogger implementations.
"""

__author__ = "Nathaniel Cotton"
__email__ = "nec2887@rit.edu"

import sys

class Key:

    __slots__ = ['key','ctrl','shift']

    def __init__(self,key,ctrl,shift):
        self.key = key
        self.ctrl = ctrl
        self.shift = shift


def getKeyLogger():
    if 'linux' == sys.platform:
        from keylogger.linuxkeylogger import LinuxKeyLogger
        return LinuxKeyLogger()
    elif 'windows' == sys.platform:
        from keylogger.windowskeylogger import WindowsKeyLogger
        return WindowsKeyLogger()

    return None

