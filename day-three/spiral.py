__author__ = 'Baldwin Chang'

"""
--- Day 3: Spiral Memory ---

You come across an experimental new kind of memory stored on an infinite two-dimensional grid.

Each square on the grid is allocated in a spiral pattern starting at a location marked 1 and then counting up while spiraling outward. For example, the first few squares are allocated like this:

17  16  15  14  13
18   5   4   3  12
19   6   1   2  11
20   7   8   9  10
21  22  23---> ...
While this is very space-efficient (no squares are skipped), requested data must be carried back to square 1 (the location of the only access port for this memory system) by programs that can only move up, down, left, or right. They always take the shortest path: the Manhattan Distance between the location of the data and square 1.

For example:

Data from square 1 is carried 0 steps, since it's at the access port.
Data from square 12 is carried 3 steps, such as: down, left, left.
Data from square 23 is carried only 2 steps: up twice.
Data from square 1024 must be carried 31 steps.
How many steps are required to carry the data from the square identified in your puzzle input all the way to the access port?
"""

puzzle_input = 361527


def layer_of(n):
    if n == 1:
        return 0

    layer = 1
    square = 3
    while square**2 < n:
        square += 2
        layer += 1
    return layer

# Some test cases
assert layer_of(1) == 0
assert layer_of(3) == 1
assert layer_of(13) == 2
assert layer_of(25) == 2


def layer_values(layer):
    if layer == 0:
        return [1]

    layer_square = layer * 2 + 1
    return [value for value in range(((layer_square - 2) ** 2) + 1, (layer_square ** 2) + 1)]

# More test cases
assert layer_values(0) == [1]
assert layer_values(1) == [2, 3, 4, 5, 6, 7, 8, 9]
assert layer_values(2) == [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]


def layer_corners(layer):
    values = layer_values(layer)
    step = int(len(values) / 4)
    return [values[step*(i + 1) - 1] for i in range(4)]

assert layer_corners(1) == [3, 5, 7, 9]
assert layer_corners(2) == [13, 17, 21, 25]


def layer_cross(layer):
    corners = layer_corners(layer)
    step = (corners[1] - corners[0]) / 2
    return [corner - step for corner in corners]

assert layer_cross(1) == [2, 4, 6, 8]
assert layer_cross(2) == [11, 15, 19, 23]


def closest_cross_value(n):
    layer = layer_of(n)
    cross = layer_cross(layer)

    distances = [abs(cross_value - n) for cross_value in cross]
    min_distance = min(distances)

    return cross[distances.index(min_distance)]

assert closest_cross_value(2) == 2
assert closest_cross_value(12) == 11
assert closest_cross_value(20) == 19


def steps_to_center(n):
    if n == 1:
        return 0

    layer = layer_of(n)
    closest_cross = closest_cross_value(n)
    distance_to_closest_cross_value = abs(closest_cross - n)

    return distance_to_closest_cross_value + layer

assert steps_to_center(2) == 1
assert steps_to_center(12) == 3
assert steps_to_center(23) == 2
assert steps_to_center(1024) == 31

print(steps_to_center(puzzle_input))
