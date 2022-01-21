class Obstacle:
    def __init__(self):
        self.direction = "N"

    def click_obstacle(self):
        if self.direction == None:
            self.direction="N"
            return

        if self.direction == "N":
            self.direction = "E"
            return

        if self.direction == "E":
            self.direction = "S"
            return

        if self.direction == "S":
            self.direction = "W"
            return

        if self.direction == "W":
            self.direction = None
            return

    def check_direction(self):
        return self.direction
