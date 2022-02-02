import os
import constants
from map.grid import Grid
from interface.panel import Panel
from robot.robot import Robot
from algorithm.astar import AStar
from algorithm.path_planning import PathPlan
import pygame
import logging

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [1020, 720]
FPS = 40


class Simulator:

    def __init__(self):
        # Initialize pygame
        self.root = pygame
        self.root.init()
        self.root.display.set_caption("MDP Algorithm Simulator")
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.screen.fill(constants.GRAY)

        # Astar class
        self.astar = None

        # Initialise 20 by 20 Grid
        self.grid = Grid(20, 20, 20)
        self.grid.draw_grid(self.screen)
        # Outline Grid
        self.grid_surface = self.root.Surface((442, 442))
        self.grid_surface.fill(constants.BLACK)
        self.screen.blit(self.grid_surface, (120, 120))
        # Draw the grid
        self.grid.draw_grid(self.screen)

        # Initialise side panel with buttons
        self.panel = Panel(self.screen)

        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()

        # Car printing process
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "car.png")
        car_image = pygame.image.load(image_path)
        self.car = Robot(self, self.screen, self.grid, self.grid_surface, constants.ROBOT_W, constants.ROBOT_H,
                         constants.ROBOT_STARTING_X, constants.ROBOT_STARTING_Y, constants.ROBOT_STARTING_ANGLE,
                         car_image)
        # Draw the car
        self.car.draw_car()

        # Loop until the user clicks the close button.
        done = False

        # -------- Main Program Loop -----------
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # User clicks the mouse. Get the position
                    pos = pygame.mouse.get_pos()
                    if (120 < pos[0] < 560) and (120 < pos[1] < 560):    # if area clicked is within grid
                        self.grid.grid_clicked(pos[0], pos[1])
                        self.screen.blit(self.grid_surface, (120, 120))  # Redraw the grid outlines
                        self.grid.update_grid(self.screen)               # Update grid if obstacles added
                        self.car.draw_car()                              # Redraw the car
                    else:                                                # otherwise, area clicked is outside of grid
                        self.check_button_clicked(pos)

            # Limit to 60 frames per second
            self.clock.tick(FPS)

            # Go ahead and update the screen with what we've drawn.
            self.root.display.flip()

        # Be IDLE friendly. If you forget this line, the program will 'hang' on exit.
        self.root.quit()

    def reprint_screen_and_buttons(self):
        self.screen.fill(constants.GRAY)
        self.panel.redraw_buttons()

    def check_button_clicked(self, pos):
        # Check if start button was pressed first:
        start_button = self.panel.buttons[0]
        x, y, l, h = start_button.get_xy_and_lh()
        if (x < pos[0] < (l + x)) and (y < pos[1] < (h + y)):
            self.start_button_clicked()
            return

        for button in self.panel.buttons[1:]:
            x, y, l, h = button.get_xy_and_lh()
            if (x < pos[0] < (l+x)) and (y < pos[1] < (h+y)):
                button_func = self.panel.get_button_clicked(button)
                if button_func == "RESET":
                    print("Reset button pressed.")
                    self.reset_button_clicked()
                if button_func == "CONNECT":
                    print("Connect button pressed.")
                elif button_func == "DISCONNECT":
                    print("Disconnect button pressed.")

                # for testing purposes
                elif button_func == "FORWARD":
                    self.car.move_forward()
                elif button_func == "BACKWARD":
                    self.car.move_backward()
                elif button_func == "FORWARD_RIGHT":
                    self.car.move_forward_steer_right()
                elif button_func == "FORWARD_LEFT":
                    self.car.move_forward_steer_left()
                elif button_func == "BACKWARD_RIGHT":
                    self.car.move_backward_steer_right()
                elif button_func == "BACKWARD_LEFT":
                    self.car.move_backward_steer_left()
                else:
                    return
            else:
                pass

    def start_button_clicked(self):
        print("START button clicked!")

        # Get fastest route
        self.astar = AStar(self.grid, 1, 1)
        fastest_route = self.astar.get_astar_route()
        logging.info("Astar route: " + str(fastest_route))

        # Path finding
        path_planner = PathPlan(self.grid, self.car, fastest_route)
        path_planner.start_robot()

    def reset_button_clicked(self):
        self.grid.reset(self.screen)
        self.car.reset()

