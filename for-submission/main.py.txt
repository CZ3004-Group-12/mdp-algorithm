import logging
from sys import argv
import constants

from interface.simulator import Simulator

# Logging
logging.basicConfig(level=logging.INFO)


def main():
    constants.HEADLESS = False
    constants.CENTER_ON_OBS = False
    if len(argv) != 1:
        for arg in argv:
            if (arg == "hl"):
                constants.HEADLESS = True
                print("Running in headless mode")
            elif (arg == "cen"):
                constants.CENTER_ON_OBS = True
                print("Pathing will center on obstacle")
    x = Simulator()
    


if __name__ == '__main__':
    main()
