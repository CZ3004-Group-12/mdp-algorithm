# Collection of colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (192, 192, 192)
BLUE = (50, 100, 150)
LIGHT_BLUE = (100, 255, 255)
LIGHT_RED = (255, 144, 144)
LIGHT_GREEN = (154, 247, 182)

# Collection of robot constants
NORTH = 0
SOUTH = 180
EAST = -90
WEST = 90
STEERING_TIME_DELAY = 1.0
NEXT_OBSTACLE_TIME_DELAY = 1
ROBOT_W = 30
ROBOT_H = 30
# Starting grid positions of car
ROBOT_STARTING_X = 2
ROBOT_STARTING_Y = 2
ROBOT_STARTING_ANGLE = NORTH
BUFFER = 3  # This is the front/back buffer of grids for turning obstacle detection

# Grid
# if (120 < pos[0] < 560) and (120 < pos[1] < 560): to define area within grid
min_pixel_pos_x = 120
min_pixel_pos_y = 120
max_pixel_pos_x = 560
max_pixel_pos_y = 560

FPS = 60

# Path planning
IS_EXCEPTION = False
IS_CHECKING = False
IS_ON_PATH = False

# RPI Connection
RPI_CONNECTED = False

