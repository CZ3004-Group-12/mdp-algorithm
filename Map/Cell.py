# status enum:
# 0 is empty
# 1 is starting area
# 2 is restricted area around obstacle
# 3 is obstacle
from Map.Obstacle import Obstacle


class Cell:
    def __init__(self, x_coordinate, y_coordinate, status):
        self.direction = None
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.obstacle = None

    def clickcell(self):
        if self.obstacle is None:
            self.obstacle = Obstacle()
            return
        self.obstacle.click_obstacle()
        return self.obstacle.check_direction()

    def checkdirection(self):
        if self.obstacle is None:
            return None
        return self.obstacle.check_direction()
