from robot.robot import BorderException
from robot.robot import ObstacleException
from robot.robot import ObstacleTurnException
import constants

MARGIN = 2


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

    def undo_target_transpose(self, target_x, target_y, target_direction):
        if target_direction == constants.NORTH:
            a = target_x
            b = target_y
            return a, b
        elif target_direction == constants.EAST:
            a = target_y
            b = -target_x
            return a, b
        elif target_direction == constants.SOUTH:
            a = -target_x
            b = -target_y
            return a, b
        elif target_direction == constants.WEST:
            a = -target_y
            b = target_x
            return a, b
        else:
            return 0, 0

    # Refer to Google Doc for details of different permutations
    # TODO: robot at target location but wrong direction
    def plan_trip_by_robot_target_directions(self, a, b, x, y, robot_direction, target_direction):
        try:
            print(a, b, x, y)
            print(robot_direction, target_direction)
            initial_a = a
            initial_b = b
            a, b, x, y = self.transpose_orientation(a, b, target_direction, x, y)
            if robot_direction == target_direction:
                if abs(a - x) <= 2 and b < y:
                    print("AR1")
                    self.AR1(a, b, x, y)
                elif a < x and b == y:
                    print("AR2")
                    self.AR2(a, b, x, y)
                elif a == x and b > y:
                    print("AR3")
                    self.AR3(a, b, x, y)
                elif a > x and b == y:
                    print("AR4")
                    self.AR4(a, b, x, y)
                elif abs(a - x) > 2 and a < x and b < y:
                    print("AR5")
                    self.AR5(a, b, x, y)
                elif a < x and b > y:
                    print("AR6")
                    self.AR6(a, b, x, y)
                elif a > x and b > y:
                    print("AR7")
                    self.AR7(a, b, x, y)
                elif abs(a - x) > 2 and a > x and b < y:
                    print("AR8")
                    self.AR8(a, b, x, y)
                else:
                    print("no case")

            elif abs(robot_direction - target_direction) == 180:
                if a == x and b < y:
                    print("BR1")
                    self.BR1(a, b, x, y)
                elif a < x and b == y:
                    print("BR2")
                    self.BR2(a, b, x, y)
                elif a == x and b > y:
                    print("BR3")
                    self.BR3(a, b, x, y)
                elif a > x and b == y:
                    print("BR4")
                    self.BR4(a, b, x, y)
                elif a < x and b < y:
                    print("BR5")
                    self.BR5(a, b, x, y)
                elif a < x and b > y:
                    print("BR6")
                    self.BR6(a, b, x, y)
                elif a > x and b > y:
                    print("BR7")
                    self.BR7(a, b, x, y)
                elif a > x and b < y:
                    print("BR8")
                    self.BR8(a, b, x, y)
                elif a == x and b == y:
                    print("BR9")
                    self.BR9(a, b, x, y)
                else:
                    print("no case")

            elif (robot_direction - target_direction == 90) or \
                    (target_direction == constants.SOUTH and robot_direction == constants.EAST):
                if a == x and b < y:
                    print("CR1")
                    self.CR1(a, b, x, y)
                elif a < x and b == y:
                    self.CR2(a, b, x, y)
                    print("CR2")
                elif a == x and b > y:
                    print("CR3")
                    self.CR3(a, b, x, y)
                elif a > x and b == y:
                    print("CR4")
                    self.CR4(a, b, x, y)
                elif a < x and b < y:
                    print("CR5")
                    self.CR5(a, b, x, y)
                elif a < x and b > y:
                    print("CR6")
                    self.CR6(a, b, x, y)
                elif a > x and b > y:
                    print("CR7")
                    self.CR7(a, b, x, y)
                elif a > x and b < y:
                    print("CR8")
                    self.CR8(a, b, x, y)
                elif a == x and b == y:
                    print("CR9")
                    self.CR9(a, b, x, y)
                else:
                    print("no case")

            elif (robot_direction - target_direction == -90) or \
                    (target_direction == constants.EAST and robot_direction == constants.SOUTH):
                if a == x and b < y:
                    print("DR1")
                    self.DR1(a, b, x, y)
                elif a < x and b == y:
                    print("DR2")
                    self.DR2(a, b, x, y)
                elif a == x and b > y:
                    print("DR3")
                    self.DR3(a, b, x, y)
                elif a > x and b == y:
                    print("DR4")
                    self.DR4(a, b, x, y)
                elif a < x and b < y:
                    print("DR5")
                    self.DR5(a, b, x, y)
                elif a < x and b > y:
                    print("DR6")
                    self.DR6(a, b, x, y)
                elif a > x and b > y:
                    print("DR7")
                    self.DR7(a, b, x, y)
                elif a > x and b < y:
                    print("DR8")
                    self.DR8(a, b, x, y)
                elif a == x and b == y:
                    print("DR9")
                    self.DR9(a, b, x, y)
                else:
                    print("no case")

            else:
                return

            self.check_reached_target(initial_a, initial_b)
        except BorderException:
            print("border--")
            # TODO: Write how to handle border collision

            self.replan_trip()

        except ObstacleException:
            print("obstacle--")
            # TODO: Write how to handle obstacle collision
            if self.check_3by3_area(self.get_grid_pos_straight("FORWARD", 3)):
                if self.check_3by3_area(self.get_grid_pos_turn("FORWARD_L")):
                    self.robot.move_forward_steer_left()
                elif self.check_3by3_area(self.get_grid_pos_turn("FORWARD_R")):
                    self.robot.move_forward_steer_right()
                elif self.check_3by3_area(self.get_grid_pos_straight("BACKWARD", 1)):
                    self.move_forward_by(1)
                else:
                    print("Nothing done for obstacle avoidance")
            else:
                if self.check_3by3_area(self.get_grid_pos_straight("BACKWARD", 3)):
                    self.move_backward_by(3)
                elif self.check_3by3_area(self.get_grid_pos_straight("BACKWARD", 2)):
                    self.move_backward_by(2)
                elif self.check_3by3_area(self.get_grid_pos_straight("BACKWARD", 1)):
                    self.move_backward_by(1)
                else:
                    print("Nothing done for obstacle avoidance")

            self.replan_trip()

        except ObstacleTurnException:
            print("obstacle-turn--")
            # TODO: Write how to handle "unable to turn due to obstacle" collisions

            self.replan_trip()

    # c is how many grids in front you want to check (use 3 for turns)
    def get_grid_pos_straight(self, movement, c):
        grid_x, grid_y, initial_angle = self.robot.grid_x, self.robot.grid_y, self.robot.angle
        if initial_angle == constants.NORTH:
            if movement == "FORWARD_R" or movement == "FORWARD_L" or movement == "FORWARD":
                grid_x, grid_y = grid_x, grid_y + c
            elif movement == "BACKWARD_R" or movement == "BACKWARD_L" or movement == "BACKWARD":
                grid_x, grid_y = grid_x, grid_y - c
        elif initial_angle == constants.SOUTH:
            if movement == "FORWARD_R" or movement == "FORWARD_L" or movement == "FORWARD":
                grid_x, grid_y = grid_x, grid_y - c
            elif movement == "BACKWARD_R" or movement == "BACKWARD_L" or movement == "BACKWARD":
                grid_x, grid_y = grid_x, grid_y + c
        elif initial_angle == constants.EAST:
            if movement == "FORWARD_R" or movement == "FORWARD_L" or movement == "FORWARD":
                grid_x, grid_y = grid_x + c, grid_y
            elif movement == "BACKWARD_R" or movement == "BACKWARD_L" or movement == "BACKWARD":
                grid_x, grid_y = grid_x - c, grid_y
        elif initial_angle == constants.WEST:
            if movement == "FORWARD_R" or movement == "FORWARD_L" or movement == "FORWARD":
                grid_x, grid_y = grid_x - c, grid_y
            elif movement == "BACKWARD_R" or movement == "BACKWARD_L" or movement == "BACKWARD":
                grid_x, grid_y = grid_x + c, grid_y
        return [grid_x, grid_y]

    # for checking the diagonal 3x3 grid
    def get_grid_pos_turn(self, movement):
        grid_x, grid_y, initial_angle = self.robot.grid_x, self.robot.grid_y, self.robot.angle
        if initial_angle == constants.NORTH:
            if movement == "FORWARD_R":
                grid_x, grid_y = grid_x + 3, grid_y + 3
            elif movement == "FORWARD_L":
                grid_x, grid_y = grid_x - 3, grid_y + 3
            elif movement == "BACKWARD_R":
                grid_x, grid_y = grid_x + 3, grid_y - 3
            elif movement == "BACKWARD_L":
                grid_x, grid_y = grid_x - 3, grid_y - 3
        elif initial_angle == constants.SOUTH:
            if movement == "FORWARD_R":
                grid_x, grid_y = grid_x - 3, grid_y - 3
            elif movement == "FORWARD_L":
                grid_x, grid_y = grid_x + 3, grid_y - 3
            elif movement == "BACKWARD_R":
                grid_x, grid_y = grid_x - 3, grid_y + 3
            elif movement == "BACKWARD_L":
                grid_x, grid_y = grid_x + 3, grid_y + 3
        elif initial_angle == constants.EAST:
            if movement == "FORWARD_R":
                grid_x, grid_y = grid_x + 3, grid_y - 3
            elif movement == "FORWARD_L":
                grid_x, grid_y = grid_x + 3, grid_y + 3
            elif movement == "BACKWARD_R":
                grid_x, grid_y = grid_x - 3, grid_y - 3
            elif movement == "BACKWARD_L":
                grid_x, grid_y = grid_x - 3, grid_y + 3
        elif initial_angle == constants.WEST:
            if movement == "FORWARD_R":
                grid_x, grid_y = grid_x - 3, grid_y + 3
            elif movement == "FORWARD_L":
                grid_x, grid_y = grid_x - 3, grid_y - 3
            elif movement == "BACKWARD_R":
                grid_x, grid_y = grid_x + 3, grid_y + 3
            elif movement == "BACKWARD_L":
                grid_x, grid_y = grid_x + 3, grid_y - 3
        return [grid_x, grid_y]

    def check_3by3_area(self, grid_pos):
        pos = self.grid.grid_to_pixel(grid_pos)
        for obstacle_id in self.grid.get_obstacle_cells():
            obstacle_grid_coord = obstacle_id.split("-")
            obstacle_grid_x, obstacle_grid_y = int(obstacle_grid_coord[0]), int(obstacle_grid_coord[1])
            obstacle_grid_coord = [obstacle_grid_x, obstacle_grid_y]

            # Using pixel position
            obstacle_pixel_x, obstacle_pixel_y = self.grid.grid_to_pixel(obstacle_grid_coord)[0], \
                                                 self.grid.grid_to_pixel(obstacle_grid_coord)[1]
            border_pixel_length = (self.grid.block_size + MARGIN) * 3  # about 3 squares border
            if (obstacle_pixel_x - border_pixel_length < pos[0] < obstacle_pixel_x + border_pixel_length) \
                    and (obstacle_pixel_y - border_pixel_length < pos[1] < obstacle_pixel_y + border_pixel_length):
                return False
        return True

    def replan_trip(self):
        a, b, x, y = self.target_x, self.target_y, self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1]
        robot_direction, target_direction = self.target_direction, self.robot.get_angle_of_rotation()
        self.plan_trip_by_robot_target_directions(a, b, x, y, robot_direction, target_direction)

    def preprocess_coords(self, a, b, x, y):
        a, b = self.undo_target_transpose(a, b, self.target_direction)
        a, b, x, y = self.transpose_orientation(a, b, self.target_direction,
                                                self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1])
        return a, b, x, y

    def AR1(self, a, b, x, y):
        if abs(b-y) <= 2:
            self.move_backward_by(abs(b - y))
            if a - x < 0:
                a, b, x, y = self.preprocess_coords(a, b, x, y)
                self.AR2(a, b, x, y)
            elif a - x > 0:
                a, b, x, y = self.preprocess_coords(a, b, x, y)
                self.AR4(a, b, x, y)
        else:
            if a - x <= 0:
                self.robot.move_forward_steer_left()
                self.move_forward_by(abs(a - x))
                self.robot.move_forward_steer_left()
                self.move_forward_by(abs(b - y))
                self.robot.move_forward_steer_left()
                self.robot.move_forward_steer_left()

            else:
                self.robot.move_forward_steer_right()
                self.move_forward_by(abs(a - x))
                self.robot.move_forward_steer_right()
                self.move_forward_by(abs(b - y))
                self.robot.move_forward_steer_right()
                self.robot.move_forward_steer_right()

    def AR2(self, a, b, x, y):
        a, b, x, y = self.preprocess_coords(a, b, x, y)
        self.AR6(a, b, x, y)

    def AR3(self, a, b, x, y):
        # Forward by abs(b-y)
        self.move_forward_by(abs(b - y))

    def AR4(self, a, b, x, y):
        a, b, x, y = self.preprocess_coords(a, b, x, y)
        self.AR7(a, b, x, y)

    def AR5(self, a, b, x, y):
        self.move_backward_by(abs(b - y))
        a, b, x, y = self.preprocess_coords(a, b, x, y)
        self.AR6(a, b, x, y)

    def AR6(self, a, b, x, y):
        if abs(b - y) < 2:
            self.move_backward_by(2 - abs(b - y))
        else:
            self.move_forward_by(abs(b - y) - 2)
        self.robot.move_forward_steer_left()
        self.move_forward_by(abs(a - x))
        self.robot.move_backward_steer_left()
        self.move_forward_by(2)

    def AR7(self, a, b, x, y):
        if abs(b - y) < 2:
            self.move_backward_by(2 - abs(b - y))
        else:
            self.move_forward_by(abs(b - y) - 2)
        self.robot.move_forward_steer_right()
        self.move_forward_by(abs(a - x))
        self.robot.move_backward_steer_right()
        self.move_forward_by(2)

    def AR8(self, a, b, x, y):
        self.move_backward_by(abs(b - y))
        a, b, x, y = self.preprocess_coords(a, b, x, y)
        self.AR7(a, b, x, y)

    def BR1(self, a, b, x, y):
        if abs(b - y) <= 2:
            self.move_forward_by(abs(b - y))
            a, b, x, y = self.preprocess_coords(a, b, x, y)
            self.BR9(a, b, x, y)
        else:
            if abs(b - y) < 10:
                self.move_backward_by(10 - abs(b - y))
            else:
                self.move_forward_by(abs(b - y) - 10)
            self.robot.move_forward_steer_right()
            self.move_backward_by(3)
            self.robot.move_forward_steer_left()
            self.robot.move_forward_steer_left()
            self.move_forward_by(3)
            self.robot.move_backward_steer_right()
            self.move_forward_by(2)

    def BR2(self, a, b, x, y):
        if abs(a - x) <= 2:
            self.robot.move_forward_steer_right()
            self.move_backward_by(6 - abs(a - x))
            self.robot.move_forward_steer_right()
        else:
            self.move_backward_by(3)
            self.robot.move_forward_steer_right()
            self.move_forward_by(abs(a - x))
            self.robot.move_backward_steer_left()
            self.move_forward_by(3)

    def BR3(self, a, b, x, y):
        self.move_backward_by(abs(b - y))
        a, b, x, y = self.preprocess_coords(a, b, x, y)
        self.BR9(a, b, x, y)

    def BR4(self, a, b, x, y):
        if abs(a - x) <= 2:
            self.robot.move_forward_steer_left()
            self.move_backward_by(6 - abs(a - x))
            self.robot.move_forward_steer_left()
        else:
            self.move_backward_by(3)
            self.robot.move_forward_steer_left()
            self.move_forward_by(abs(a - x))
            self.robot.move_backward_steer_right()
            self.move_forward_by(3)

    def BR5(self, a, b, x, y):
        if abs(a - x) <= 2:
            if abs(b - y) <= 2:
                self.move_forward_by(abs(b - y))
                self.robot.move_forward_steer_right()
                self.move_backward_by(6 - abs(a - x))
                self.robot.move_forward_steer_right()
            else:
                self.robot.move_backward_steer_right()
                a, b, x, y = self.preprocess_coords(a, b, x, y)
                self.DR8(a, b, x, y)

        else:
            if abs(b - y) - 3 >= 0:
                self.move_forward_by(abs(b - y) - 3)
            else:
                self.move_backward_by(3 - abs(b - y))
            self.robot.move_forward_steer_right()
            self.move_forward_by(abs(a - x))
            self.robot.move_backward_steer_left()
            self.move_forward_by(3)

    def BR6(self, a, b, x, y):
        self.move_backward_by(abs(b - y))
        if abs(a - x) > 0:
            self.robot.move_forward_steer_right()
            self.move_forward_by(abs(a - x))
            self.robot.move_backward_steer_left()
            self.move_forward_by(6)
        else:
            a, b, x, y = self.preprocess_coords(a, b, x, y)
            self.BR2(a, b, x, y)

    def BR7(self, a, b, x, y):
        self.move_backward_by(abs(b - y))
        if abs(a) - abs(x) < 0:
            self.robot.move_forward_steer_left()
            self.move_forward_by(abs(a - x))
            self.robot.move_backward_steer_right()
            self.move_forward_by(6)
        else:
            a, b, x, y = self.preprocess_coords(a, b, x, y)
            self.BR4(a, b, x, y)

    def BR8(self, a, b, x, y):
        if abs(a - x) <= 2:
            if abs(b - y) <= 2:
                self.move_forward_by(abs(b - y))
                self.robot.move_forward_steer_left()
                self.move_backward_by(6 - abs(a - x))
                self.robot.move_forward_steer_left()
            else:
                self.robot.move_backward_steer_left()
                a, b, x, y = self.preprocess_coords(a, b, x, y)
                self.CR5(a, b, x, y)

        else:
            if abs(b - y) >= 3:
                self.move_forward_by(abs(b - y) - 3)
            else:
                self.move_backward_by(3 - abs(b - y))
            self.robot.move_forward_steer_left()
            self.move_forward_by(abs(a - x))
            self.robot.move_backward_steer_right()
            self.move_forward_by(3)

    def BR9(self, a, b, x, y):
        self.robot.move_forward_steer_right()
        self.move_backward_by(6)
        self.robot.move_forward_steer_right()

    def CR1(self, a, b, x, y):
        # Backward Left
        self.robot.move_backward_steer_left()
        a, b, x, y = self.preprocess_coords(a, b, x, y)
        self.AR5(a, b, x, y)

    def CR2(self, a, b, x, y):
        self.move_forward_by(abs(a-x) + 3)
        a, b, x, y = self.preprocess_coords(a, b, x, y)
        self.CR4(a, b, x, y)
        pass

    def CR3(self, a, b, x, y):
        a, b, x, y = self.preprocess_coords(a, b, x, y)
        self.CR6(a, b, x, y)
        pass

    def CR4(self, a, b, x, y):
        if abs(a - x) <= 2:
            self.move_forward_by(3 - abs(a - x))
        else:
            self.move_backward_by(abs(x - a) - 3)
        # Backward Left
        self.robot.move_backward_steer_left()
        self.move_forward_by(abs(b - y)+3)

    def CR5(self, a, b, x, y):
        # Backward Left
        self.robot.move_backward_steer_left()
        if abs(y - b) > 3:
            a, b, x, y = self.preprocess_coords(a, b, x, y)
            self.AR5(a, b, x, y)
        elif abs(y - b) == 3:
            a, b, x, y = self.preprocess_coords(a, b, x, y)
            self.AR2(a, b, x, y)
        else:
            a, b, x, y = self.preprocess_coords(a, b, x, y)
            self.AR6(a, b, x, y)
        pass

    def CR6(self, a, b, x, y):
        self.move_forward_by(abs(a - x) + 3)
        a, b, x, y = self.preprocess_coords(a, b, x, y)
        self.CR7(a, b, x, y)

    def CR7(self, a, b, x, y):
        self.move_backward_by(abs(x - a) - 3)
        self.robot.move_backward_steer_left()
        self.move_forward_by(abs(b - y) + 3)

    def CR8(self, a, b, x, y):
        if abs(x - a) <= 5:
            self.move_forward_by(6 - abs(x - a))
        self.robot.move_backward_steer_left()
        if abs(y - b) > 3:
            a, b, x, y = self.preprocess_coords(a, b, x, y)
            self.AR8(a, b, x, y)
        elif abs(y - b) == 3:
            a, b, x, y = self.preprocess_coords(a, b, x, y)
            self.AR4(a, b, x, y)
        else:
            a, b, x, y = self.preprocess_coords(a, b, x, y)
            self.AR7(a, b, x, y)

    def CR9(self, a, b, x, y):
        self.move_forward_by(3)
        self.robot.move_backward_steer_left()
        self.move_forward_by(3)

    def DR1(self, a, b, x, y):
        self.robot.move_backward_steer_right()
        a, b, x, y = self.preprocess_coords(a, b, x, y)
        self.AR8(a, b, x, y)

    def DR2(self, a, b, x, y):
        if abs(a - x) <= 2:
            self.move_forward_by(3 - abs(a - x))
        else:
            self.move_backward_by(abs(a - x) - 3)
        # Backward Right
        self.robot.move_backward_steer_right()
        self.move_forward_by(abs(b - y) + 3)

    def DR3(self, a, b, x, y):
        a, b, x, y = self.preprocess_coords(a, b, x, y)
        self.DR7(a, b, x, y)

    def DR4(self, a, b, x, y):
        self.move_forward_by(abs(b - y) + 3)
        a, b, x, y = self.preprocess_coords(a, b, x, y)
        self.DR7(a, b, x, y)

    def DR5(self, a, b, x, y):
        if abs(x - a) <= 5:
            self.move_forward_by(6 - abs(a - x))
        self.robot.move_backward_steer_right()
        if abs(y - b) > 3:
            a, b, x, y = self.preprocess_coords(a, b, x, y)
            self.AR5(a, b, x, y)
        elif abs(y - b) == 3:
            a, b, x, y = self.preprocess_coords(a, b, x, y)
            self.AR2(a, b, x, y)
        else:
            a, b, x, y = self.preprocess_coords(a, b, x, y)
            self.AR6(a, b, x, y)

    def DR6(self, a, b, x, y):
        if abs(a - x) <= 2:
            self.move_forward_by(3 - abs(a - x))
        else:
            self.move_backward_by(abs(a - x) - 3)
        self.robot.move_backward_steer_right()
        self.move_forward_by(abs(b - y) + 3)

    def DR7(self, a, b, x, y):
        self.move_forward_by(abs(a - x) + 3)
        a, b, x, y = self.preprocess_coords(a, b, x, y)
        self.DR6(a, b, x, y)

    def DR8(self, a, b, x, y):
        # Backward Right
        self.robot.move_backward_steer_right()
        if abs(y - b) > 3:
            a, b, x, y = self.preprocess_coords(a, b, x, y)
            self.AR8(a, b, x, y)
        elif abs(y - b) == 3:
            a, b, x, y = self.preprocess_coords(a, b, x, y)
            self.AR4(a, b, x, y)
        else:
            a, b, x, y = self.preprocess_coords(a, b, x, y)
            self.AR7(a, b, x, y)
        pass

    def DR9(self, a, b, x, y):
        self.move_forward_by(3)
        self.robot.move_backward_steer_right()
        self.move_forward_by(3)

    def move_forward_by(self, no_of_steps):
        for i in range(int(no_of_steps)):
            self.robot.move_forward()

    def move_backward_by(self, no_of_steps):
        for i in range(int(no_of_steps)):
            self.robot.move_backward()

    def check_reached_target(self, target_a, target_b):
        x, y = self.robot.get_grid_pos()[0], self.robot.get_grid_pos()[1]
        if target_a == x and target_b == y:
            # Move car 2 steps backwards for next move
            # time.sleep(constants.NEXT_OBSTACLE_TIME_DELAY)
            #self.move_backward_by(1)
            # time.sleep(constants.NEXT_OBSTACLE_TIME_DELAY)
            pass
