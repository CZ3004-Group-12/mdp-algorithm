
import os
import constants

import threading
from communication.comms import AlgoClient
from map.grid import Grid
from interface.panel import Panel
from robot.robot import Robot
from algorithm.astar import AStar
from algorithm.path_planning import PathPlan
import pygame
import logging
import queue

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [960, 660]


class Simulator:

    def __init__(self):
        self.comms = None

        # Initialize pygame
        self.root = pygame
        self.root.init()
        self.root.display.set_caption("MDP Algorithm Simulator")
        self.screen = None
        if not constants.HEADLESS:
            self.screen = pygame.display.set_mode(WINDOW_SIZE)
            self.screen.fill(constants.GRAY)

        # Callback methods queue - for passing of callback functions from worker thread to main UI thread
        self.callback_queue = queue.Queue()

        # Astar class
        self.astar = None
        # Path planner class
        self.path_planner = None

        # Initialise 20 by 20 Grid
        self.grid = Grid(20, 20, 20)
        self.grid.draw_grid(self.screen)
        # Outline Grid
        self.grid_surface = self.root.Surface((442, 442))
        self.grid_surface.fill(constants.BLACK)
        if not constants.HEADLESS:
            self.screen.blit(self.grid_surface, (120, 120))
        # Draw the grid
        self.grid.draw_grid(self.screen)

        # Initialise side panel with buttons
        self.panel = Panel(self.screen)

        # Used to manage how fast the screen updates
        # self.clock = pygame.time.Clock()
        self.startTime = pygame.time.get_ticks() / 1000
        self.ticks = 0

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
        if constants.HEADLESS:  # to simplify implementation, we use 2 threads even if headless
            print("Waiting to connect")
            self.comms = AlgoClient()
            self.comms.connect()
            print("Connected!")
            self.recv_thread = threading.Thread(target=self.receiving_process)
            constants.RPI_CONNECTED = True
            self.recv_thread.start()
            while True:
                try:
                    callback = self.callback_queue.get(False)  # doesn't block
                except queue.Empty:  # raised when queue is empty
                    continue
                if isinstance(callback, list):
                        print(callback)
                        callback[0](callback[1])
                else:
                    callback()

        else:
            while not done:
                # Check for callbacks from worker thread
                while True:
                    try:
                        callback = self.callback_queue.get(False)  # doesn't block
                    except queue.Empty:  # raised when queue is empty
                        break
                    if isinstance(callback, list):
                        print(callback)
                        callback[0](callback[1])
                    else:
                        callback()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        # User clicks the mouse. Get the position
                        pos = pygame.mouse.get_pos()
                        if (120 < pos[0] < 560) and (120 < pos[1] < 560):  # if area clicked is within grid
                            self.grid.grid_clicked(pos[0], pos[1])
                            self.screen.blit(self.grid_surface, (120, 120))  # Redraw the grid outlines
                            self.grid.update_grid(self.screen)  # Update grid if obstacles added
                            self.car.draw_car()  # Redraw the car

                        else:  # otherwise, area clicked is outside of grid
                            self.check_button_clicked(pos)
                
                # Limit to 20 frames per second
                now = pygame.time.get_ticks()/1000
                if now - self.startTime > 1 / constants.FPS:
                    self.startTime = now
                    self.root.display.flip()

        # Be IDLE friendly. If you forget this line, the program will 'hang' on exit.
        self.root.quit()

    def receiving_process(self):
        """
        Method to be run in a separate thread to listen for commands from the socket
        Methods that update the UI must be passed into self.callback_queue for running in the main UI thread
        Running UI updating methods in a worker thread will cause a flashing effect as both threads attempt to update the UI
        """
        
        while constants.RPI_CONNECTED:
            try:
                txt = self.comms.recv()
                if (txt == None):
                    continue
                txt_split = txt.split("|")
                source, message = txt_split[0], txt_split[1]
                if source == "AND":  # From Android
                    print("Received command from ANDROID")
                    message_split = message.split("/", 2)
                    command = message_split[0]
                    task = message_split[1]
                    # E.g. message_split = START/EXPLORE/(R,1,1,0)/(00,04,15,-90)/(01,16,17,90)/(02,12,11,180)/(03,07,03,0)/(04,17,04,90)
                    if command == "START" and task == "EXPLORE":  # Week 8 Task
                        # Reset first
                        self.callback_queue.put(self.reset_button_clicked)

                        obstacles = message_split[2]
                        obstacles_split = obstacles.split("/")

                        # Set robot starting pos
                        print("Setting robot position...")
                        robot_starting_pos = obstacles_split[0].strip("()")
                        robot_params = robot_starting_pos.split(",")
                        print(robot_params)
                        robot_x, robot_y, robot_dir = int(robot_params[1]), int(robot_params[2]), int(robot_params[3])

                        self.callback_queue.put([self.car.update_robot, [robot_dir, self.grid.grid_to_pixel((robot_x, robot_y))]])
                        self.callback_queue.put(self.car.redraw_car)

                        # Create obstacles given parameters
                        print("Creating obstacles...")
                        for obstacle in obstacles_split[1:]:
                            obstacle = obstacle[1:-1]
                            params = obstacle.split(",")
                            id, grid_x, grid_y, dir = params[0], int(params[1]), int(params[2]), int(params[3])
                            self.callback_queue.put([self.grid.create_obstacle, [grid_x, grid_y, dir]])

                        # Update grid, start explore
                        self.callback_queue.put(self.car.redraw_car)
                        print("[AND] Doing path calculation...")
                        self.callback_queue.put(self.start_button_clicked)
                        
                    elif command == "START" and task == "PATH":  # Week 9 Task
                        pass

                elif source == "RPI":
                    print("Received command from RPI")
                    # E.g. ROBOT/NEXT
                    message_split = message.split("/", 1)
                    command = message_split[0]
                    params = message_split[1]
                    if command == "ROBOT" and params == "NEXT":
                        self.callback_queue.put(self.path_planner.send_to_rpi)

            except IndexError:
                self.comms.send("Invalid command: " + txt)
                print("Invalid command: " + txt)

    def reprint_screen_and_buttons(self):
        self.screen.fill(constants.GRAY)
        self.panel.redraw_buttons()

    def check_button_clicked(self, pos):
        # Check if start button was pressed first:
        start_button = self.panel.buttons[-1]
        x, y, l, h = start_button.get_xy_and_lh()
        if (x < pos[0] < (l + x)) and (y < pos[1] < (h + y)):
            self.start_button_clicked()
            return

        for button in self.panel.buttons[0:-1]:
            x, y, l, h = button.get_xy_and_lh()
            if (x < pos[0] < (l + x)) and (y < pos[1] < (h + y)):
                button_func = self.panel.get_button_clicked(button)
                if button_func == "RESET":
                    print("Reset button pressed.")
                    self.reset_button_clicked()
                if button_func == "CONNECT":
                    print("Connect button pressed.")
                    self.comms = AlgoClient()
                    self.comms.connect()
                    self.recv_thread = threading.Thread(target=self.receiving_process)
                    constants.RPI_CONNECTED = True
                    self.recv_thread.start()
                elif button_func == "DISCONNECT":
                    print("Disconnect button pressed.")
                    self.comms.disconnect()
                    constants.RPI_CONNECTED = False
                    self.comms = None

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
        self.astar = AStar(self.grid, self.car.grid_x, self.car.grid_y)
        fastest_route = self.astar.get_astar_route()
        logging.info("Astar route: " + str(fastest_route))
        optimized_fastest_route = self.grid.get_optimized_target_locations(fastest_route)
        self.car.optimized_target_locations = optimized_fastest_route[1:]
        logging.info("Optimized Astar route: " + str(optimized_fastest_route))

        # Path finding
        self.path_planner = PathPlan(self, self.grid, self.car, optimized_fastest_route)
        self.path_planner.start_robot()

        if constants.RPI_CONNECTED:
            self.path_planner.send_to_rpi()

    def reset_button_clicked(self):
        self.grid.reset(self.screen)
        self.car.reset()

