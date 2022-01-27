from queue import PriorityQueue
import math


class AStar:

    def __init__(self, grid, start_cell_x, start_cell_y):
        self.TURNS_COST = 14
        self.STRAIGHT_COST = 10

        self.grid = grid
        self.cells = grid.get_cells()
        self.all_target_locations = self.get_ordered_target(start_cell_x, start_cell_y,0, grid)
        # Cells to be evaluated; Put the cells with the lowest cost in first
        self.open_cells = PriorityQueue()
        # Cells already evaluated
        self.closed_cells = [[0 for x in range(20)] for y in range(20)]
        # x-coord = column; y-coord = 19-row
        # closed_cells[r][c] where r = 19 - y-coord; c = x-coord
        # Mark cells that need not be checked (aka obstacle boundary cells) as visited
        # for row in range(20):
        #     for column in range(20):
        #         if column < 4 and row > 15:
        #             self.cells[row][column] = Cell(column, (19 - row), 1)  # 19 is to correct the positive direction
        #         else:
        #             self.cells[row][column] = Cell(column, (19 - row), 0)

        self.start_cell_x = start_cell_x
        self.start_cell_y = start_cell_y

        self.target_cells = grid.get_obstacle_cells()

    def get_displacement(self, pos1, pos2):
        return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

    def get_ordered_target(self, x, y, direction, grid):
        all_target_unordered = grid.get_target_locations()
        all_target_ordered = []
        all_target_ordered.append((x, y, direction, None))
        # The order is based on the shortest distance between the previous position to the next target location.
        for j in range(len(all_target_unordered)):
            for i in range(len(all_target_unordered)):
                index = 0
                temp = len(all_target_ordered) - 1
                smallest = self.get_displacement([all_target_ordered[temp][0], all_target_ordered[temp][1]],
                                            [all_target_unordered[0][0], all_target_unordered[0][1]])
                if smallest > self.get_displacement([all_target_ordered[temp][0], all_target_ordered[temp][1]],
                                               [all_target_unordered[i][0], all_target_unordered[i][1]]):
                    smallest = self.get_displacement([all_target_ordered[temp][0], all_target_ordered[temp][1]],
                                                [all_target_unordered[i][0], all_target_unordered[i][1]])
                    index = i
            all_target_ordered.append(all_target_unordered.pop(index))
            print(all_target_ordered)
        return all_target_ordered




