import pygame

from cells import cell

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 20
HEIGHT = 20

# This sets the margin between each cell
MARGIN = 5


class Grid(object):

    def __init__(self, grid_x, grid_y):
        self.x_size = grid_x
        self.size_y = grid_y
        self.grid = []
        for row in range(grid_x):
            # Add an empty array that will hold each cell
            # in this row
            self.grid.append([])
            for column in range(grid_y):
                self.grid[row].append(cell(grid_x, grid_y, 0))  # Append a cell

    def value(self, x, y):
        return self.cell[x][y].getstatus()

    def click_grid(self, x_coordinate, y_coordinate):
        # Change the x/y screen coordinates to grid coordinates
        column = x_coordinate // (WIDTH + MARGIN)
        row = y_coordinate // (HEIGHT + MARGIN)
        # Set that location to one
        self.grid[row][column].setstatus(1)
        print(self.grid[row][column].getstatus())
        print("Click ", x_coordinate, " ", y_coordinate, "Grid coordinates: ", row, column)

    def draw_grid(self, screen):
        # Draw the grid
        for row in range(20):
            for column in range(20):
                color = WHITE
                if self.grid[row][column].getstatus() == 1:
                    color = GREEN
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])
