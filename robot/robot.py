import os
from math import sin, radians, degrees, copysign
from pygame.math import Vector2
from map import colours
import pygame

# This sets the margin between each Cell
MARGIN = 2

# How fast/direction in x
dx = 2
# How fast/direction in x
dy = 3

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
        # self.velocity = 3
        # self.acceleration = 1

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
        pygame.display.flip()
        pygame.draw.rect(self.screen, colours.RED, self.car_rect, 1)


    # TODO Engine (Acceleration/Deceleration/Move Backwards

    # TODO: define possible movements (for turning motions picture steering wheel direction)
    # ALL MOTIONS take place in minimal unit.
    # for 1: is by 10 (one grid)
    # for 2-5: is 30 by 30 (3x3 grid) area plus rotation
    # 1. straight (one grid) - up, down, left, right
    # 2. forward right/clockwise pi/2 turn
    # 3. forward left/anticlockwise pi/2 turn
    # 4. backward right/anticlockwise pi/2 turn
    # 5. backward left/clockwise pi/2 turn

    def move_up(self):
        self.pixel_pos[1] -= 20 + MARGIN
        self.car_rect = pygame.Rect(self.pixel_pos[0] - (0.5 * self.screen_width),
                                    self.pixel_pos[1] - (0.5 * self.screen_height),
                                    self.screen_width, self.screen_height)

        # Need to redraw over everything (grid_surface, grid and car)
        self.screen.blit(self.grid_surface, (120, 120))
        self.grid.update_grid(self.screen)
        self.draw_car()

    # def move_up(self):
    #     for speed in range(self.speed, 0, -1):
    #         new_y = self.y - speed
    #         xs = [0]
    #         for inc in range(1, self.nudge_limit + 1):
    #             xs.append(inc)
    #             xs.append(-inc)
    #         for x in [self.x + e for e in xs]:
    #             if not self.hits_grid(x, new_y):
    #                 self.x = x
    #                 self.y = new_y
    #                 if self.y < 0:
    #                     self.y += self.screen_height
    #                 return
    #
    # def move_down(self):
    #     for speed in range(self.speed, 0, -1):
    #         new_y = self.y + speed
    #         xs = [0]
    #         for inc in range(1, self.nudge_limit + 1):
    #             xs.append(inc)
    #             xs.append(-inc)
    #         for x in [self.x + e for e in xs]:
    #             if not self.hits_grid(x, new_y):
    #                 self.x = x
    #                 self.y = new_y
    #                 if self.y >= self.screen_height:
    #                     self.y -= self.screen_height
    #                 return
    #
    # def move_left(self):
    #     for speed in range(self.speed, 0, -1):
    #         new_x = self.x - speed
    #         ys = [0]
    #         for inc in range(1, self.nudge_limit + 1):
    #             ys.append(inc)
    #             ys.append(-inc)
    #         for y in [self.y + e for e in ys]:
    #             if not self.hits_grid(new_x, y):
    #                 self.x = new_x
    #                 self.y = y
    #                 return
    #
    # def move_right(self):
    #     for speed in range(self.speed, 0, -1):
    #         new_x = self.x + speed
    #         ys = [0]
    #         for inc in range(1, self.nudge_limit + 1):
    #             ys.append(inc)
    #             ys.append(-inc)
    #         for y in [self.y + e for e in ys]:
    #             if not self.hits_grid(new_x, y):
    #                 self.x = new_x
    #                 self.y = y
    #                 return
    #
    # def hits_grid(self, x, y):
    #     offsets = [
    #         [x, y],
    #         [x + self.xs - 1, y],
    #         [x + self.xs - 1, y + self.ys - 1],
    #         [x, y + self.ys - 1]
    #     ]
    #     for p in offsets:
    #         if p[1] < 0:
    #             p[1] += self.screen_height
    #         if p[1] >= self.screen_height:
    #             p[1] -= self.screen_height
    #     index_pairs = set([self.grid.pixel_to_grid(*e) for e in offsets])
    #     return any([self.grid.value(*e) == 'x' for e in index_pairs])
