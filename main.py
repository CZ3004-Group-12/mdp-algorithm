import logging
from sys import argv
import constants

from interface.simulator import Simulator

# Logging
logging.basicConfig(level=logging.INFO)


def main():
    print(argv)
    if len(argv) == 2 and str(argv[1]) == "hl":
        constants.HEADLESS = True
    else:
        constants.HEADLESS = False
    x = Simulator()
    


if __name__ == '__main__':
    main()
