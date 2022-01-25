from interface.buttons import Button
import constants


class Panel(object):

    def __init__(self, surface):
        # Buttons
        self.buttons = []

        start_button = Button(surface, constants.GREEN, 650, 500, 100, 25, "START", constants.BLACK, "START")
        self.buttons.append(start_button)

        connect_button = Button(surface, constants.LIGHT_BLUE, 650, 120, 110, 25, "Connect to RPI", constants.BLACK, "CONNECT")
        self.buttons.append(connect_button)
        disconnect_button = Button(surface, constants.LIGHT_BLUE, 650, 150, 150, 25, "Disconnect from RPI", constants.BLACK, "DISCONNECT")
        self.buttons.append(disconnect_button)

    def button_clicked(self, button):
        button.pressed()
