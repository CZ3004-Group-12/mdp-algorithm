class Obstacle:
    def __init__(self, x_coordinate, y_coordinate):
        # TODO: if possible, combine obstacle class into cell
        # TODO: set unique ids to identify different obstacles
        # TODO: need boolean parameter to mark obstacle as visited
        # TODO: need to define cells which car must reach to consider as "visited" a obstacle
        self.direction = "N"
        self.obstacle_id = str(x_coordinate) + "-" + str(y_coordinate)
        self.visited = False

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

    def get_obstacle_id(self):
        return self.obstacle_id

    def mark_visited(self):
        self.visited = True
