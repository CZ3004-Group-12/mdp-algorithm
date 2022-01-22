from simulator.buttons import Button
from map import colours


class Panel(object):

    def __init__(self, surface):

        self.connect_button = Button(surface, colours.LIGHT_BLUE, 650, 120, 100, 25, "Connect to RPI", colours.BLACK)

