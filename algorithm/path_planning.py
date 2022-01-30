import constants

dt = 0.02
# dt = round(self.clock.get_time() / 1000, 2)


class PathPlan(object):

    def __init__(self, grid, robot, fastest_route):

        self.grid = grid
        self.robot = robot
        self.fastest_route = fastest_route

    def start_robot(self):
        for target in self.fastest_route:
            target_x = target[0]
            target_y = target[1]
            target_direction = target[2]
            obstacle_cell = target[3]

            robot_x = self.robot.get_grid_pos()[0]
            robot_y = self.robot.get_grid_pos()[1]
            robot_direction = self.robot.get_angle_of_rotation()

            # Target Coordinates: (a, b); Robot Coordinates: (x, y)
            a, b, x, y = self.transpose_orientation(target_x, target_y, target_direction, robot_x, robot_y)

            self.plan_trip_by_robot_target_directions(a, b, x, y, robot_direction, target_direction)

    def transpose_orientation(self, target_x, target_y, target_direction, robot_x, robot_y):
        if target_direction == constants.NORTH:
            a = target_x
            b = target_y
            x = robot_x
            y = robot_y
            return a, b, x, y
        elif target_direction == constants.EAST:
            a = -target_y
            b = target_x
            x = -robot_y
            y = robot_x
            return a, b, x, y
        elif target_direction == constants.SOUTH:
            a = -target_x
            b = -target_y
            x = -robot_x
            y = -robot_y
            return a, b, x, y
        elif target_direction == constants.WEST:
            a = target_y
            b = -target_x
            x = robot_y
            y = -robot_x
            return a, b, x, y
        else:
            return 0, 0, 0, 0

    # Refer to Google Doc for details of different permutations
    def plan_trip_by_robot_target_directions(self, a, b, x, y, robot_direction, target_direction):
        if robot_direction == target_direction:
            if abs(a - x) <= 2 and b < y:
                self.AR1(a, b, x, y)
            elif a < x and b == y:
                self.AR2(a, b, x, y)
            elif a == x and b > y:
                self.AR3(a, b, x, y)
            # TODO: add the other 5 cases
            
        elif abs(robot_direction - target_direction) == 180:
            if abs(a - x) <= 2 and b < y:
                self.BR1(a, b, x, y)
            elif a < x and b == y:
                self.BR2(a, b, x, y)
            elif a == x and b > y:
                self.BR3(a, b, x, y)
            # TODO: add the other 5 cases
            
        elif (robot_direction - target_direction == 90) or \
                (target_direction == constants.SOUTH and robot_direction == constants.EAST):
            if a == x and b < y:
                self.CR1(a, b, x, y)
            elif a < x and b == y:
                self.CR2(a, b, x, y)
            elif a == x and b > y:
                self.CR3(a, b, x, y)
            # TODO: add the other 5 cases
            
        elif (robot_direction - target_direction == -90) or \
                (target_direction == constants.EAST and robot_direction == constants.SOUTH):
            if a == x and b < y:
                self.DR1(a, b, x, y)
            elif a < x and b == y:
                self.DR2(a, b, x, y)
            elif a == x and b > y:
                self.DR3(a, b, x, y)
            # TODO: add the other 5 cases
            
        else:
            return

    def AR1(self, a, b, x, y):
        pass

    def AR2(self, a, b, x, y):
        pass

    def AR3(self, a, b, x, y):
        # Forward by abs(b-y)
        for i in range(int(abs(b-y))):
            self.robot.move_forward(dt)
