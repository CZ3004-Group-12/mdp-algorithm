import logging
import pygame

from map.cell import Cell
import constants

# This sets the margin between each Cell
MARGIN = 2

# This is the margin around the top and left of the grids
OUTER_MARGIN = 120


class Grid(object):

    def __init__(self, grid_column, grid_row, block_size):
        self.grid_column = grid_column
        self.grid_row = grid_row
        self.block_size = block_size
        self.cells = [[0 for x in range(grid_column)] for y in range(grid_row)]

        # NOTE!! row and columns start from the top right, but coordinates have to start from the bottom left
        # x-coord = column; y-coord = 19-row
        for row in range(grid_row):
            for column in range(grid_column):
                if column < 4 and row > 15:
                    self.cells[row][column] = Cell(column, (19 - row), 1)  # 19 is to correct the positive direction
                else:
                    self.cells[row][column] = Cell(column, (19 - row), 0)

    def get_block_size(self):
        return self.block_size

    def get_cells(self):
        return self.cells

    def get_cell(self, row, column):
        return self.cells[row][column]

    def grid_clicked(self, x_coordinate, y_coordinate):
        # Change the x/y screen coordinates to grid coordinates
        column = (x_coordinate - 120) // (self.block_size + MARGIN)
        row = (y_coordinate - 120) // (self.block_size + MARGIN)
        # Set that location to one
        cell = self.get_cell(row, column)
        cell.cell_clicked()
        logging.info("Clicked (x,y): (" + str(x_coordinate) + "," + str(y_coordinate) + "); column, row: " + str(column)
                     + "," + str(row) + "; Grid coordinates: " + str(cell.get_xcoord()) + " " + str(cell.get_ycoord()))
        logging.info(self.pixel_to_grid([x_coordinate, y_coordinate]))

    def draw_grid(self, screen):
        # Draw the grid
        for row in range(20):
            for column in range(20):
                cell = self.cells[row][column]
                color = constants.WHITE
                if cell.get_cell_status() == 1:  # cell is part of starting area
                    color = constants.BLUE
                pygame.draw.rect(screen,
                                 color,
                                 [OUTER_MARGIN + (MARGIN + self.block_size) * column + MARGIN,
                                  OUTER_MARGIN + (MARGIN + self.block_size) * row + MARGIN,
                                  self.block_size,
                                  self.block_size])

    def update_grid(self, screen):
        # Draw the grid
        for row in range(20):
            for column in range(20):
                cell = self.cells[row][column]
                color = constants.WHITE
                if cell.get_cell_status() == 1:  # cell is part of starting area
                    color = constants.BLUE
                if cell.get_obstacle_direction() is not None:
                    color = constants.GREEN
                pygame.draw.rect(screen,
                                 color,
                                 [OUTER_MARGIN + (MARGIN + self.block_size) * column + MARGIN,
                                  OUTER_MARGIN + (MARGIN + self.block_size) * row + MARGIN,
                                  self.block_size,
                                  self.block_size])
                if cell.get_obstacle_direction() == "N":
                    pygame.draw.rect(screen,
                                     constants.RED,
                                     [OUTER_MARGIN + (MARGIN + self.block_size) * column + MARGIN,
                                      OUTER_MARGIN + (MARGIN + self.block_size) * row + MARGIN,
                                      self.block_size,
                                      2])
                if cell.get_obstacle_direction() == "E":
                    pygame.draw.rect(screen,
                                     constants.RED,
                                     [OUTER_MARGIN + (MARGIN + self.block_size) * column + MARGIN + 18,
                                      OUTER_MARGIN + (MARGIN + self.block_size) * row + MARGIN,
                                      2,
                                      self.block_size])
                if cell.get_obstacle_direction() == "S":
                    pygame.draw.rect(screen,
                                     constants.RED,
                                     [OUTER_MARGIN + (MARGIN + self.block_size) * column + MARGIN,
                                      OUTER_MARGIN + (MARGIN + self.block_size) * row + MARGIN + 18,
                                      self.block_size,
                                      2])
                if cell.get_obstacle_direction() == "W":
                    pygame.draw.rect(screen,
                                     constants.RED,
                                     [OUTER_MARGIN + (MARGIN + self.block_size) * column + MARGIN,
                                      OUTER_MARGIN + (MARGIN + self.block_size) * row + MARGIN,
                                      2,
                                      self.block_size])

    def grid_to_pixel(self, pos):
        x_pixel = (pos[0]) * (self.block_size + MARGIN) + 120 + (self.block_size + MARGIN) / 2
        y_pixel = (19 - pos[1]) * (self.block_size + MARGIN) + 120 + (self.block_size + MARGIN) / 2
        return [x_pixel, y_pixel]

    def pixel_to_grid(self, pos):
        x_grid = (pos[0] - 120) // (self.block_size + MARGIN)
        y_grid = 19 - ((pos[1] - 120) // (self.block_size + MARGIN))
        return [x_grid, y_grid]

