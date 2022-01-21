starting_position_x = 0
starting_position_y = 0


class Robot(object):

    def __init__(self, grid, grid_width, grid_height, robot_w, robot_h):
        self.screen_width = grid_width
        self.screen_height = grid_height
        self.robot_w = robot_w
        self.robot_h = robot_h
        self.xs = grid_width / grid.get_block_size()
        self.ys = grid_height / grid.get_block_size()
        self.x = self.xs
        self.y = self.ys
        self.grid = grid
        # self.speed = 3
        # self.nudge_limit = 2

    def get_grid_pos(self):
        return self.grid.pixel_to_grid(self.x, self.y)

    # def move_up(self):
    #     for speed in range(self.speed, 0, -1):
    #         new_y = self.y - speed
    #         xs = [0]
    #         for inc in range(1, self.nudge_limit + 1):
    #             xs.append(inc)
    #             xs.append(-inc)
    #         for x in [self.x + e for e in xs]:
    #             if not self.hits_grid(x, new_y):
    #                 self.x = x
    #                 self.y = new_y
    #                 if self.y < 0:
    #                     self.y += self.screen_height
    #                 return
    #
    # def move_down(self):
    #     for speed in range(self.speed, 0, -1):
    #         new_y = self.y + speed
    #         xs = [0]
    #         for inc in range(1, self.nudge_limit + 1):
    #             xs.append(inc)
    #             xs.append(-inc)
    #         for x in [self.x + e for e in xs]:
    #             if not self.hits_grid(x, new_y):
    #                 self.x = x
    #                 self.y = new_y
    #                 if self.y >= self.screen_height:
    #                     self.y -= self.screen_height
    #                 return
    #
    # def move_left(self):
    #     for speed in range(self.speed, 0, -1):
    #         new_x = self.x - speed
    #         ys = [0]
    #         for inc in range(1, self.nudge_limit + 1):
    #             ys.append(inc)
    #             ys.append(-inc)
    #         for y in [self.y + e for e in ys]:
    #             if not self.hits_grid(new_x, y):
    #                 self.x = new_x
    #                 self.y = y
    #                 return
    #
    # def move_right(self):
    #     for speed in range(self.speed, 0, -1):
    #         new_x = self.x + speed
    #         ys = [0]
    #         for inc in range(1, self.nudge_limit + 1):
    #             ys.append(inc)
    #             ys.append(-inc)
    #         for y in [self.y + e for e in ys]:
    #             if not self.hits_grid(new_x, y):
    #                 self.x = new_x
    #                 self.y = y
    #                 return
    #
    # def hits_grid(self, x, y):
    #     offsets = [
    #         [x, y],
    #         [x + self.xs - 1, y],
    #         [x + self.xs - 1, y + self.ys - 1],
    #         [x, y + self.ys - 1]
    #     ]
    #     for p in offsets:
    #         if p[1] < 0:
    #             p[1] += self.screen_height
    #         if p[1] >= self.screen_height:
    #             p[1] -= self.screen_height
    #     index_pairs = set([self.grid.pixel_to_grid(*e) for e in offsets])
    #     return any([self.grid.value(*e) == 'x' for e in index_pairs])
