import os
import time
from math import sin, radians, degrees, copysign
from pygame.math import Vector2
from map import constants
import pygame

# This sets the margin between each Cell
MARGIN = 2
ONE_CELL = 20 + MARGIN
THREE_CELL = 3 * ONE_CELL


class Robot(object):

    def __init__(self, screen, grid, grid_surface, robot_w, robot_h, grid_x, grid_y, angle, car_image):
        self.robot_w = robot_w
        self.robot_h = robot_h
        # actual pixel width and height of robot (inclusive of margin
        self.screen_width = grid.get_block_size() * robot_w / 10 + (robot_w / 10 * MARGIN) + MARGIN
        self.screen_height = grid.get_block_size() * robot_h / 10 + (robot_h / 10 * MARGIN) + MARGIN
        # NOTE: grid_x and grid_y are the grid coordinates of the middle square of the 3x3 car area
        self.grid_x = grid_x
        self.grid_y = grid_y
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
        return self.grid.pixel_to_grid(self.pixel_pos)

    def draw_car(self):
        rotated = pygame.transform.rotate(self.car_image, self.angle)
        rect = rotated.get_rect()
        rect.center = self.car_rect.center
        self.screen.blit(rotated, rect)
        # screen.blit(rotated, self.get_pixel_pos() - (rect.width / 2, rect.height / 2))
        pygame.draw.rect(self.screen, constants.RED, self.car_rect, 1)
        pygame.display.flip()

    def redraw_car(self):
        # Need to redraw over everything (grid_surface, grid and car)
        self.screen.blit(self.grid_surface, (120, 120))
        self.grid.update_grid(self.screen)
        self.draw_car()

    # TODO Engine (Acceleration/Deceleration/Move Backwards

    # TODO: define possible movements (for turning motions picture steering wheel direction)
    # ALL MOTIONS take place in minimal unit.
    # for 1: is by 10 (one grid)
    # for 2-5: is 30 by 30 (3x3 grid) area plus rotation
    # 1. straight (one grid) - forward, backwards
    # 2. forward right/clockwise pi/2 turn
    # 3. forward left/anticlockwise pi/2 turn
    # 4. backward right/anticlockwise pi/2 turn
    # 5. backward left/clockwise pi/2 turn
    def move_forward(self, dt):
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

        # Set velocity of car
        self.velocity += (0, -self.speed)
        while self.get_pixel_pos() != final_pixel_pos:
            self.pixel_pos += self.velocity.rotate(-self.angle) * dt
            self.car_rect = pygame.Rect(self.pixel_pos[0] - (0.5 * self.screen_width),
                                        self.pixel_pos[1] - (0.5 * self.screen_height),
                                        self.screen_width, self.screen_height)
            self.redraw_car()

        # Reset velocity to 0
        self.velocity -= (0, -self.speed)
        self.pixel_pos = final_pixel_pos

    def move_backward(self, dt):
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

        # Set velocity of car
        self.velocity += (0, self.speed)
        while self.get_pixel_pos() != final_pixel_pos:
            self.pixel_pos += self.velocity.rotate(-self.angle) * dt
            self.car_rect = pygame.Rect(self.pixel_pos[0] - (0.5 * self.screen_width),
                                        self.pixel_pos[1] - (0.5 * self.screen_height),
                                        self.screen_width, self.screen_height)
            self.redraw_car()
        # Reset velocity to 0
        self.velocity -= (0, self.speed)
        self.pixel_pos = final_pixel_pos

    def move_forward_steer_right(self, dt):
        print("STEERING RIGHT FORWARD FACING", self.angle)
        # Pause to simulate time taken for wheels to full rotate
        time.sleep(constants.STEERING_TIME_DELAY)

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
        self.angle = final_angle
        self.pixel_pos = final_pixel_pos

    def move_forward_steer_left(self, dt):
        print("STEERING LEFT FORWARD FACING", self.angle)
        # Pause to simulate time taken for wheels to full rotate
        time.sleep(constants.STEERING_TIME_DELAY)

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
        self.angle = final_angle
        self.pixel_pos = final_pixel_pos

    def move_backward_steer_right(self, dt):
        print("STEERING RIGHT BACKWARD FACING", self.angle)
        # Pause to simulate time taken for wheels to full rotate
        time.sleep(constants.STEERING_TIME_DELAY)

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
        self.angle = final_angle
        self.pixel_pos = final_pixel_pos
        print(self.angle)

    def move_backward_steer_left(self, dt):
        print("STEERING LEFT BACKWARD FACING", self.angle)
        # Pause to simulate time taken for wheels to full rotate
        time.sleep(constants.STEERING_TIME_DELAY)

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
        self.angle = final_angle
        self.pixel_pos = final_pixel_pos

    def check_if_reached(self, initial_angle, final_pixel_pos):
        # Set position to stop moving
        if round(self.get_pixel_pos()[0]) == final_pixel_pos[0] \
                and round(self.get_pixel_pos()[1]) == final_pixel_pos[1] \
                and abs(self.angle - initial_angle) <= 90:
            return True
        else:
            return False

    def get_angle_of_rotation(self):
        return self.angle

    def check_obstacles(self):
        grid_x = self.grid_x
        grid_y = self.grid_y
        angle = self.get_angle_of_rotation()
        if angle == "Border":
            return "Border"
        if angle == map.constants.NORTH:
            for i in range(3):
                if grid.check_obstacle_cell(grid_x + i - 1, grid_y + 3) is not None:
                    return grid.get_cell(grid_x + 3, grid_y + i - 1)
        elif angle == map.constants.EAST:
            for i in range(3):
                if grid.check_obstacle_cell(grid_x + 3, grid_y + i - 1) is not None:
                    return grid.get_cell(grid_x + 3, grid_y + i - 1)
        elif angle == map.constants.SOUTH:
            for i in range(3):
                if grid.check_obstacle_cell(grid_x + i - 1, grid_y - 3) is not None:
                    return grid.get_cell(grid_x + i - 1, grid_y + 3)
        elif angle == map.constants.WEST:
            for i in range(3):
                if grid.check_obstacle_cell(grid_x - 3, grid_y + i - 1) is not None:
                    return grid.get_cell(grid_x - 3, grid_y + i - 1)
