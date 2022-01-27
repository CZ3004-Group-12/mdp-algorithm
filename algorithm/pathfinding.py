from map import grid
from algorithm import destinationnodes
import math


class PathFinding:
    def __init__(self, robot):
        self.grid = grid
        self.robot = robot
        self.obstacles = self.robot.check_obstacles()
        self.destination_nodes = self.find_destination_nodes()

    def find_destination_nodes(self):
        nodes = []
        for i in self.obstacles:
            if i.get_obstacle_direction == map.constants.NORTH:
                nodes.append(
                    destinationnodes.DestinationNodes(i.get_x_coord(),
                                                      i.get_y_cooord() + 3,
                                                      map.constants.SOUTH))
            elif i.get_obstacle_direction == map.constants.SOUTH:
                nodes.append(
                    destinationnodes.DestinationNodes(i.get_x_coord(),
                                                      i.get_y_cooord() - 3,
                                                      map.constants.NORTH))
            elif i.get_obstacle_direction == map.constants.WEST:
                nodes.append(
                    destinationnodes.DestinationNodes(i.get_x_coord() - 3,
                                                      i.get_y_cooord(),
                                                      map.constants.EAST))
            elif i.get_obstacle_direction == map.constants.EAST:
                nodes.append(
                    destinationnodes.DestinationNodes(i.get_x_coord() + 3,
                                                      i.get_y_cooord(),
                                                      map.constants.WEST))
        return nodes



    # TODO: Path finding algorithm
    def find_path(self):
        #hi

    def next_node(self):
        robot_pos=self.robot.get_grid_pos()
        smallest=100000
        for i in self.destination_nodes:
            displacement = math.sqrt(((robot_pos[0]-i.get_pos()[0])**2)+(robot_pos[1]-i.get_pos()[1])**2)
            if i.check_visited() == False and displacement < smallest:




    def get_destination_nodes(self):
        return self.destination_nodes