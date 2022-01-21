import pygame, logging

from map.cell import Cell

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
LIGHT_BLUE = (50, 100, 150)


# This sets the margin between each Cell
MARGIN = 2

# This is the margin around the top and left of the grids
OUTER_MARGIN = 120


class Grid(object):

    def __init__(self, grid_x, grid_y, block_size):
        self.x_size = grid_x
        self.size_y = grid_y
        self.block_size = block_size
        self.cells = [[0 for x in range(grid_x)] for y in range(grid_y)]

        for row in range(grid_y):
            # Add an empty array that will hold each Cell
            # in this row
            for column in range(grid_x):
                if column < 4 and row > 15:
                    self.cells[row][column] = Cell(grid_x, grid_y, 1)
                else:
                    self.cells[row][column] = Cell(grid_x, grid_y, 0)  # Append a Cell

    # TODO: write function to get coordinates of object on grid
    # def value(self, x, y):
    #     cell = self.get_cell(x, y)
    #     return cell.getstatus()

    def get_block_size(self):
        return self.block_size

    def get_cells(self):
        return self.cells

    def get_cell(self, row, column):
        return self.cells[row][column]

    def grid_clicked(self, x_coordinate, y_coordinate):
        # Change the x/y screen coordinates to grid coordinates
        column = x_coordinate // (self.block_size + MARGIN)
        row = y_coordinate // (self.block_size + MARGIN)
        # Set that location to one
        cell = self.get_cell(row, column)
        cell.cell_clicked()
        logging.info("Clicked (x,y): (" + str(x_coordinate) + "," + str(y_coordinate) + "); Grid coordinates: "
                     + str(row) + " " + str(column))

    def draw_grid(self, screen):
        # Draw the grid
        for row in range(20):
            for column in range(20):
                cell = self.cells[row][column]
                color = WHITE
                if cell.get_cell_status() == 1:  # cell is part of starting area
                    color = LIGHT_BLUE
                if cell.get_obstacle_direction() is not None:
                    color = GREEN
                pygame.draw.rect(screen,
                                 color,
                                 [OUTER_MARGIN + (MARGIN + self.block_size) * column + MARGIN,
                                  OUTER_MARGIN + (MARGIN + self.block_size) * row + MARGIN,
                                  self.block_size,
                                  self.block_size])
                if cell.get_obstacle_direction() == "N":
                    pygame.draw.rect(screen,
                                     RED,
                                     [OUTER_MARGIN + (MARGIN + self.block_size) * column + MARGIN,
                                      OUTER_MARGIN + (MARGIN + self.block_size) * row + MARGIN,
                                      self.block_size,
                                      2])
                if cell.get_obstacle_direction() == "E":
                    pygame.draw.rect(screen,
                                     RED,
                                     [OUTER_MARGIN + (MARGIN + self.block_size) * column + MARGIN + 18,
                                      OUTER_MARGIN + (MARGIN + self.block_size) * row + MARGIN,
                                      2,
                                      self.block_size])
                if cell.get_obstacle_direction() == "S":
                    pygame.draw.rect(screen,
                                     RED,
                                     [OUTER_MARGIN + (MARGIN + self.block_size) * column + MARGIN,
                                      OUTER_MARGIN + (MARGIN + self.block_size) * row + MARGIN + 18,
                                      self.block_size,
                                      2])
                if cell.get_obstacle_direction() == "W":
                    pygame.draw.rect(screen,
                                     RED,
                                     [OUTER_MARGIN + (MARGIN + self.block_size) * column + MARGIN,
                                      OUTER_MARGIN + (MARGIN + self.block_size) * row + MARGIN,
                                      2,
                                      self.block_size])
