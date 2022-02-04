import time
from math import degrees
from pygame.math import Vector2
import constants
import pygame

# This sets the margin between each Cell
MARGIN = 2
ONE_CELL = 20 + MARGIN
THREE_CELL = 3 * ONE_CELL
dt = 0.4


# dt = round(self.clock.get_time() / 1000, 2)

class BorderException(Exception):
    pass


class ObstacleException(Exception):
    pass


class ObstacleTurnException(Exception):
    pass


class Robot(object):

    def __init__(self, simulator, screen, grid, grid_surface, robot_w, robot_h, grid_x, grid_y, angle, car_image):
        self.robot_w = robot_w
        self.robot_h = robot_h
        # actual pixel width and height of robot (inclusive of margin)
        self.screen_width = grid.get_block_size() * robot_w / 10 + (robot_w / 10 * MARGIN) + MARGIN
        self.screen_height = grid.get_block_size() * robot_h / 10 + (robot_h / 10 * MARGIN) + MARGIN
        # NOTE: grid_x and grid_y are the grid coordinates of the middle square of the 3x3 car area
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.simulator = simulator
        self.screen = screen
        self.grid = grid
        self.grid_surface = grid_surface
        # the position of the middle of the car with respect to the grid
        self.pixel_pos = Vector2(self.grid.grid_to_pixel([self.grid_x, self.grid_y])[0],
                                 self.grid.grid_to_pixel([self.grid_x, self.grid_y])[1])
        # self.pixel_pos = Vector2(grid.grid_to_pixel([1,1])[0],grid.grid_to_pixel([1,1])[1])
        self.angle = angle
        self.car_image = car_image
        self.car_rect = pygame.Rect(self.pixel_pos[0] - (0.5 * self.screen_width),
                                    self.pixel_pos[1] - (0.5 * self.screen_height),
                                    self.screen_width, self.screen_height)

        # TODO update the car speed
        self.speed = 10
        self.velocity = Vector2(0.0, 0.0)
        self.steering = 0.0

    def get_pixel_pos(self):
        return self.pixel_pos

    def get_grid_pos(self):
        return (self.grid_x, self.grid_y)

    def get_angle_of_rotation(self):
        return self.angle

    def draw_car(self):
        rotated = pygame.transform.rotate(self.car_image, self.angle)
        rect = rotated.get_rect()
        rect.center = self.car_rect.center
        self.screen.blit(rotated, rect)
        # screen.blit(rotated, self.get_pixel_pos() - (rect.width / 2, rect.height / 2))
        pygame.draw.rect(self.screen, constants.RED, self.car_rect, 1)

        # Refresh screen by frame rate
        now = pygame.time.get_ticks() / 1000
        if now - self.simulator.startTime > 1 / constants.FPS:
            self.simulator.startTime = now
            self.simulator.root.display.flip()

    def redraw_car(self):
        # Need to redraw over everything (grid_surface, grid and car)
        self.simulator.reprint_screen_and_buttons()
        self.screen.blit(self.grid_surface, (120, 120))
        self.grid.update_grid(self.screen)
        self.draw_car()

    def check_movement_complete(self, final_pixel_pos):
        return abs(self.get_pixel_pos()[0] - final_pixel_pos[0]) > 2 or abs(
            self.get_pixel_pos()[1] - final_pixel_pos[1]) > 2

    # TODO: define possible movements (for turning motions picture steering wheel direction)
    # ALL MOTIONS take place in minimal unit.
    # for 1: is by 10 (one grid)
    # for 2-5: is 30 by 30 (3x3 grid) area plus rotation
    # 1. straight (one grid) - forward, backwards
    # 2. forward right/clockwise pi/2 turn
    # 3. forward left/anticlockwise pi/2 turn
    # 4. backward right/anticlockwise pi/2 turn
    # 5. backward left/clockwise pi/2 turn
    def move_forward(self):
        print("MOVE FORWARD FACING", self.angle)
        initial_pixel_pos = self.get_pixel_pos()
        # Set position to stop moving
        if self.angle == constants.NORTH:  # CAR FACING NORTH
            final_pixel_pos = Vector2(initial_pixel_pos[0], initial_pixel_pos[1] - ONE_CELL)
        elif self.angle == constants.SOUTH:  # CAR FACING SOUTH
            final_pixel_pos = Vector2(initial_pixel_pos[0], initial_pixel_pos[1] + ONE_CELL)
        elif self.angle == constants.EAST:  # CAR FACING EAST
            final_pixel_pos = Vector2(initial_pixel_pos[0] + ONE_CELL, initial_pixel_pos[1])
        elif self.angle == constants.WEST:  # CAR FACING WEST
            final_pixel_pos = Vector2(initial_pixel_pos[0] - ONE_CELL, initial_pixel_pos[1])
        else:
            final_pixel_pos = initial_pixel_pos  # car will not move
        final_angle = self.angle

        if self.check_within_border(final_pixel_pos) and self.check_exclude_obstacles_straight(final_pixel_pos):
            # Set velocity of car
            self.velocity += (0, -self.speed)
            while self.check_movement_complete(final_pixel_pos):
                self.pixel_pos += self.velocity.rotate(-self.angle) * dt
                self.car_rect = pygame.Rect(self.pixel_pos[0] - (0.5 * self.screen_width),
                                            self.pixel_pos[1] - (0.5 * self.screen_height),
                                            self.screen_width, self.screen_height)
                self.redraw_car()

            # Reset velocity to 0
            self.velocity -= (0, -self.speed)
            self.correct_coords_and_angle(final_angle, final_pixel_pos)
            self.redraw_car()

            self.check_if_target_reached(final_pixel_pos, final_angle)
            return True
        else:
            return False

    def move_backward(self):
        print("MOVE BACKWARD FACING", self.angle)
        initial_pixel_pos = self.get_pixel_pos()
        # Set position to stop moving
        if self.angle == constants.NORTH:  # CAR FACING NORTH
            final_pixel_pos = Vector2(initial_pixel_pos[0], initial_pixel_pos[1] + ONE_CELL)
        elif self.angle == constants.SOUTH:  # CAR FACING SOUTH
            final_pixel_pos = Vector2(initial_pixel_pos[0], initial_pixel_pos[1] - ONE_CELL)
        elif self.angle == constants.EAST:  # CAR FACING EAST
            final_pixel_pos = Vector2(initial_pixel_pos[0] - ONE_CELL, initial_pixel_pos[1])
        elif self.angle == constants.WEST:  # CAR FACING WEST
            final_pixel_pos = Vector2(initial_pixel_pos[0] + ONE_CELL, initial_pixel_pos[1])
        else:
            final_pixel_pos = initial_pixel_pos  # car will not move
        final_angle = self.angle

        if self.check_within_border(final_pixel_pos) and self.check_exclude_obstacles_straight(final_pixel_pos):
            # Set velocity of car
            self.velocity += (0, self.speed)
            while self.check_movement_complete(final_pixel_pos):
                self.pixel_pos += self.velocity.rotate(-self.angle) * dt
                self.car_rect = pygame.Rect(self.pixel_pos[0] - (0.5 * self.screen_width),
                                            self.pixel_pos[1] - (0.5 * self.screen_height),
                                            self.screen_width, self.screen_height)
                self.redraw_car()
            # Reset velocity to 0
            self.velocity -= (0, self.speed)
            self.correct_coords_and_angle(final_angle, final_pixel_pos)
            self.redraw_car()

            self.check_if_target_reached(final_pixel_pos, final_angle)
            return True
        else:
            return False

    def move_forward_steer_right(self):
        print("STEERING RIGHT FORWARD FACING", self.angle)
        # Pause to simulate time taken for wheels to full rotate
        # time.sleep(constants.STEERING_TIME_DELAY)

        initial_pixel_pos = self.get_pixel_pos()
        initial_angle = self.angle
        # Set position to stop moving
        if self.angle == constants.NORTH:  # CAR FACING NORTH
            final_pixel_pos = Vector2(initial_pixel_pos[0] + THREE_CELL, initial_pixel_pos[1] - THREE_CELL)
            final_angle = constants.EAST
        elif self.angle == constants.SOUTH:  # CAR FACING SOUTH
            final_pixel_pos = Vector2(initial_pixel_pos[0] - THREE_CELL, initial_pixel_pos[1] + THREE_CELL)
            final_angle = constants.WEST
        elif self.angle == constants.EAST:  # CAR FACING EAST
            final_pixel_pos = Vector2(initial_pixel_pos[0] + THREE_CELL, initial_pixel_pos[1] + THREE_CELL)
            final_angle = constants.SOUTH
        elif self.angle == constants.WEST:  # CAR FACING WEST
            final_pixel_pos = Vector2(initial_pixel_pos[0] - THREE_CELL, initial_pixel_pos[1] - THREE_CELL)
            final_angle = constants.NORTH
        else:
            final_pixel_pos = initial_pixel_pos  # car will not move
            final_angle = initial_angle

        if self.check_within_border(final_pixel_pos) and self.check_exclude_obstacles(final_pixel_pos, "FORWARD_R"):
            # Pause to simulate time taken for wheels to full rotate
            # time.sleep(constants.STEERING_TIME_DELAY)

            # Set velocity of car
            self.velocity += (0, -self.speed)
            while not self.check_if_reached(initial_angle, final_pixel_pos):
                turning_radius = THREE_CELL
                angular_velocity = self.velocity.y / turning_radius

                self.pixel_pos += self.velocity.rotate(-self.angle) * dt
                self.angle += degrees(angular_velocity) * dt

                self.car_rect = pygame.Rect(self.pixel_pos[0] - (0.5 * self.screen_width),
                                            self.pixel_pos[1] - (0.5 * self.screen_height),
                                            self.screen_width, self.screen_height)
                self.redraw_car()

            # Reset velocity to 0 and do corrections for angle and coordinates
            self.velocity -= (0, -self.speed)
            self.correct_coords_and_angle(final_angle, final_pixel_pos)
            self.redraw_car()

            self.check_if_target_reached(final_pixel_pos, final_angle)
            return True
        else:
            return False

    def move_forward_steer_left(self):
        print("STEERING LEFT FORWARD FACING", self.angle)
        # Pause to simulate time taken for wheels to full rotate
        # time.sleep(constants.STEERING_TIME_DELAY)

        initial_pixel_pos = self.get_pixel_pos()
        initial_angle = self.angle
        # Set position to stop moving
        if self.angle == constants.NORTH:  # CAR FACING NORTH
            final_pixel_pos = Vector2(initial_pixel_pos[0] - THREE_CELL, initial_pixel_pos[1] - THREE_CELL)
            final_angle = constants.WEST
        elif self.angle == constants.SOUTH:  # CAR FACING SOUTH
            final_pixel_pos = Vector2(initial_pixel_pos[0] + THREE_CELL, initial_pixel_pos[1] + THREE_CELL)
            final_angle = constants.EAST
        elif self.angle == constants.EAST:  # CAR FACING EAST
            final_pixel_pos = Vector2(initial_pixel_pos[0] + THREE_CELL, initial_pixel_pos[1] - THREE_CELL)
            final_angle = constants.NORTH
        elif self.angle == constants.WEST:  # CAR FACING WEST
            final_pixel_pos = Vector2(initial_pixel_pos[0] - THREE_CELL, initial_pixel_pos[1] + THREE_CELL)
            final_angle = constants.SOUTH
        else:
            final_pixel_pos = initial_pixel_pos  # car will not move
            final_angle = initial_angle

        if self.check_within_border(final_pixel_pos) and self.check_exclude_obstacles(final_pixel_pos, "FORWARD_L"):
            # Pause to simulate time taken for wheels to full rotate
            # time.sleep(constants.STEERING_TIME_DELAY)

            # Set velocity of car
            self.velocity += (0, -self.speed)
            while not self.check_if_reached(initial_angle, final_pixel_pos):
                turning_radius = THREE_CELL
                angular_velocity = self.velocity.y / turning_radius

                self.pixel_pos += self.velocity.rotate(-self.angle) * dt
                self.angle -= degrees(angular_velocity) * dt

                self.car_rect = pygame.Rect(self.pixel_pos[0] - (0.5 * self.screen_width),
                                            self.pixel_pos[1] - (0.5 * self.screen_height),
                                            self.screen_width, self.screen_height)
                self.redraw_car()

            # Reset velocity to 0 and do corrections for angle and coordinates
            self.velocity -= (0, -self.speed)
            self.correct_coords_and_angle(final_angle, final_pixel_pos)
            self.redraw_car()

            self.check_if_target_reached(final_pixel_pos, final_angle)
            return True
        else:
            return False

    def move_backward_steer_right(self):
        print("STEERING RIGHT BACKWARD FACING", self.angle)
        # Pause to simulate time taken for wheels to full rotate
        # time.sleep(constants.STEERING_TIME_DELAY)

        initial_pixel_pos = self.get_pixel_pos()
        initial_angle = self.angle
        # Set position to stop moving
        if self.angle == constants.NORTH:  # CAR FACING NORTH
            final_pixel_pos = Vector2(initial_pixel_pos[0] + THREE_CELL, initial_pixel_pos[1] + THREE_CELL)
            final_angle = constants.WEST
        elif self.angle == constants.SOUTH:  # CAR FACING SOUTH
            final_pixel_pos = Vector2(initial_pixel_pos[0] - THREE_CELL, initial_pixel_pos[1] - THREE_CELL)
            final_angle = constants.EAST
        elif self.angle == constants.EAST:  # CAR FACING EAST
            final_pixel_pos = Vector2(initial_pixel_pos[0] - THREE_CELL, initial_pixel_pos[1] + THREE_CELL)
            final_angle = constants.NORTH
        elif self.angle == constants.WEST:  # CAR FACING WEST
            final_pixel_pos = Vector2(initial_pixel_pos[0] + THREE_CELL, initial_pixel_pos[1] - THREE_CELL)
            final_angle = constants.SOUTH
        else:
            final_pixel_pos = initial_pixel_pos  # car will not move
            final_angle = initial_angle

        if self.check_within_border(final_pixel_pos) and self.check_exclude_obstacles(final_pixel_pos, "BACKWARD_R"):
            # Pause to simulate time taken for wheels to full rotate
            # time.sleep(constants.STEERING_TIME_DELAY)

            # Set velocity of car
            self.velocity += (0, -self.speed)
            while not self.check_if_reached(initial_angle, final_pixel_pos):
                turning_radius = THREE_CELL
                angular_velocity = self.velocity.y / turning_radius

                self.pixel_pos -= self.velocity.rotate(-self.angle) * dt
                self.angle -= degrees(angular_velocity) * dt

                self.car_rect = pygame.Rect(self.pixel_pos[0] - (0.5 * self.screen_width),
                                            self.pixel_pos[1] - (0.5 * self.screen_height),
                                            self.screen_width, self.screen_height)
                self.redraw_car()

            # Reset velocity to 0 and do corrections for angle and coordinates
            self.velocity -= (0, -self.speed)
            self.correct_coords_and_angle(final_angle, final_pixel_pos)
            self.redraw_car()

            self.check_if_target_reached(final_pixel_pos, final_angle)
            return True
        else:
            return False

    def move_backward_steer_left(self):
        print("STEERING LEFT BACKWARD FACING", self.angle)

        initial_pixel_pos = self.get_pixel_pos()
        initial_angle = self.angle
        # Set position to stop moving
        if self.angle == constants.NORTH:  # CAR FACING NORTH
            final_pixel_pos = Vector2(initial_pixel_pos[0] - THREE_CELL, initial_pixel_pos[1] + THREE_CELL)
            final_angle = constants.EAST
        elif self.angle == constants.SOUTH:  # CAR FACING SOUTH
            final_pixel_pos = Vector2(initial_pixel_pos[0] + THREE_CELL, initial_pixel_pos[1] - THREE_CELL)
            final_angle = constants.WEST
        elif self.angle == constants.EAST:  # CAR FACING EAST
            final_pixel_pos = Vector2(initial_pixel_pos[0] - THREE_CELL, initial_pixel_pos[1] - THREE_CELL)
            final_angle = constants.SOUTH
        elif self.angle == constants.WEST:  # CAR FACING WEST
            final_pixel_pos = Vector2(initial_pixel_pos[0] + THREE_CELL, initial_pixel_pos[1] + THREE_CELL)
            final_angle = constants.NORTH
        else:
            final_pixel_pos = initial_pixel_pos  # car will not move
            final_angle = initial_angle

        if self.check_within_border(final_pixel_pos) and self.check_exclude_obstacles(final_pixel_pos, "BACKWARD_L"):
            # Pause to simulate time taken for wheels to full rotate
            # time.sleep(constants.STEERING_TIME_DELAY)

            # Set velocity of car
            self.velocity += (0, -self.speed)
            while not self.check_if_reached(initial_angle, final_pixel_pos):
                turning_radius = THREE_CELL
                angular_velocity = self.velocity.y / turning_radius

                self.pixel_pos -= self.velocity.rotate(-self.angle) * dt
                self.angle += degrees(angular_velocity) * dt

                self.car_rect = pygame.Rect(self.pixel_pos[0] - (0.5 * self.screen_width),
                                            self.pixel_pos[1] - (0.5 * self.screen_height),
                                            self.screen_width, self.screen_height)
                self.redraw_car()

            # Reset velocity to 0 and do corrections for angle and coordinates
            self.velocity -= (0, -self.speed)
            self.correct_coords_and_angle(final_angle, final_pixel_pos)
            self.redraw_car()

            self.check_if_target_reached(final_pixel_pos, final_angle)
            return True
        else:
            return False

    def correct_coords_and_angle(self, final_angle, final_pixel_pos):
        self.angle = final_angle
        self.pixel_pos = final_pixel_pos
        self.grid_x = self.grid.pixel_to_grid(final_pixel_pos)[0]
        self.grid_y = self.grid.pixel_to_grid(final_pixel_pos)[1]
        self.car_rect = pygame.Rect(self.pixel_pos[0] - (0.5 * self.screen_width),
                                    self.pixel_pos[1] - (0.5 * self.screen_height),
                                    self.screen_width, self.screen_height)

    def check_if_reached(self, initial_angle, final_pixel_pos):
        # Set position to stop moving
        if self.check_movement_complete(final_pixel_pos) \
                and abs(self.angle - initial_angle) > 85:
            return True
        else:
            return False

    # TODO: it is possible for robot to move outside of border for now (to meet some of the limitations of path planning
    def check_within_border(self, pos):
        if (constants.min_pixel_pos_x + self.robot_w < pos[0] < constants.max_pixel_pos_x - self.robot_w) \
                and (constants.min_pixel_pos_y + self.robot_h < pos[1] < constants.max_pixel_pos_y - self.robot_h):
            return True
        #raise BorderException("BORDER")
        return True
        # return False

    # TODO: for now, it is strictly right in front of the image, 4 grids away (counting from the centre of car)
    def check_if_target_reached(self, final_pixel_pos, final_angle):
        target_locations = self.grid.get_target_locations()
        for target_loc in target_locations:
            target_grid_x = target_loc[0]
            target_grid_y = target_loc[1]
            target_direction = target_loc[2]
            obstacle_cell = target_loc[3]

            final_grid_pos = self.grid.pixel_to_grid(final_pixel_pos)
            final_grid_x = final_grid_pos[0]
            final_grid_y = final_grid_pos[1]
            # print("Checking for obstacles visited:", target_loc)

            # Check if in target grid
            if (final_grid_x == target_grid_x) and (final_grid_y == target_grid_y) and (
                    final_angle == target_direction):
                self.grid.set_obstacle_as_visited(obstacle_cell)

                # Repaint grid and car
                self.redraw_car()
                print("--Obstacle was visited!")

    # def get_cells_occupied_by_car(self):
    #     cells = [self.grid.get_cell_by_xycoords(self.grid_x - 1, self.grid_y - 1),
    #              self.grid.get_cell_by_xycoords(self.grid_x - 1, self.grid_y),
    #              self.grid.get_cell_by_xycoords(self.grid_x - 1, self.grid_y + 1),
    #              self.grid.get_cell_by_xycoords(self.grid_x, self.grid_y - 1),
    #              self.grid.get_cell_by_xycoords(self.grid_x, self.grid_y),
    #              self.grid.get_cell_by_xycoords(self.grid_x, self.grid_y + 1),
    #              self.grid.get_cell_by_xycoords(self.grid_x - 1, self.grid_y - 1),
    #              self.grid.get_cell_by_xycoords(self.grid_x - 1, self.grid_y),
    #              self.grid.get_cell_by_xycoords(self.grid_x - 1, self.grid_y) + 1]
    #     return cells

    def check_exclude_obstacles_straight(self, final_pixel_pos):
        for obstacle_id in self.grid.get_obstacle_cells():
            obstacle_grid_coord = obstacle_id.split("-")
            obstacle_grid_x, obstacle_grid_y = int(obstacle_grid_coord[0]), int(obstacle_grid_coord[1])
            obstacle_grid_coord = [obstacle_grid_x, obstacle_grid_y]

            # Using pixel position
            obstacle_pixel_x, obstacle_pixel_y = self.grid.grid_to_pixel(obstacle_grid_coord)[0], \
                                                 self.grid.grid_to_pixel(obstacle_grid_coord)[1]
            border_pixel_length = (self.grid.block_size + MARGIN) * 3  # about 3 squares border
            if (obstacle_pixel_x - border_pixel_length < final_pixel_pos[0] < obstacle_pixel_x + border_pixel_length) \
                    and (obstacle_pixel_y - border_pixel_length < final_pixel_pos[
                1] < obstacle_pixel_y + border_pixel_length):
                raise ObstacleException("OBSTACLE")
                return True

            # Using grid position
            # grid_coord = self.grid.pixel_to_grid(final_pixel_pos)
            # grid_x, grid_y = grid_coord[0], grid_coord[1]
            # if (obstacle_grid_x - 3 <= grid_x <= obstacle_grid_x + 3) \
            #         and (obstacle_grid_y - 3 <= grid_y <= obstacle_grid_y + 3):   # about 3 squares
            #     print("OBSTACLE!!")
            #     return False

        return True

    # NOTE (it's basically checking the 3x3 grid in front/behind the robot to see if its obstacle free and can turn)
    def check_turning_radius(self, turn):
        # Since movement is a turn, create a wider obstacle barrier to account for turning
        # initial position + 3~ grids (according to direction of turn)
        initial_grid_x, initial_grid_y, initial_angle = self.grid_x, self.grid_y, self.angle
        grid_x, grid_y = initial_grid_x, initial_grid_y
        if initial_angle == constants.NORTH:
            if turn == "FORWARD_R" or turn == "FORWARD_L":
                # + 3y
                grid_x, grid_y = grid_x, grid_y + 3
                pass
            elif turn == "BACKWARD_R" or turn == "BACKWARD_L":
                # - 3y
                grid_x, grid_y = grid_x, grid_y - 3
                pass
        elif initial_angle == constants.SOUTH:
            if turn == "FORWARD_R" or turn == "FORWARD_L":
                # - 3y
                grid_x, grid_y = grid_x, grid_y - 3
                pass
            elif turn == "BACKWARD_R" or turn == "BACKWARD_L":
                # + 3y
                grid_x, grid_y = grid_x, grid_y + 3
                pass
        elif initial_angle == constants.EAST:
            if turn == "FORWARD_R" or turn == "FORWARD_L":
                # + 3x
                grid_x, grid_y = grid_x + 3, grid_y
                pass
            elif turn == "BACKWARD_R" or turn == "BACKWARD_L":
                # - 3x
                grid_x, grid_y = grid_x - 3, grid_y
                pass
        elif initial_angle == constants.WEST:
            if turn == "FORWARD_R" or turn == "FORWARD_L":
                # - 3x
                grid_x, grid_y = grid_x - 3, grid_y
                pass
            elif turn == "BACKWARD_R" or turn == "BACKWARD_L":
                # + 3x
                grid_x, grid_y = grid_x + 3, grid_y
                pass

        for obstacle_id in self.grid.get_obstacle_cells():
            obstacle_grid_coord = obstacle_id.split("-")
            obstacle_grid_x, obstacle_grid_y = int(obstacle_grid_coord[0]), int(obstacle_grid_coord[1])
            obstacle_grid_coord = [obstacle_grid_x, obstacle_grid_y]

            # Using pixel position
            obstacle_pixel_x, obstacle_pixel_y = self.grid.grid_to_pixel(obstacle_grid_coord)[0], \
                                                 self.grid.grid_to_pixel(obstacle_grid_coord)[1]
            turning_pixel = self.grid.grid_to_pixel((grid_x, grid_y))
            border_pixel_length = (self.grid.block_size + MARGIN) * 3  # about 3 squares border
            if (obstacle_pixel_x - border_pixel_length < turning_pixel[0] < obstacle_pixel_x + border_pixel_length) \
                    and (
                    obstacle_pixel_y - border_pixel_length < turning_pixel[1] < obstacle_pixel_y + border_pixel_length):
                #raise ObstacleTurnException("OBSTACLE_TURN")
                return True

            # Using grid position
            # if (obstacle_grid_x - 3 <= grid_x <= obstacle_grid_x + 3) \
            #         and (obstacle_grid_y - 3 <= grid_y <= obstacle_grid_y + 3):  # about 3 squares
            #     print("OBSTACLE (TURN)!!")
            #     return False

        return True

    def check_exclude_obstacles(self, final_pixel_pos, turn):
        # Checks if final position will clash into any obstacles, then checks for turning radius obstacles
        if self.check_exclude_obstacles_straight(final_pixel_pos):
            return self.check_turning_radius(turn)
        return False

    # TODO: (slightly later) PATH PLANNING: define sets of robot movements according to destination
    #  image facing direction and robot facing direction (refer to lecture vid for the permutations)

    def reset(self):
        self.angle = constants.ROBOT_STARTING_ANGLE
        self.grid_x = constants.ROBOT_STARTING_X
        self.grid_y = constants.ROBOT_STARTING_Y
        self.pixel_pos = Vector2(self.grid.grid_to_pixel([self.grid_x, self.grid_y])[0],
                                 self.grid.grid_to_pixel([self.grid_x, self.grid_y])[1])
        self.car_rect = pygame.Rect(self.pixel_pos[0] - (0.5 * self.screen_width),
                                    self.pixel_pos[1] - (0.5 * self.screen_height),
                                    self.screen_width, self.screen_height)
        self.redraw_car()
