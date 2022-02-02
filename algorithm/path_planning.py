import constants

dt = 0.04


# dt = round(self.clock.get_time() / 1000, 2)


class PathPlan(object):

    def __init__(self, grid, robot, fastest_route):

        self.grid = grid
        self.robot = robot
        self.fastest_route = fastest_route
        self.target_x = 0
        self.target_y = 0
        self.target_direction = 0
        self.robot_x = self.robot.get_grid_pos()[0]
        self.robot_y = self.robot.get_grid_pos()[1]
        self.robot_direction = self.robot.get_angle_of_rotation()


    def start_robot(self):
        for target in self.fastest_route[1:]:
            self.target_x = target[0]
            self.target_y = target[1]
            self.target_direction = target[2]
            obstacle_cell = target[3]

            self.robot_x = self.robot.get_grid_pos()[0]
            self.robot_y = self.robot.get_grid_pos()[1]
            self.robot_direction = self.robot.get_angle_of_rotation()

            # Target Coordinates: (a, b); Robot Coordinates: (x, y)
            self.plan_trip_by_robot_target_directions(self.target_x, self.target_y, self.robot_x, self.robot_y,
                                                      self.robot_direction, self.target_direction)

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
            elif a < x and b == y:
                self.AR4(a, b, x, y)
            elif abs(a - x) > 2 and a < x and b < y:
                self.AR5(a, b, x, y)
            elif a < x and b > y:
                self.AR6(a, b, x, y)
            elif a > x and b > y:
                self.AR7(a, b, x, y)
            elif abs(a - x) > 2 and a > x and b < y:
                self.AR8(a, b, x, y)
            # TODO: add the other 5 cases

        elif abs(robot_direction - target_direction) == 180:
            if abs(a - x) <= 2 and b < y:
                self.BR1(a, b, x, y)
            elif a < x and b == y:
                self.BR2(a, b, x, y)
            elif a == x and b > y:
                self.BR3(a, b, x, y)
            elif a < x and b == y:
                self.BR4(a, b, x, y)
            elif abs(a - x) > 2 and a < x and b < y:
                self.BR5(a, b, x, y)
            elif a < x and b > y:
                self.BR6(a, b, x, y)
            elif a > x and b > y:
                self.BR7(a, b, x, y)
            elif abs(a - x) > 2 and a > x and b < y:
                self.BR8(a, b, x, y)
            # TODO: add the other 5 cases

        elif (robot_direction - target_direction == 90) or \
                (target_direction == constants.SOUTH and robot_direction == constants.EAST):
            if a == x and b < y:
                self.CR1(a, b, x, y)
            elif a < x and b == y:
                self.CR2(a, b, x, y)
            elif a == x and b > y:
                self.CR3(a, b, x, y)
            elif a < x and b == y:
                self.CR4(a, b, x, y)
            elif a < x and b < y:
                self.CR5(a, b, x, y)
            elif a < x and b > y:
                self.CR6(a, b, x, y)
            elif a > x and b > y:
                self.CR7(a, b, x, y)
            elif a > x and b < y:
                self.CR8(a, b, x, y)
            # TODO: add the other 5 cases

        elif (robot_direction - target_direction == -90) or \
                (target_direction == constants.EAST and robot_direction == constants.SOUTH):
            if a == x and b < y:
                self.DR1(a, b, x, y)
            elif a < x and b == y:
                self.DR2(a, b, x, y)
            elif a == x and b > y:
                self.DR3(a, b, x, y)
            elif a < x and b == y:
                self.DR4(a, b, x, y)
            elif a < x and b < y:
                self.DR5(a, b, x, y)
            elif a < x and b > y:
                self.DR6(a, b, x, y)
            elif a > x and b > y:
                self.DR7(a, b, x, y)
            elif a > x and b < y:
                self.DR8(a, b, x, y)
            # TODO: add the other 5 cases

        else:
            return

    def AR1(self, a, b, x, y):
        if a - x <= 0:
            # Forward Left
            self.robot.move_forward_steer_left(dt)
            for i in range(int(abs(a - x))):
                self.robot.move_forward(dt)
            # Forward Left
            self.robot.move_forward_steer_left(dt)
            for i in range(int(abs(b - y))):
                self.robot.move_forward(dt)
            # Forward Left
            self.robot.move_forward_steer_left(dt)
            # Forward Left
            self.robot.move_forward_steer_left(dt)

        else:
            # Forward Right
            self.robot.move_forward_steer_right(dt)
            for i in range(int(abs(a - x))):
                self.robot.move_forward(dt)
            # Forward Right
            self.robot.move_forward_steer_right(dt)
            for i in range(int(abs(b - y))):
                self.robot.move_forward(dt)
            # Forward Right
            self.robot.move_forward_steer_right(dt)
            # Forward Right
            self.robot.move_forward_steer_right(dt)

    def AR2(self, a, b, x, y):
        # Forward by 6
        for i in range(6):
            self.robot.move_backward(dt)
        # Apply AR6
        self.AR6(a, b, self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])

    def AR3(self, a, b, x, y):
        # Forward by abs(b-y)
        for i in range(int(abs(b - y))):
            self.robot.move_forward(dt)

    def AR4(self, a, b, x, y):
        for i in range(6):
            self.robot.move_backward(dt)
        self.AR7(a, b, self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])

    def AR5(self, a, b, x, y):
        for i in range(int(abs(b - y))):
            self.robot.move_backward(dt)
        self.AR2(a, b, self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])

    def AR6(self, a, b, x, y):
        if abs(a - x) >= 6 and abs(b - y) >= 6:
            # Forward Left
            self.robot.move_forward_steer_left(dt)
            for i in range(int(abs(a - x) - 6)):
                self.robot.move_forward(dt)
            self.robot.move_forward_steer_right(dt)
            for i in range(int(abs(b - y) - 6)):
                self.robot.move_forward(dt)

        elif abs(a - x) < 6 and abs(b - y) >= 6:
            # Forward Left
            self.robot.move_forward_steer_left(dt)
            for i in range(int(6 - abs(a - x))):
                self.robot.move_backward(dt)
            # Forward Right
            self.robot.move_forward_steer_right(dt)
            for i in range(int(abs(b - y) - 6)):
                self.robot.move_forward(dt)

        elif abs(a - x) >= 6 and abs(b - y) < 6:
            for i in range(int(6 - abs(b - y))):
                self.robot.move_backward(dt)
            # Forward Left
            self.robot.move_forward_steer_left(dt)
            for i in range(int(abs(a - x) - 6)):
                self.robot.move_forward(dt)
            # Forward Right
            self.robot.move_forward_steer_right(dt)

        elif abs(a - x) < 6 and abs(b - y) < 6:
            for i in range(int(6 - abs(b - y))):
                self.robot.move_backward(dt)
            # Forward Left
            self.robot.move_forward_steer_left(dt)
            for i in range(int(6 - abs(a - x))):
                self.robot.move_backward(dt)
            # Forward Right
            self.robot.move_forward_steer_right(dt)

    def AR7(self, a, b, x, y):
        if abs(a - x) >= 6 and abs(b - y) >= 6:
            # Forward Right
            self.robot.move_forward_steer_right(dt)
            for i in range(int(abs(a - x) - 6)):
                self.robot.move_forward(dt)
            # Forward Left
            self.robot.move_forward_steer_left(dt)
            for i in range(int(abs(b - y) - 6)):
                self.robot.move_forward(dt)

        elif abs(a - x) < 6 and abs(b - y) >= 6:
            # Forward Right
            self.robot.move_forward_steer_right(dt)
            for i in range(int(6 - abs(a - x))):
                self.robot.move_backward(dt)
            # Forward Left
            self.robot.move_forward_steer_left(dt)
            for i in range(int(abs(b - y) - 6)):
                self.robot.move_forward(dt)

        elif abs(a - x) >= 6 and abs(b - y) < 6:
            for i in range(int(6 - abs(b - y))):
                self.robot.move_backward(dt)
            # Forward Right
            self.robot.move_forward_steer_right(dt)
            for i in range(int(abs(a - x) - 6)):
                self.robot.move_forward(dt)
            # Forward Left
            self.robot.move_forward_steer_left(dt)

        elif abs(a - x) < 6 and abs(b - y) < 6:
            for i in range(int(6 - abs(b - y))):
                self.robot.move_backward(dt)
            self.robot.move_forward_steer_right(dt)
            for i in range(int(6 - abs(a - x))):
                self.robot.move_backward(dt)
            # Forward Left
            self.robot.move_forward_steer_left(dt)

    def AR8(self, a, b, x, y):
        for i in range(int(abs(b - y))):
            self.robot.move_backward(dt)
        self.AR4(a, b, self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])

    def BR1(self, a, b, x, y):
        if abs(b - y) < 10:
            for i in range(10 - abs(b - y)):
                self.robot.move_backward(dt)
        # Forward Left
        self.robot.move_forward_steer_left(dt)
        if a - x > 0:
            for i in range(abs(a - x)):
                self.robot.move_forward(dt)
        # Forward Right
        self.robot.move_forward_steer_right(dt)
        for i in range(abs(b - y) - 6):
            self.robot.move_forward(dt)
        self.BR2(a, b, self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])

    def BR2(self, a, b, x, y):
        for i in range(6):
            self.robot.move_forward(dt)
        self.BR6(a, b, self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])

    def BR3(self, a, b, x, y):
        if abs(b - y) < 6:
            for i in range(6 - abs(b - y)):
                self.robot.move_forward(dt)
        # Backward Right
        self.robot.move_backward_steer_right(dt)
        # Forward Right
        self.robot.move_forward_steer_right(dt)
        for i in range(abs(b - y) - 6):
            self.robot.move_forward(dt)

    def BR4(self, a, b, x, y):
        for i in range(6):
            self.robot.move_forward(dt)
        self.BR7(a, b, self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])

    def BR5(self, a, b, x, y):
        for i in range(abs(a - x)):
            self.robot.move_forward(dt)
        self.BR2(a, b, self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])

    def BR6(self, a, b, x, y):
        if abs(b - y) < 6:
            for i in range(6 - abs(b - y)):
                self.robot.move_forward(dt)
        # Backward Right
        self.robot.move_backward_steer_right(dt)
        for i in range(abs(a - x)):
            self.robot.move_backward(dt)
        # Forward Left
        self.robot.move_forward_steer_left(dt)
        for i in range(abs(b - y) - 6):
            self.robot.move_forward(dt)

    def BR7(self, a, b, x, y):
        if abs(b - y) < 6:
            for i in range(6 - abs(b - y)):
                self.robot.move_forward(dt)
        # Backward Left
        self.robot.move_backward_steer_left(dt)
        for i in range(abs(a - x)):
            self.robot.move_backward(dt)
        # Forward Right
        self.robot.move_forward_steer_right(dt)
        for i in range(abs(b - y) - 6):
            self.robot.move_forward(dt)

    def BR8(self, a, b, x, y):
        for i in range(abs(a - x)):
            self.robot.move_forward(dt)
        self.BR4(a, b, self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])

    def CR1(self, a, b, x, y):
        # Backward Left
        self.robot.move_backward_steer_left(dt)
        self.AR5(a, b, self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])

    def CR2(self, a, b, x, y):
        for i in range(abs(b - y) + 3):
            self.robot.move_forward(dt)
        self.CR4(a, b, self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])
        pass

    def CR3(self, a, b, x, y):
        self.CR6(a, b, self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])
        pass

    def CR4(self, a, b, x, y):
        if abs(a - x) <= 2:
            for i in range(3 - abs(a - x)):
                self.robot.move_forward(dt)
        else:
            for i in range(abs(x - a) - 3):
                self.robot.move_backward(dt)
        # Backward Left
        self.robot.move_backward_steer_left(dt)
        for i in range(abs(b - y)):
            self.robot.move_forward(dt)

    def CR5(self, a, b, x, y):
        # Backward Left
        self.robot.move_backward_steer_left(dt)
        if abs(y - b) > 3:
            self.AR5(a, b, self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])
        elif abs(y - b) == 3:
            self.AR2(a, b, self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])
        else:
            self.AR6(a, b, self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])
        pass

    def CR6(self, a, b, x, y):
        for i in range(abs(a - x) + 3):
            self.robot.move_forward(dt)
        self.CR7(a, b, self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])

    def CR7(self, a, b, x, y):
        for i in range(abs(x - a) - 3):
            self.robot.move_backward(dt)
        # Backward Left
        self.robot.move_backward_steer_left(dt)
        for i in range(abs(b - y)):
            self.robot.move_forward(dt)

    def CR8(self, a, b, x, y):
        if abs(x - a) <= 5:
            for i in range(6 - abs(x - a)):
                self.robot.move_forward(dt)
        # Backward Left
        self.robot.move_backward_steer_left(dt)
        if abs(y - b) > 3:
            self.AR8(a, b, self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])
        elif abs(y - b) == 3:
            self.AR4(a, b, self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])
        else:
            self.AR7(a, b, self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])

    def DR1(self, a, b, x, y):
        self.robot.move_backward_steer_right(dt)
        self.AR8(a, b, self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])

    def DR2(self, a, b, x, y):
        if abs(a - x) <= 2:
            for i in range(3 - abs(a - x)):
                self.robot.move_forward(dt)
        else:
            for i in range(abs(x - a) - 3):
                self.robot.move_backward(dt)
        # Backward Right
        self.robot.move_backward_steer_right(dt)
        for i in range(abs(b - y)):
            self.robot.move_forward(dt)

    def DR3(self, a, b, x, y):
        self.DR7(a, b, self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])

    def DR4(self, a, b, x, y):
        for i in range(abs(b - y) + 3):
            self.robot.move_forward(dt)
        self.DR2(a, b, self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])

    def DR5(self, a, b, x, y):
        if abs(x - a) <= 5:
            for i in range(6 - abs(x - a)):
                self.robot.move_forward(dt)
        # Backward Right
        self.robot.move_backward_steer_right(dt)
        if abs(y - b) > 3:
            self.AR5(a, b, self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])
        elif abs(y - b) == 3:
            self.AR2(a, b, self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])
        else:
            self.AR6(a, b, self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])

    def DR6(self, a, b, x, y):
        for i in range(abs(x - a) - 3):
            self.robot.move_backward(dt)
        # Backward Right
        self.robot.move_backward_steer_right(dt)
        for i in range(abs(b - y)):
            self.robot.move_forward(dt)

    def DR7(self, a, b, x, y):
        for i in range(abs(a - x) + 3):
            self.robot.move_forward(dt)
        self.DR6(a, b, self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])

    def DR8(self, a, b, x, y):
        # Backward Right
        self.robot.move_backward_steer_right(dt)
        if abs(y - b) > 3:
            self.AR8(a, b, self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])
        elif abs(y - b) == 3:
            self.AR4(a, b, self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])
        else:
            self.AR7(a, b, self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])
        pass
