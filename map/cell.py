# status enum:
# 0 is empty
# 1 is starting area
# 2 is restricted area around obstacle
# 3 is obstacle
from map.obstacle import Obstacle


class Cell:
    def __init__(self, x_coordinate, y_coordinate, status):
        self.direction = None
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.status = status
        self.obstacle = None

    def cell_clicked(self):
        if self.y_coordinate < 4 and self.x_coordinate < 4:
            return
        if self.obstacle is None:
            self.obstacle = Obstacle()
            return
        self.obstacle.obstacle_clicked()
        return self.obstacle.get_direction()

    def get_obstacle_direction(self):
        if self.obstacle is None:
            return None
        return self.obstacle.get_direction()

    def get_cell_status(self):
        return self.status

    def get_xcoord(self):
        return self.x_coordinate

    def get_ycoord(self):
        return self.y_coordinate
