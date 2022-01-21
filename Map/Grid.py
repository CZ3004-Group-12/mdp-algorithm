import pygame

from Map.Cell import Cell

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 20
HEIGHT = 20

# This sets the margin between each Cell
MARGIN = 2

# This is the margin around the top and left of the grids
OuterMargin = 120


class Grid(object):

    def __init__(self, grid_x, grid_y):
        self.x_size = grid_x
        self.size_y = grid_y
        self.grid = []
        for row in range(grid_x):
            # Add an empty array that will hold each Cell
            # in this row
            self.grid.append([])
            for column in range(grid_y):
                if column < 4 and row < 4:
                    status = self.grid[row].append(Cell(grid_x, grid_y, 1))
                else:
                    self.grid[row].append(Cell(grid_x, grid_y, 0))  # Append a Cell

    def value(self, x, y):
        return self.cell[x][y].getstatus()

    def click_grid(self, x_coordinate, y_coordinate):
        # Change the x/y screen coordinates to grid coordinates
        column = x_coordinate // (WIDTH + MARGIN)
        row = y_coordinate // (HEIGHT + MARGIN)
        # Set that location to one
        self.grid[row][column].clickcell();
        print("Click ", x_coordinate, " ", y_coordinate, "Grid coordinates: ", row, column)


    def draw_grid(self, screen):
        # Draw the grid
        for row in range(20):
            for column in range(20):
                color = WHITE
                if self.grid[row][column].checkdirection() != None:
                    color = GREEN
                pygame.draw.rect(screen,
                                 color,
                                 [OuterMargin+(MARGIN + WIDTH) * column + MARGIN,
                                  OuterMargin+(MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])
                print(self.grid[0][0].checkdirection())
                if self.grid[row][column].checkdirection() == "N":
                    pygame.draw.rect(screen,
                                     RED,
                                     [OuterMargin + (MARGIN + WIDTH) * column + MARGIN,
                                      OuterMargin + (MARGIN + HEIGHT) * row + MARGIN,
                                      WIDTH,
                                      2])
                if self.grid[row][column].checkdirection() == "E":
                    pygame.draw.rect(screen,
                                     RED,
                                     [OuterMargin + (MARGIN + WIDTH) * column + MARGIN+18,
                                      OuterMargin + (MARGIN + HEIGHT) * row + MARGIN ,
                                      2,
                                      HEIGHT])
                if self.grid[row][column].checkdirection() == "S":
                    pygame.draw.rect(screen,
                                     RED,
                                     [OuterMargin + (MARGIN + WIDTH) * column + MARGIN,
                                      OuterMargin + (MARGIN + HEIGHT) * row + MARGIN+18,
                                      WIDTH,
                                      2])
                if self.grid[row][column].checkdirection() == "W":
                    pygame.draw.rect(screen,
                                     RED,
                                     [OuterMargin + (MARGIN + WIDTH) * column + MARGIN,
                                      OuterMargin + (MARGIN + HEIGHT) * row + MARGIN,
                                      2,
                                      HEIGHT])