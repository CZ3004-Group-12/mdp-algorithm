class Obstacle:
    def __init__(self):
        # TODO: if possible, combine obstacle class into cell
        # TODO: set unique ids to identify different obstacles
        # TODO: need boolean parameter to mark obstacle as visited
        # TODO: need to define cells which car must reach to consider as "visited" a obstacle
        self.direction = "N"

    def obstacle_clicked(self):
        if self.direction is None:
            self.direction = "N"
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

    def get_direction(self):
        return self.direction
