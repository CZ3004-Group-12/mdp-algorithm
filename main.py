import logging
from sys import argv
from constants import HEADLESS

from interface.simulator import Simulator

# Logging
logging.basicConfig(level=logging.INFO)


def main():
    print(argv)
    if len(argv) == 2 and str(argv[1]) == "hl":
        HEADLESS = True
    else:
        HEADLESS = False
    x = Simulator()
    


if __name__ == '__main__':
    main()
