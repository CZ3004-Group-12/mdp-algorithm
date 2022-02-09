import constants


class Obstacle:
    def __init__(self, x_coordinate, y_coordinate):
        # TODO: if possible, combine obstacle class into cell
        # TODO: set unique ids to identify different obstacles
        # TODO: need boolean parameter to mark obstacle as visited
        # TODO: need to define cells which car must reach to consider as "visited" a obstacle
        self.direction = constants.NORTH
        self.obstacle_id = str(x_coordinate) + "-" + str(y_coordinate)
        self.visited = False

    def obstacle_clicked(self):
        if self.direction is None:
            self.direction = constants.NORTH
            return

        if self.direction == constants.NORTH:
            self.direction = constants.EAST
            return

        if self.direction == constants.EAST:
            self.direction = constants.SOUTH
            return

        if self.direction == constants.SOUTH:
            self.direction = constants.WEST
            return

        if self.direction == constants.WEST:
            self.direction = None
            return

    def set_direction(self, dir):
        self.direction = dir

    def get_direction(self):
        return self.direction

    def get_obstacle_id(self):
        return self.obstacle_id

    def mark_visited(self):
        self.visited = True
