class DestinationNodes:
    def __init__(self, x_coordinates, y_coordinates, angle):
        self.x_coordinates = x_coordinates
        self.y_coordinates = y_coordinates
        self.angle = angle
        self.visited = False

    def get_pos(self):
        return [self.x_coordinates, self.y_coordinates]

    def get_angle(self):
        return self.angle

    def visit_node(self, x, y):
        if self.x_coordinates == x and self.y_coordinates == y and self.visited == False:
            self.visited = True
            return True
        else:
            return False

    def check_visited(self):
        return self.visited