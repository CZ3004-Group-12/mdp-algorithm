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
        self.cells_virtual = [[0 for x in range(grid_column)] for y in range(grid_row)]

        # NOTE!! row and columns start from the top right, but coordinates have to start from the bottom left
        # x-coord = column; y-coord = 19-row
        for row in range(grid_row):
            for column in range(grid_column):
                if column < 4 and row > 15:
                    self.cells[row][column] = Cell(column, (19 - row), 1)  # 19 is to correct the positive direction
                else:
                    self.cells[row][column] = Cell(column, (19 - row), 0)

        self.obstacle_cells = {}

    def get_block_size(self):
        return self.block_size

    def get_cells(self):
        return self.cells

    def get_cell(self, row, column):
        return self.cells[row][column]

    def get_cell_by_xycoords(self, x, y):
        column = x
        row = 19 - y
        return self.cells[row][column]

    def get_obstacle_cells(self):
        return self.obstacle_cells

    def get_target_locations(self):
        target_locations = []
        for obstacle_cell in self.obstacle_cells.values():
            # Get target grid positions and NSEW direction that car's centre has to reach for image rec
            target_grid_x, target_grid_y = obstacle_cell.get_xcoord(), obstacle_cell.get_ycoord()
            obstacle_direction = obstacle_cell.get_obstacle_direction()
            target_direction = constants.NORTH
            if obstacle_direction == constants.NORTH:
                target_direction = constants.SOUTH
                target_grid_x, target_grid_y = obstacle_cell.get_xcoord(), obstacle_cell.get_ycoord() + 4
            elif obstacle_direction == constants.SOUTH:
                target_direction = constants.NORTH
                target_grid_x, target_grid_y = obstacle_cell.get_xcoord(), obstacle_cell.get_ycoord() - 4
            elif obstacle_direction == constants.EAST:
                target_direction = constants.WEST
                target_grid_x, target_grid_y = obstacle_cell.get_xcoord() + 4, obstacle_cell.get_ycoord()
            elif obstacle_direction == constants.WEST:
                target_direction = constants.EAST
                target_grid_x, target_grid_y = obstacle_cell.get_xcoord() - 4, obstacle_cell.get_ycoord()

            target_loc = (target_grid_x, target_grid_y, target_direction, obstacle_cell)
            target_locations.append(target_loc)

        return target_locations

    def grid_clicked(self, x_coordinate, y_coordinate):
        # Change the x/y screen coordinates to grid coordinates
        column = (x_coordinate - 120) // (self.block_size + MARGIN)
        row = (y_coordinate - 120) // (self.block_size + MARGIN)

        # Set that location to one
        cell = self.get_cell(row, column)
        cell.cell_clicked()
        # Add/remove cell from dict of obstacles accordingly
        if cell.get_cell_status() == 3:
            if cell.get_obstacle().get_obstacle_id() not in self.obstacle_cells.keys():
                self.obstacle_cells[cell.get_obstacle().get_obstacle_id()] = cell   # '1-12': cell()
        elif cell.get_cell_status() == 0:
            key_to_remove = str(cell.get_xcoord()) + '-' + str(cell.get_ycoord())   # '1-12'
            if key_to_remove in self.obstacle_cells.keys():
                del self.obstacle_cells[key_to_remove]
        self.unset_obstacle_boundary_cells(cell)  # runs only for empty cell
        self.set_starting_area_cells(cell)        # runs only for empty cell
        for r in range(self.grid_row):
            for c in range(self.grid_column):
                a = self.get_cell(r, c)
                self.set_obstacle_boundary_cells(a)  # runs only for obstacle cell

        # Update virtual map for path planning
        for r in range(20):
            for c in range(20):
                cell_status = self.cells[r][c].get_cell_status()
                self.cells_virtual[r][c] = cell_status

        logging.info("Clicked (x,y): (" + str(x_coordinate) + "," + str(y_coordinate) + "); column, row: " + str(column)
                     + "," + str(row) + "; Grid coordinates: " + str(cell.get_xcoord()) + " " + str(cell.get_ycoord())
                     + "; Direction: " + str(cell.get_obstacle_direction()))

    def set_obstacle_boundary_cells(self, cell):
        if cell.get_cell_status() == 3:
            # Set cells around obstacle as boundary
            x, y = cell.get_xcoord() + 1, cell.get_ycoord() + 1  # top right
            if x >= 0 and y >= 0 and x <= 19 and y <= 19 and self.get_cell_by_xycoords(x, y).get_cell_status() != 3:
                self.get_cell_by_xycoords(x, y).set_obstacle_boundary_status()
            x, y = cell.get_xcoord() + 1, cell.get_ycoord()  # right
            if x >= 0 and y >= 0 and x <= 19 and y <= 19 and self.get_cell_by_xycoords(x, y).get_cell_status() != 3:
                self.get_cell_by_xycoords(x, y).set_obstacle_boundary_status()
            x, y = cell.get_xcoord() + 1, cell.get_ycoord() - 1  # bottom right
            if x >= 0 and y >= 0 and x <= 19 and y <= 19 and self.get_cell_by_xycoords(x, y).get_cell_status() != 3:
                self.get_cell_by_xycoords(x, y).set_obstacle_boundary_status()
            x, y = cell.get_xcoord(), cell.get_ycoord() + 1  # top
            if x >= 0 and y >= 0 and x <= 19 and y <= 19 and self.get_cell_by_xycoords(x, y).get_cell_status() != 3:
                self.get_cell_by_xycoords(x, y).set_obstacle_boundary_status()
            x, y = cell.get_xcoord(), cell.get_ycoord() - 1  # bottom
            if x >= 0 and y >= 0 and x <= 19 and y <= 19 and self.get_cell_by_xycoords(x, y).get_cell_status() != 3:
                self.get_cell_by_xycoords(x, y).set_obstacle_boundary_status()
            x, y = cell.get_xcoord() - 1, cell.get_ycoord() + 1  # top left
            if x >= 0 and y >= 0 and x <= 19 and y <= 19 and self.get_cell_by_xycoords(x, y).get_cell_status() != 3:
                self.get_cell_by_xycoords(x, y).set_obstacle_boundary_status()
            x, y = cell.get_xcoord() - 1, cell.get_ycoord()  # left
            if x >= 0 and y >= 0 and x <= 19 and y <= 19 and self.get_cell_by_xycoords(x, y).get_cell_status() != 3:
                self.get_cell_by_xycoords(x, y).set_obstacle_boundary_status()
            x, y = cell.get_xcoord() - 1, cell.get_ycoord() - 1  # bottom left
            if x >= 0 and y >= 0 and x <= 19 and y <= 19 and self.get_cell_by_xycoords(x, y).get_cell_status() != 3:
                self.get_cell_by_xycoords(x, y).set_obstacle_boundary_status()

            # # Extend boundary by 2 squares
            # x, y = cell.get_xcoord() + 2, cell.get_ycoord() + 2  # top right
            # if x >= 0 and y >= 0 and x <= 19 and y <= 19 and self.get_cell_by_xycoords(x, y).get_cell_status() != 3:
            #     self.get_cell_by_xycoords(x, y).set_obstacle_boundary_status()
            # x, y = cell.get_xcoord() + 2, cell.get_ycoord()  # right
            # if x >= 0 and y >= 0 and x <= 19 and y <= 19 and self.get_cell_by_xycoords(x, y).get_cell_status() != 3:
            #     self.get_cell_by_xycoords(x, y).set_obstacle_boundary_status()
            # x, y = cell.get_xcoord() + 2, cell.get_ycoord() - 2  # bottom right
            # if x >= 0 and y >= 0 and x <= 19 and y <= 19 and self.get_cell_by_xycoords(x, y).get_cell_status() != 3:
            #     self.get_cell_by_xycoords(x, y).set_obstacle_boundary_status()
            # x, y = cell.get_xcoord(), cell.get_ycoord() + 2  # top
            # if x >= 0 and y >= 0 and x <= 19 and y <= 19 and self.get_cell_by_xycoords(x, y).get_cell_status() != 3:
            #     self.get_cell_by_xycoords(x, y).set_obstacle_boundary_status()
            # x, y = cell.get_xcoord(), cell.get_ycoord() - 2  # bottom
            # if x >= 0 and y >= 0 and x <= 19 and y <= 19 and self.get_cell_by_xycoords(x, y).get_cell_status() != 3:
            #     self.get_cell_by_xycoords(x, y).set_obstacle_boundary_status()
            # x, y = cell.get_xcoord() - 2, cell.get_ycoord() + 2  # top left
            # if x >= 0 and y >= 0 and x <= 19 and y <= 19 and self.get_cell_by_xycoords(x, y).get_cell_status() != 3:
            #     self.get_cell_by_xycoords(x, y).set_obstacle_boundary_status()
            # x, y = cell.get_xcoord() - 2, cell.get_ycoord()  # left
            # if x >= 0 and y >= 0 and x <= 19 and y <= 19 and self.get_cell_by_xycoords(x, y).get_cell_status() != 3:
            #     self.get_cell_by_xycoords(x, y).set_obstacle_boundary_status()
            # x, y = cell.get_xcoord() - 2, cell.get_ycoord() - 2  # bottom left
            # if x >= 0 and y >= 0 and x <= 19 and y <= 19 and self.get_cell_by_xycoords(x, y).get_cell_status() != 3:
            #     self.get_cell_by_xycoords(x, y).set_obstacle_boundary_status()

    def unset_obstacle_boundary_cells(self, cell):
        if cell.get_cell_status() == 0:
            # UNSET cells around removed obstacle as empty
            x, y = cell.get_xcoord() + 1, cell.get_ycoord() + 1  # top right
            if x >= 0 and y >= 0 and x <= 19 and y <= 19 and self.get_cell_by_xycoords(x, y).get_cell_status() != 3:
                self.get_cell_by_xycoords(x, y).set_empty_status()
            x, y = cell.get_xcoord() + 1, cell.get_ycoord()  # right
            if x >= 0 and y >= 0 and x <= 19 and y <= 19 and self.get_cell_by_xycoords(x, y).get_cell_status() != 3:
                self.get_cell_by_xycoords(x, y).set_empty_status()
            x, y = cell.get_xcoord() + 1, cell.get_ycoord() - 1  # bottom right
            if x >= 0 and y >= 0 and x <= 19 and y <= 19 and self.get_cell_by_xycoords(x, y).get_cell_status() != 3:
                self.get_cell_by_xycoords(x, y).set_empty_status()
            x, y = cell.get_xcoord(), cell.get_ycoord() + 1  # top
            if x >= 0 and y >= 0 and x <= 19 and y <= 19 and self.get_cell_by_xycoords(x, y).get_cell_status() != 3:
                self.get_cell_by_xycoords(x, y).set_empty_status()
            x, y = cell.get_xcoord(), cell.get_ycoord() - 1  # bottom
            if x >= 0 and y >= 0 and x <= 19 and y <= 19 and self.get_cell_by_xycoords(x, y).get_cell_status() != 3:
                self.get_cell_by_xycoords(x, y).set_empty_status()
            x, y = cell.get_xcoord() - 1, cell.get_ycoord() + 1  # top left
            if x >= 0 and y >= 0 and x <= 19 and y <= 19 and self.get_cell_by_xycoords(x, y).get_cell_status() != 3:
                self.get_cell_by_xycoords(x, y).set_empty_status()
            x, y = cell.get_xcoord() - 1, cell.get_ycoord()  # left
            if x >= 0 and y >= 0 and x <= 19 and y <= 19 and self.get_cell_by_xycoords(x, y).get_cell_status() != 3:
                self.get_cell_by_xycoords(x, y).set_empty_status()
            x, y = cell.get_xcoord() - 1, cell.get_ycoord() - 1  # bottom left
            if x >= 0 and y >= 0 and x <= 19 and y <= 19 and self.get_cell_by_xycoords(x, y).get_cell_status() != 3:
                self.get_cell_by_xycoords(x, y).set_empty_status()

            # # Extended boundary
            # x, y = cell.get_xcoord() + 2, cell.get_ycoord() + 2  # top right
            # if x >= 0 and y >= 0 and x <= 19 and y <= 19 and self.get_cell_by_xycoords(x, y).get_cell_status() != 3:
            #     self.get_cell_by_xycoords(x, y).set_empty_status()
            # x, y = cell.get_xcoord() + 2, cell.get_ycoord()  # right
            # if x >= 0 and y >= 0 and x <= 19 and y <= 19 and self.get_cell_by_xycoords(x, y).get_cell_status() != 3:
            #     self.get_cell_by_xycoords(x, y).set_empty_status()
            # x, y = cell.get_xcoord() + 2, cell.get_ycoord() - 2  # bottom right
            # if x >= 0 and y >= 0 and x <= 19 and y <= 19 and self.get_cell_by_xycoords(x, y).get_cell_status() != 3:
            #     self.get_cell_by_xycoords(x, y).set_empty_status()
            # x, y = cell.get_xcoord(), cell.get_ycoord() + 2  # top
            # if x >= 0 and y >= 0 and x <= 19 and y <= 19 and self.get_cell_by_xycoords(x, y).get_cell_status() != 3:
            #     self.get_cell_by_xycoords(x, y).set_empty_status()
            # x, y = cell.get_xcoord(), cell.get_ycoord() - 2  # bottom
            # if x >= 0 and y >= 0 and x <= 19 and y <= 19 and self.get_cell_by_xycoords(x, y).get_cell_status() != 3:
            #     self.get_cell_by_xycoords(x, y).set_empty_status()
            # x, y = cell.get_xcoord() - 2, cell.get_ycoord() + 2  # top left
            # if x >= 0 and y >= 0 and x <= 19 and y <= 19 and self.get_cell_by_xycoords(x, y).get_cell_status() != 3:
            #     self.get_cell_by_xycoords(x, y).set_empty_status()
            # x, y = cell.get_xcoord() - 2, cell.get_ycoord()  # left
            # if x >= 0 and y >= 0 and x <= 19 and y <= 19 and self.get_cell_by_xycoords(x, y).get_cell_status() != 3:
            #     self.get_cell_by_xycoords(x, y).set_empty_status()
            # x, y = cell.get_xcoord() - 2, cell.get_ycoord() - 2  # bottom left
            # if x >= 0 and y >= 0 and x <= 19 and y <= 19 and self.get_cell_by_xycoords(x, y).get_cell_status() != 3:
            #     self.get_cell_by_xycoords(x, y).set_empty_status()

    def set_starting_area_cells(self, cell):
        if cell.get_cell_status() == 0:
            # Reset starting area cells
            x, y = cell.get_xcoord() + 1, cell.get_ycoord() + 1  # top right
            if 0 <= x < 4 and 0 <= y < 4:
                self.get_cell_by_xycoords(x, y).set_starting_area_status()
            x, y = cell.get_xcoord() + 1, cell.get_ycoord()  # right
            if 0 <= x < 4 and 0 <= y < 4:
                self.get_cell_by_xycoords(x, y).set_starting_area_status()
            x, y = cell.get_xcoord() + 1, cell.get_ycoord() - 1  # bottom right
            if 0 <= x < 4 and 0 <= y < 4:
                self.get_cell_by_xycoords(x, y).set_starting_area_status()
            x, y = cell.get_xcoord(), cell.get_ycoord() + 1  # top
            if 0 <= x < 4 and 0 <= y < 4:
                self.get_cell_by_xycoords(x, y).set_starting_area_status()
            x, y = cell.get_xcoord(), cell.get_ycoord() - 1  # bottom
            if 0 <= x < 4 and 0 <= y < 4:
                self.get_cell_by_xycoords(x, y).set_starting_area_status()
            x, y = cell.get_xcoord() - 1, cell.get_ycoord() + 1  # top left
            if 0 <= x < 4 and 0 <= y < 4:
                self.get_cell_by_xycoords(x, y).set_starting_area_status()
            x, y = cell.get_xcoord() - 1, cell.get_ycoord()  # left
            if 0 <= x < 4 and 0 <= y < 4:
                self.get_cell_by_xycoords(x, y).set_starting_area_status()
            x, y = cell.get_xcoord() - 1, cell.get_ycoord() - 1  # bottom left
            if 0 <= x < 4 and 0 <= y < 4:
                self.get_cell_by_xycoords(x, y).set_starting_area_status()

    def set_obstacle_as_visited(self, obstacle_cell):
        obstacle_cell.set_obstacle_visited_status()

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
                cell = self.get_cell(row, column)
                color = constants.WHITE
                if cell.get_cell_status() == 1:  # cell is part of starting area
                    color = constants.BLUE
                if cell.get_cell_status() == 2:  # cell is not an obstacle but is an obstacle boundary
                    color = constants.LIGHT_RED
                if cell.get_cell_status() == 3:  # cell has an obstacle
                    color = constants.GREEN
                if cell.get_cell_status() == 4:  # obstacle cell has been visited
                    color = constants.LIGHT_GREEN
                if cell.get_cell_status() >= 5:  # cell is part of path
                    color = constants.GRAY
                pygame.draw.rect(screen,
                                 color,
                                 [OUTER_MARGIN + (MARGIN + self.block_size) * column + MARGIN,
                                  OUTER_MARGIN + (MARGIN + self.block_size) * row + MARGIN,
                                  self.block_size,
                                  self.block_size])
                if cell.get_obstacle_direction() == constants.NORTH:
                    pygame.draw.rect(screen,
                                     constants.RED,
                                     [OUTER_MARGIN + (MARGIN + self.block_size) * column + MARGIN,
                                      OUTER_MARGIN + (MARGIN + self.block_size) * row + MARGIN,
                                      self.block_size,
                                      2])
                if cell.get_obstacle_direction() == constants.EAST:
                    pygame.draw.rect(screen,
                                     constants.RED,
                                     [OUTER_MARGIN + (MARGIN + self.block_size) * column + MARGIN + 18,
                                      OUTER_MARGIN + (MARGIN + self.block_size) * row + MARGIN,
                                      2,
                                      self.block_size])
                if cell.get_obstacle_direction() == constants.SOUTH:
                    pygame.draw.rect(screen,
                                     constants.RED,
                                     [OUTER_MARGIN + (MARGIN + self.block_size) * column + MARGIN,
                                      OUTER_MARGIN + (MARGIN + self.block_size) * row + MARGIN + 18,
                                      self.block_size,
                                      2])
                if cell.get_obstacle_direction() == constants.WEST:
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

    def reset(self, screen):
        self.obstacle_cells = {}
        for row in range(self.grid_row):
            for column in range(self.grid_column):
                if column < 4 and row > 15:
                    self.cells[row][column] = Cell(column, (19 - row), 1)  # 19 is to correct the positive direction
                else:
                    self.cells[row][column] = Cell(column, (19 - row), 0)
        self.draw_grid(screen)
