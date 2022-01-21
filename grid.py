import pygame, math

BLACK = (0, 0, 0)

class Grid(object):

    def __init__(self, grid_x, grid_y, cell_size):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.cell_size = cell_size

    def value(self, x, y):
        index = x + (self.w * y)
        return self.data[index]

    def draw_grid(self, screen, x_offset, y_offset):
        for x in range(x_offset, int(self.grid_x), self.cell_size):
            for y in range(y_offset, int(self.grid_y), self.cell_size):
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, BLACK, rect, 1)


