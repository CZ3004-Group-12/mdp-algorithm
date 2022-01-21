#!/usr/bin/env python

import pygame, math, sys
from grid import Grid
# from robot import Robot

WHITE = (200, 200, 200)
SCREEN_HEIGHT, SCREEN_WIDTH = 700, 900

def main():
    global screen, clock
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('MDP Algorithm Simulator')

    font = pygame.font.SysFont('arialrounded', 12)

    clock = pygame.time.Clock()
    screen.fill(WHITE)

    while True:
        # Draw the 200x200 grid
        grid_scale = 1.5
        grid_x, grid_y = 400*grid_scale, 400*grid_scale
        grid_offset_x, grid_offset_y = 10, 10
        cell_size = 20
        grid = Grid(grid_x, grid_y, cell_size)
        grid.draw_grid(screen, grid_offset_x, grid_offset_y)

        # Load 30x30 robot
        # robot_w, robot_h = 30, 30
        # robot = Robot(grid, grid_x, grid_y, robot_w, robot_h)

        # Quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


if __name__ == '__main__':
    main()