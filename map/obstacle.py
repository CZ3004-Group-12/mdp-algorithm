import map.constants
from map import constants

class Obstacle:
    def __init__(self):
        self.direction = map.constants.NORTH

    def obstacle_clicked(self):
        if self.direction is None:
            self.direction = map.constants.NORTH
            return

        if self.direction == map.constants.NORTH:
            self.direction = map.constants.EAST
            return

        if self.direction == map.constants.EAST:
            self.direction = map.constants.SOUTH
            return

        if self.direction == map.constants.SOUTH:
            self.direction = map.constants.WEST
            return

        if self.direction == map.constants.WEST:
            self.direction = None
            return

    def get_direction(self):
        return self.direction
