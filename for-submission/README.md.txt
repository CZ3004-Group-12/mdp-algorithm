### For running the project:

- Python Libraries needed:
  1. pygame
  2. numpy
- Use pip install to install the above libraries before running the project

### Details to note:

The arena:

- The map is a 20 by 20 grid of cells
- Each cell represents 10cm x 10cm

The robot:

- Modeled as a 3x3 on the grid
- Actual robot size is about 20cm x 21cm
- Turning radius:
    - Notes suggested about 25cm turning radius
    - In the simulator, the turning radius used is 3x3 which is 30cm by 30cm

The "obstacle" model:

- Physical size is identical to size on grid (1x1) (10cm x 10cm)
- Obstacle border given for astar path planning is about 20cm (2 cells away)
- Obstacle border given for hardcoded shortest path is about 10cm (1 cell away)

###