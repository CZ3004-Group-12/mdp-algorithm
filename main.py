# #!/usr/bin/env python
#
# import pygame
# import math, sys
# from grid import Grid
# # from robot import Robot
#
# WHITE = (200, 200, 200)
# SCREEN_HEIGHT, SCREEN_WIDTH = 700, 900
#
# def main():
# #     global screen, clock
# #     pygame.init()
# #     screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# #     pygame.display.set_caption('MDP Algorithm Simulator')
# #
# #     font = pygame.font.SysFont('arialrounded', 12)
# #
# #     clock = pygame.time.Clock()
# #     screen.fill(WHITE)
# #
# #     while True:
# #         # Draw the 200x200 grid
# #         grid_scale = 1.5
# #         grid_x, grid_y = 400*grid_scale, 400*grid_scale
# #         grid_offset_x, grid_offset_y = 10, 10
# #         cell_size = 20
# #         grid = Grid(grid_x, grid_y, cell_size)
# #         grid.draw_grid(screen, grid_offset_x, grid_offset_y)
# #
# #         # Load 30x30 robot
# #         # robot_w, robot_h = 30, 30
# #         # robot = Robot(grid, grid_x, grid_y, robot_w, robot_h)
# #
# #         # Quit
# #         for event in pygame.event.get():
# #             if event.type == pygame.QUIT:
# #                 pygame.quit()
# #                 sys.exit()
# #
# #         pygame.display.update()
# #
# #
# # if __name__ == '__main__':
# #     main()
"""
 Example program to show using an array to back a grid on-screen.

 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/

 Explanation video: http://youtu.be/mdTeqiWyFnc
"""
import pygame

# Define some colors
from grid import Grid

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
grid = Grid(20,20)

# Initialize pygame
pygame.init()

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [600, 600]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("Array Backed Grid")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            grid.click_grid(pos[0], pos[1])

    # Set the screen background
    screen.fill(BLACK)
    grid.draw_grid(screen)

    # Limit to 60 frames per second
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
