import pygame
import logging
import os
from map import colours
from map.grid import Grid
from interface.panel import Panel
from robot.robot import Robot
import pygame

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [1020, 720]


class Simulator:

    def __init__(self):
        # Initialize pygame
        self.root = pygame
        self.root.init()
        self.root.display.set_caption("MDP Algorithm Simulator")
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.screen.fill(colours.GRAY)

        # Initialise 20 by 20 Grid
        self.grid = Grid(20, 20, 20)
        self.grid.draw_grid(self.screen)
        # Outline Grid
        self.grid_surface = self.root.Surface((442, 442))
        self.grid_surface.fill(colours.BLACK)
        self.screen.blit(self.grid_surface, (120, 120))

        # Initialise side panel with buttons
        self.panel = Panel(self.screen)

        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()


        #car printing process
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "car.png")
        car_image = pygame.image.load(image_path)
        car = Robot(self.grid, pygame, 30, 30)
        ppu=32



        # Loop until the user clicks the close button.
        done = False

        # -------- Main Program Loop -----------
        while not done:
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    done = True  # Flag that we are done so we exit this loop
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # User clicks the mouse. Get the position
                    pos = pygame.mouse.get_pos()
                    if (120 < pos[0] < 560) and (120 < pos[1] < 560):  # if area clicked is within grid
                        self.grid.grid_clicked(pos[0], pos[1])
                    else:  # otherwise, area clicked is outside of grid
                        self.check_button_clicked(pos)

            # Draw the grid
            self.grid.draw_grid(self.screen)
            # Draw the car
            rotated = pygame.transform.rotate(car_image, 0)
            rect = rotated.get_rect()
            self.screen.blit(rotated, car.get_pixel_pos() - (rect.width / 2, rect.height / 2))
            pygame.display.flip()


            # Limit to 60 frames per second
            self.clock.tick(60)

            # Go ahead and update the screen with what we've drawn.
            self.root.display.flip()

        # Be IDLE friendly. If you forget this line, the program will 'hang' on exit.
        self.root.quit()

    def check_button_clicked(self, pos):
        for button in self.panel.buttons:
            x, y, l, h = button.get_xy_and_lh()
            if (x < pos[0] < (l+x)) and (y < pos[1] < (h+y)):
                self.panel.button_clicked(button)
            else:
                pass

