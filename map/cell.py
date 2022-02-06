# status enum:
# 0 is empty
# 1 is starting area
# 2 is boundary area around obstacle
# 3 is obstacle
# 4 is obstacle visited
# 5 and above is path to take
from map.obstacle import Obstacle


class Cell:
    def __init__(self, x_coordinate, y_coordinate, status):
        # self.direction = None
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.status = status
        self.obstacle = None

    def cell_clicked(self):
        if self.y_coordinate < 4 and self.x_coordinate < 4:
            return
        if self.obstacle is None:
            self.obstacle = Obstacle(self.x_coordinate, self.y_coordinate)
            self.status = 3
            return
        self.obstacle.obstacle_clicked()
        if self.obstacle.get_direction() is None:
            self.obstacle = None
            self.status = 0

    def set_obstacle_boundary_status(self):
        self.status = 2

    def set_starting_area_status(self):
        self.status = 1

    def set_empty_status(self):
        self.status = 0

    def set_obstacle_visited_status(self):
        self.status = 4

    def set_path_status(self, num):
        self.status = 5

    def get_obstacle(self):
        return self.obstacle

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
