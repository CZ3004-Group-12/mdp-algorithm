import pygame
import logging

# Define some colors
from map.grid import Grid

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Logging
logging.basicConfig(level=logging.INFO)


def main():
    # Initialize pygame
    pygame.init()

    # Create a 2 dimensional array. A two-dimensional
    grid = Grid(20, 20, 20)

    # Set the HEIGHT and WIDTH of the screen
    WINDOW_SIZE = [1280, 720]
    screen = pygame.display.set_mode(WINDOW_SIZE)

    # Set title of screen
    pygame.display.set_caption("MDP Algorithm Simulator")

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # Loop until the user clicks the close button.
    done = False

    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                if (120 < pos[0] < 560) and (120 < pos[1] < 560):  # if area clicked is within grid
                    grid.grid_clicked(pos[0] - 120, pos[1] - 120)

        # Set the screen background
        screen.fill(BLACK)
        grid.draw_grid(screen)

        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()


if __name__ == '__main__':
    main()
