from queue import PriorityQueue


class AStar:

    def __init__(self, grid, start_cell_x, start_cell_y, obstacle_cells):
        self.TURNS_COST = 14
        self.STRAIGHT_COST = 10

        self.grid = grid
        self.cells = grid.get_cells()

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

        self.target_cells = obstacle_cells
