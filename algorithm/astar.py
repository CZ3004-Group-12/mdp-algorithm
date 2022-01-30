from queue import PriorityQueue
import math


class AStar:

    def __init__(self, grid, start_cell_x, start_cell_y):
        self.TURNS_COST = 14
        self.STRAIGHT_COST = 10

        self.grid = grid
        self.cells = grid.get_cells()

        self.start_cell_x = start_cell_x
        self.start_cell_y = start_cell_y

        # Cells to be evaluated; Put the cells with the lowest cost in first
        self.all_target_locations = self.get_astar_route()

        self.recorded_movements = []

    def get_displacement(self, pos1, pos2):
        return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

    def get_astar_route(self):
        all_target_unordered = self.grid.get_target_locations()
        all_target_ordered = []
        all_target_ordered.append((self.start_cell_x, self.start_cell_y, 0, None))   # append robot starting positions and direction
        # The order is based on the shortest distance between the previous position to the next target location.
        while len(all_target_unordered) != 0:
            index = 0
            temp = len(all_target_ordered) - 1
            smallest = self.get_displacement([all_target_ordered[temp][0], all_target_ordered[temp][1]],
                                             [all_target_unordered[0][0], all_target_unordered[0][1]])
            for i in range(len(all_target_unordered)):

                if smallest > self.get_displacement([all_target_ordered[temp][0], all_target_ordered[temp][1]],
                                               [all_target_unordered[i][0], all_target_unordered[i][1]]):
                    smallest = self.get_displacement([all_target_ordered[temp][0], all_target_ordered[temp][1]],
                                                [all_target_unordered[i][0], all_target_unordered[i][1]])
                    index = i
            all_target_ordered.append(all_target_unordered.pop(index))
        # print(all_target_ordered)
        return all_target_ordered




