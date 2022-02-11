import logging
from sys import argv

from interface.simulator import Simulator

# Logging
logging.basicConfig(level=logging.INFO)


def main():
    print(argv)
    if len(argv) == 2 and str(argv[1]) == "hl":
        x =Simulator(True)
    else:
        x= Simulator(False)
    


if __name__ == '__main__':
    main()
