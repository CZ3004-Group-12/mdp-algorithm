from interface.buttons import Button
import constants


class Panel(object):

    def __init__(self, surface):
        # Buttons
        self.buttons = []

        start_button = Button(surface, constants.GREEN, 650, 500, 100, 25, "START", constants.BLACK, "START")
        self.buttons.append(start_button)
        reset_button = Button(surface, constants.RED, 650, 470, 100, 25, "Reset", constants.BLACK, "RESET")
        self.buttons.append(reset_button)

        connect_button = Button(surface, constants.LIGHT_BLUE, 650, 120, 110, 25, "Connect to RPI", constants.BLACK, "CONNECT")
        self.buttons.append(connect_button)
        disconnect_button = Button(surface, constants.LIGHT_BLUE, 650, 150, 150, 25, "Disconnect from RPI", constants.BLACK, "DISCONNECT")
        self.buttons.append(disconnect_button)
        draw_path_button = Button(surface, constants.GREEN, 650, 180, 150, 25, "Draw Path", constants.BLACK, "DRAWPATH")
        self.buttons.append(draw_path_button)

        # For testing
        forward_button = Button(surface, constants.LIGHT_GREEN, 800, 120, 100, 25, "Forward", constants.BLACK, "FORWARD")
        self.buttons.append(forward_button)
        backward_button = Button(surface, constants.LIGHT_GREEN, 800, 150, 100, 25, "Backward", constants.BLACK, "BACKWARD")
        self.buttons.append(backward_button)
        for_right_button = Button(surface, constants.LIGHT_GREEN, 800, 180, 100, 25, "Forward R", constants.BLACK, "FORWARD_RIGHT")
        self.buttons.append(for_right_button)
        for_left_button = Button(surface, constants.LIGHT_GREEN, 800, 210, 100, 25, "Forward L", constants.BLACK, "FORWARD_LEFT")
        self.buttons.append(for_left_button)
        back_right_button = Button(surface, constants.LIGHT_GREEN, 800, 240, 100, 25, "Backward R", constants.BLACK, "BACKWARD_RIGHT")
        self.buttons.append(back_right_button)
        back_left_button = Button(surface, constants.LIGHT_GREEN, 800, 270, 100, 25, "Backward L", constants.BLACK, "BACKWARD_LEFT")
        self.buttons.append(back_left_button)


    def button_clicked(self, button):
        return button.pressed()

    def get_button_clicked(self, button):
        return button.get_function()
