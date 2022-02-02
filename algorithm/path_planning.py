import constants


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
        print(a, b, x, y)
        print(robot_direction, target_direction)
        if robot_direction == target_direction:
            if abs(a - x) <= 2 and b < y:
                a, b, x, y = self.transpose_orientation(a, b, target_direction, x, y)
                print("AR1")
                self.AR1(a, b, x, y)
            elif a < x and b == y:
                a, b, x, y = self.transpose_orientation(a, b, target_direction, x, y)
                print("AR2")
                self.AR2(a, b, x, y)
            elif a == x and b > y:
                a, b, x, y = self.transpose_orientation(a, b, target_direction, x, y)
                print("AR3")
                self.AR3(a, b, x, y)
            elif a > x and b == y:
                a, b, x, y = self.transpose_orientation(a, b, target_direction, x, y)
                print("AR4")
                self.AR4(a, b, x, y)
            elif abs(a - x) > 2 and a < x and b < y:
                a, b, x, y = self.transpose_orientation(a, b, target_direction, x, y)
                print("AR5")
                self.AR5(a, b, x, y)
            elif a < x and b > y:
                a, b, x, y = self.transpose_orientation(a, b, target_direction, x, y)
                print("AR6")
                self.AR6(a, b, x, y)
            elif a > x and b > y:
                a, b, x, y = self.transpose_orientation(a, b, target_direction, x, y)
                print("AR7")
                self.AR7(a, b, x, y)
            elif abs(a - x) > 2 and a > x and b < y:
                a, b, x, y = self.transpose_orientation(a, b, target_direction, x, y)
                print("AR8")
                self.AR8(a, b, x, y)

        elif abs(robot_direction - target_direction) == 180:
            if a == x and b < y:
                a, b, x, y = self.transpose_orientation(a, b, target_direction, x, y)
                print("BR1")
                self.BR1(a, b, x, y)
            elif a < x and b == y:
                a, b, x, y = self.transpose_orientation(a, b, target_direction, x, y)
                print("BR2")
                self.BR2(a, b, x, y)
            elif abs(a-x) <= 2 and b > y:
                a, b, x, y = self.transpose_orientation(a, b, target_direction, x, y)
                print("BR3")
                self.BR3(a, b, x, y)
            elif a > x and b == y:
                a, b, x, y = self.transpose_orientation(a, b, target_direction, x, y)
                print("BR4")
                self.BR4(a, b, x, y)
            elif a < x and b < y:
                a, b, x, y = self.transpose_orientation(a, b, target_direction, x, y)
                print("BR5")
                self.BR5(a, b, x, y)
            elif abs(a-x) > 2 and a < x and b > y:
                a, b, x, y = self.transpose_orientation(a, b, target_direction, x, y)
                print("BR6")
                self.BR6(a, b, x, y)
            elif abs(a-x) > 2 and a > x and b > y:
                a, b, x, y = self.transpose_orientation(a, b, target_direction, x, y)
                print("BR7")
                self.BR7(a, b, x, y)
            elif a > x and b < y:
                a, b, x, y = self.transpose_orientation(a, b, target_direction, x, y)
                print("BR8")
                self.BR8(a, b, x, y)

        elif (robot_direction - target_direction == 90) or \
                (target_direction == constants.SOUTH and robot_direction == constants.EAST):
            if a == x and b < y:
                a, b, x, y = self.transpose_orientation(a, b, target_direction, x, y)
                print("CR1")
                self.CR1(a, b, x, y)
            elif a < x and b == y:
                self.CR2(a, b, x, y)
                a, b, x, y = self.transpose_orientation(a, b, target_direction, x, y)
                print("CR2")
            elif a == x and b > y:
                a, b, x, y = self.transpose_orientation(a, b, target_direction, x, y)
                print("CR3")
                self.CR3(a, b, x, y)
            elif a > x and b == y:
                a, b, x, y = self.transpose_orientation(a, b, target_direction, x, y)
                print("CR4")
                self.CR4(a, b, x, y)
            elif a < x and b < y:
                a, b, x, y = self.transpose_orientation(a, b, target_direction, x, y)
                print("CR5")
                self.CR5(a, b, x, y)
            elif a < x and b > y:
                a, b, x, y = self.transpose_orientation(a, b, target_direction, x, y)
                print("CR6")
                self.CR6(a, b, x, y)
            elif a > x and b > y:
                a, b, x, y = self.transpose_orientation(a, b, target_direction, x, y)
                print("CR7")
                self.CR7(a, b, x, y)
            elif a > x and b < y:
                a, b, x, y = self.transpose_orientation(a, b, target_direction, x, y)
                print("CR8")
                self.CR8(a, b, x, y)

        elif (robot_direction - target_direction == -90) or \
                (target_direction == constants.EAST and robot_direction == constants.SOUTH):
            if a == x and b < y:
                a, b, x, y = self.transpose_orientation(a, b, target_direction, x, y)
                print("DR1")
                self.DR1(a, b, x, y)
            elif a < x and b == y:
                a, b, x, y = self.transpose_orientation(a, b, target_direction, x, y)
                print("DR2")
                self.DR2(a, b, x, y)
            elif a == x and b > y:
                a, b, x, y = self.transpose_orientation(a, b, target_direction, x, y)
                print("DR3")
                self.DR3(a, b, x, y)
            elif a > x and b == y:
                a, b, x, y = self.transpose_orientation(a, b, target_direction, x, y)
                print("DR4")
                self.DR4(a, b, x, y)
            elif a < x and b < y:
                a, b, x, y = self.transpose_orientation(a, b, target_direction, x, y)
                print("DR5")
                self.DR5(a, b, x, y)
            elif a < x and b > y:
                a, b, x, y = self.transpose_orientation(a, b, target_direction, x, y)
                print("DR6")
                self.DR6(a, b, x, y)
            elif a > x and b > y:
                a, b, x, y = self.transpose_orientation(a, b, target_direction, x, y)
                print("DR7")
                self.DR7(a, b, x, y)
            elif a > x and b < y:
                a, b, x, y = self.transpose_orientation(a, b, target_direction, x, y)
                print("DR8")
                self.DR8(a, b, x, y)

        else:
            return

    def AR1(self, a, b, x, y):
        if a - x <= 0:
            # Forward Left
            self.robot.move_forward_steer_left()
            for i in range(int(abs(a - x))):
                self.robot.move_forward()
            # Forward Left
            self.robot.move_forward_steer_left()
            for i in range(int(abs(b - y))):
                self.robot.move_forward()
            # Forward Left
            self.robot.move_forward_steer_left()
            # Forward Left
            self.robot.move_forward_steer_left()

        else:
            # Forward Right
            self.robot.move_forward_steer_right()
            for i in range(int(abs(a - x))):
                self.robot.move_forward()
            # Forward Right
            self.robot.move_forward_steer_right()
            for i in range(int(abs(b - y))):
                self.robot.move_forward()
            # Forward Right
            self.robot.move_forward_steer_right()
            # Forward Right
            self.robot.move_forward_steer_right()

    def AR2(self, a, b, x, y):
        # Forward by 6
        for i in range(6):
            self.robot.move_backward()
        # Apply AR6
        a, b, x, y = self.transpose_orientation(abs(a), abs(b), self.target_direction,
                                                self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])
        self.AR6(a, b, x, y)

    def AR3(self, a, b, x, y):
        # Forward by abs(b-y)
        for i in range(int(abs(b - y))):
            self.robot.move_forward()

    def AR4(self, a, b, x, y):
        for i in range(6):
            self.robot.move_backward()
        a, b, x, y = self.transpose_orientation(abs(a), abs(b), self.target_direction,
                                                self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])
        self.AR7(a, b, x, y)

    def AR5(self, a, b, x, y):
        for i in range(int(abs(b - y))):
            self.robot.move_backward()
        a, b, x, y = self.transpose_orientation(abs(a), abs(b), self.target_direction,
                                                self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])
        self.AR2(a, b, x, y)

    def AR6(self, a, b, x, y):
        if abs(a - x) >= 6 and abs(b - y) >= 6:
            # Forward Left
            self.robot.move_forward_steer_left()
            for i in range(int(abs(a - x) - 6)):
                self.robot.move_forward()
            self.robot.move_forward_steer_right()
            for i in range(int(abs(b - y) - 6)):
                self.robot.move_forward()

        elif abs(a - x) < 6 and abs(b - y) >= 6:
            # Forward Left
            self.robot.move_forward_steer_left()
            for i in range(int(6 - abs(a - x))):
                self.robot.move_backward()
            # Forward Right
            self.robot.move_forward_steer_right()
            for i in range(int(abs(b - y) - 6)):
                self.robot.move_forward()

        elif abs(a - x) >= 6 and abs(b - y) < 6:
            for i in range(int(6 - abs(b - y))):
                self.robot.move_backward()
            # Forward Left
            self.robot.move_forward_steer_left()
            for i in range(int(abs(a - x) - 6)):
                self.robot.move_forward()
            # Forward Right
            self.robot.move_forward_steer_right()

        elif abs(a - x) < 6 and abs(b - y) < 6:
            for i in range(int(6 - abs(b - y))):
                self.robot.move_backward()
            # Forward Left
            self.robot.move_forward_steer_left()
            for i in range(int(6 - abs(a - x))):
                self.robot.move_backward()
            # Forward Right
            self.robot.move_forward_steer_right()

    def AR7(self, a, b, x, y):
        if abs(a - x) >= 6 and abs(b - y) >= 6:
            # Forward Right
            self.robot.move_forward_steer_right()
            for i in range(int(abs(a - x) - 6)):
                self.robot.move_forward()
            # Forward Left
            self.robot.move_forward_steer_left()
            for i in range(int(abs(b - y) - 6)):
                self.robot.move_forward()

        elif abs(a - x) < 6 and abs(b - y) >= 6:
            # Forward Right
            self.robot.move_forward_steer_right()
            for i in range(int(6 - abs(a - x))):
                self.robot.move_backward()
            # Forward Left
            self.robot.move_forward_steer_left()
            for i in range(int(abs(b - y) - 6)):
                self.robot.move_forward()

        elif abs(a - x) >= 6 and abs(b - y) < 6:
            for i in range(int(6 - abs(b - y))):
                self.robot.move_backward()
            # Forward Right
            self.robot.move_forward_steer_right()
            for i in range(int(abs(a - x) - 6)):
                self.robot.move_forward()
            # Forward Left
            self.robot.move_forward_steer_left()

        elif abs(a - x) < 6 and abs(b - y) < 6:
            for i in range(int(6 - abs(b - y))):
                self.robot.move_backward()
            self.robot.move_forward_steer_right()
            for i in range(int(6 - abs(a - x))):
                self.robot.move_backward()
            # Forward Left
            self.robot.move_forward_steer_left()

    def AR8(self, a, b, x, y):
        for i in range(int(abs(b - y))):
            self.robot.move_backward()
        a, b, x, y = self.transpose_orientation(abs(a), abs(b), self.target_direction,
                                                self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])
        self.AR4(a, b, x, y)

    def BR1(self, a, b, x, y):
        self.robot.move_forward_steer_right()
        self.robot.move_backward_steer_left()
        for i in range(int(abs(b - y) + 6)):
            self.robot.move_forward()

    def BR2(self, a, b, x, y):
        for i in range(3):
            self.robot.move_backward()
        self.robot.move_forward_steer_left()
        for i in range(int(abs(a - x))):
            self.robot.move_forward()
        self.robot.move_backward_steer_right()
        for i in range(3):
            self.robot.move_forward()

    def BR3(self, a, b, x, y):
        if abs(b-y) <= 2:
            self.robot.move_forward_steer_right()
            self.robot.move_backward_steer_left()
            for i in range(int(6 - abs(b - y))):
                self.robot.move_forward()
        else:
            if abs(b-y) < 10:
                for i in range(int(10 - abs(b - y))):
                    self.robot.move_backward()
            else:
                for i in range(int(abs(b - y) - 10)):
                    self.robot.move_forward()
            self.robot.move_forward_steer_right()
            if abs(a) - abs(x) > 0:
                for i in range(int(abs(a - x))):
                    self.robot.move_forward()
            elif abs(a) - abs(x) < 0:
                for i in range(int(abs(a - x))):
                    self.robot.move_backward()
            self.robot.move_forward_steer_left()
            self.robot.move_forward()
            self.robot.move_forward_steer_left()
            for i in range(6):
                self.robot.move_forward()
            self.robot.move_backward_steer_right()
            for i in range(3):
                self.robot.move_forward()

    def BR4(self, a, b, x, y):
        for i in range(3):
            self.robot.move_backward()
        self.robot.move_forward_steer_right()
        for i in range(int(abs(a - x))):
            self.robot.move_forward()
        self.robot.move_backward_steer_left()
        for i in range(3):
            self.robot.move_forward()

    def BR5(self, a, b, x, y):
        if abs(a-x) <= 2:
            self.robot.move_forward_steer_right()
            a, b, x, y = self.transpose_orientation(abs(a), abs(b), self.target_direction,
                                                    self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])
            self.DR8(a, b, x, y)
        else:
            for i in range(int(abs(b-y))):
                self.robot.move_backward()
            a, b, x, y = self.transpose_orientation(abs(a), abs(b), self.target_direction,
                                                    self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])
            self.BR2(a, b, x, y)

    def BR6(self, a, b, x, y):
        for i in range(int(abs(b - y))):
            self.robot.move_forward()
        a, b, x, y = self.transpose_orientation(abs(a), abs(b), self.target_direction,
                                                self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])
        self.BR2(a, b, x, y)

    def BR7(self, a, b, x, y):
        for i in range(int(abs(b - y))):
            self.robot.move_forward()
        a, b, x, y = self.transpose_orientation(abs(a), abs(b), self.target_direction,
                                                self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])
        self.BR4(a, b, x, y)

    def BR8(self, a, b, x, y):
        if abs(b - y) < 6:
            for i in range(int(6 - abs(b - y))):
                self.robot.move_forward()
        else:
            for i in range(int(abs(b - y) - 6)):
                self.robot.move_backward()
        self.robot.move_backward_steer_left()
        if abs(a - x) <= 2:
            for i in range(int(3 - abs(a - x))):
                self.robot.move_forward()
        else:
            for i in range(int(abs(a - x))):
                self.robot.move_forward()
        self.robot.move_forward_steer_right()

    def CR1(self, a, b, x, y):
        # Backward Left
        self.robot.move_backward_steer_left()
        a, b, x, y = self.transpose_orientation(abs(a), abs(b), self.target_direction,
                                                self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])
        self.AR5(a, b, x, y)

    def CR2(self, a, b, x, y):
        for i in range(int(abs(b - y) + 3)):
            self.robot.move_forward()
        a, b, x, y = self.transpose_orientation(abs(a), abs(b), self.target_direction,
                                                self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])
        self.CR4(a, b, x, y)
        pass

    def CR3(self, a, b, x, y):
        a, b, x, y = self.transpose_orientation(abs(a), abs(b), self.target_direction,
                                                self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])
        self.CR6(a, b, x, y)
        pass

    def CR4(self, a, b, x, y):
        if abs(a - x) <= 2:
            for i in range(int(3 - abs(a - x))):
                self.robot.move_forward()
        else:
            for i in range(int(abs(x - a) - 3)):
                self.robot.move_backward()
        # Backward Left
        self.robot.move_backward_steer_left()
        for i in range(int(abs(b - y))):
            self.robot.move_forward()

    def CR5(self, a, b, x, y):
        # Backward Left
        self.robot.move_backward_steer_left()
        if abs(y - b) > 3:
            a, b, x, y = self.transpose_orientation(abs(a), abs(b), self.target_direction,
                                                    self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])
            self.AR5(a, b, x, y)
        elif abs(y - b) == 3:
            a, b, x, y = self.transpose_orientation(abs(a), abs(b), self.target_direction,
                                                    self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])
            self.AR2(a, b, x, y)
        else:
            a, b, x, y = self.transpose_orientation(abs(a), abs(b), self.target_direction,
                                                    self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])
            self.AR6(a, b, x, y)
        pass

    def CR6(self, a, b, x, y):
        for i in range(int(abs(a - x) + 3)):
            self.robot.move_forward()
        a, b, x, y = self.transpose_orientation(abs(a), abs(b), self.target_direction,
                                                self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])
        self.CR7(a, b, x, y)

    def CR7(self, a, b, x, y):
        for i in range(int(abs(x - a) - 3)):
            self.robot.move_backward()
        # Backward Left
        self.robot.move_backward_steer_left()
        for i in range(int(abs(b - y))):
            self.robot.move_forward()

    def CR8(self, a, b, x, y):
        if abs(x - a) <= 5:
            for i in range(int(6 - abs(x - a))):
                self.robot.move_forward()
        # Backward Left
        self.robot.move_backward_steer_left()
        if abs(y - b) > 3:
            a, b, x, y = self.transpose_orientation(abs(a), abs(b), self.target_direction,
                                                    self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])
            self.AR8(a, b, x, y)
        elif abs(y - b) == 3:
            a, b, x, y = self.transpose_orientation(abs(a), abs(b), self.target_direction,
                                                    self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])
            self.AR4(a, b, x, y)
        else:
            a, b, x, y = self.transpose_orientation(abs(a), abs(b), self.target_direction,
                                                    self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])
            self.AR7(a, b, x, y)

    def DR1(self, a, b, x, y):
        self.robot.move_backward_steer_right()
        a, b, x, y = self.transpose_orientation(abs(a), abs(b), self.target_direction,
                                                self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])
        self.AR8(a, b, x, y)

    def DR2(self, a, b, x, y):
        if abs(a - x) <= 2:
            for i in range(int(3 - abs(a - x))):
                self.robot.move_forward()
        else:
            for i in range(int(abs(x - a) - 3)):
                self.robot.move_backward()
        # Backward Right
        self.robot.move_backward_steer_right()
        for i in range(int(abs(b - y))):
            self.robot.move_forward()

    def DR3(self, a, b, x, y):
        a, b, x, y = self.transpose_orientation(abs(a), abs(b), self.target_direction,
                                                self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])
        self.DR7(a, b, x, y)

    def DR4(self, a, b, x, y):
        for i in range(int(abs(b - y) + 3)):
            self.robot.move_forward()
        a, b, x, y = self.transpose_orientation(abs(a), abs(b), self.target_direction,
                                                self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])
        self.DR2(a, b, x, y)

    def DR5(self, a, b, x, y):
        if abs(x - a) <= 5:
            for i in range(int(6 - abs(x - a))):
                self.robot.move_forward()
        # Backward Right
        self.robot.move_backward_steer_right()
        if abs(y - b) > 3:
            a, b, x, y = self.transpose_orientation(abs(a), abs(b), self.target_direction,
                                                    self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])
            self.AR5(a, b, x, y)
        elif abs(y - b) == 3:
            a, b, x, y = self.transpose_orientation(abs(a), abs(b), self.target_direction,
                                                    self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])
            self.AR2(a, b, x, y)
        else:
            a, b, x, y = self.transpose_orientation(abs(a), abs(b), self.target_direction,
                                                    self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])
            self.AR6(a, b, x, y)

    def DR6(self, a, b, x, y):
        for i in range(int(abs(x - a) - 3)):
            self.robot.move_backward()
        # Backward Right
        self.robot.move_backward_steer_right()
        for i in range(int(abs(b - y))):
            self.robot.move_forward()

    def DR7(self, a, b, x, y):
        for i in range(int(abs(a - x) + 3)):
            self.robot.move_forward()
        a, b, x, y = self.transpose_orientation(abs(a), abs(b), self.target_direction,
                                                self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])
        self.DR6(a, b, x, y)

    def DR8(self, a, b, x, y):
        # Backward Right
        self.robot.move_backward_steer_right()
        if abs(y - b) > 3:
            a, b, x, y = self.transpose_orientation(abs(a), abs(b), self.target_direction,
                                                    self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])
            self.AR8(a, b, x, y)
        elif abs(y - b) == 3:
            a, b, x, y = self.transpose_orientation(abs(a), abs(b), self.target_direction,
                                                    self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])
            self.AR4(a, b, x, y)
        else:
            a, b, x, y = self.transpose_orientation(abs(a), abs(b), self.target_direction,
                                                    self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])
            self.AR7(a, b, x, y)
        pass
