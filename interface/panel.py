from interface.buttons import Button
from map import colours


class Panel(object):

    def __init__(self, surface):
        # Buttons
        self.buttons = []

        start_button = Button(surface, colours.GREEN, 650, 500, 100, 25, "START", colours.BLACK, "START")
        self.buttons.append(start_button)

        connect_button = Button(surface, colours.LIGHT_BLUE, 650, 120, 110, 25, "Connect to RPI", colours.BLACK, "CONNECT")
        self.buttons.append(connect_button)
        disconnect_button = Button(surface, colours.LIGHT_BLUE, 650, 150, 150, 25, "Disconnect from RPI", colours.BLACK, "DISCONNECT")
        self.buttons.append(disconnect_button)

    def button_clicked(self, button):
        button.pressed()
