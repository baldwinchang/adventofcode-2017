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
    step = int((corners[1] - corners[0]) / 2)
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

"""
--- Part Two ---

As a stress test on the system, the programs here clear the grid and then store the value 1 in square 1. Then, in the same allocation order as shown above, they store the sum of the values in all adjacent squares, including diagonals.

So, the first few squares' values are chosen as follows:

Square 1 starts with the value 1.
Square 2 has only one adjacent filled square (with value 1), so it also stores 1.
Square 3 has both of the above squares as neighbors and stores the sum of their values, 2.
Square 4 has all three of the aforementioned squares as neighbors and stores the sum of their values, 4.
Square 5 only has the first and fourth squares as neighbors, so it gets the value 5.
Once a square is written, its value does not change. Therefore, the first few squares would receive the following values:

147  142  133  122   59
304    5    4    2   57
330   10    1    1   54
351   11   23   25   26
362  747  806--->   ...
What is the first value written that is larger than your puzzle input?
"""

# We can utilize the previous written code as indices
# for this part of the puzzle.

# It looks like only indices that have been calculated so far are considered
#
# Reader note:
# This is a naive solution... but I am proud that I have deduced this far.


def layer_sides(layer):
    if layer == 0:
        return [[1], [1], [1], [1]]

    side_length = (2 * layer) - 1
    values = layer_values(layer)
    corners = layer_corners(layer)

    sides = list()
    for i in range(4):
        side = list()
        side.append(corners[(i - 1) % len(corners)])
        side.extend(values[i*side_length + i:(i+1)*side_length + i])
        side.append(corners[i % len(corners)])

        sides.append(side)
    return sides


def adjacent_indices(index):
    if index == 1:
        return [1]

    # We care about the immediately adjacent squares
    indices = set()

    # Some important landmarks
    current_layer = layer_of(index)
    previous_layer = current_layer - 1

    # Layer values
    current_layer_values = layer_values(current_layer)

    # Layer sides
    current_layer_sides = layer_sides(current_layer)
    # no_corners match the previous side lengths
    current_layer_sides_no_corners = [current_layer_sides[i][1:-1] for i in range(len(current_layer_sides))]
    previous_layer_sides = layer_sides(previous_layer)

    # Layer Corners
    current_layer_corners = layer_corners(current_layer)
    previous_layer_corners = layer_corners(previous_layer)

    # Simple adjacent indices
    indices.add(index - 1)

    # If I am at the end of my current layer, I will wrap around
    # to the first value of my layer
    if current_layer_values[-1] == index:
        indices.add(current_layer_values[0])

    # If I am close to a corner (distance of one, I want to consider the index immediately prior)
    for corner in current_layer_corners:
        if abs(index - corner) == 1:
            previous_value = current_layer_values[(current_layer_values.index(corner) - 1) % len(current_layer_values)]
            if previous_value < index:
                indices.add(previous_value)
            next_value = current_layer_values[(current_layer_values.index(corner) + 1) % len(current_layer_values)]
            if next_value < index:
                indices.add(next_value)

    # If I am a corner, I have special rules
    # previous corner is my adjacent
    if index in current_layer_corners:
        indices.add(previous_layer_corners[current_layer_corners.index(index)])
    else:
        # Depending on the side I am in
        # 0 = right, 1 = top, 2 = left, 3 = bottom
        # These are based on the convention declared in layer_sides_no_corners
        for i in range(4):
            if index in current_layer_sides[i]:
                previous_layer_index = current_layer_sides_no_corners[i].index(index)
                previous_layer_side = previous_layer_sides[i]
                # add immediate previous layer
                indices.add(previous_layer_side[previous_layer_index])
                # next, up to a wall
                indices.add(previous_layer_side[min(previous_layer_index + 1, len(previous_layer_side) - 1)])
                # previous, up to a wall
                indices.add(previous_layer_side[max(previous_layer_index - 1, 0)])
    return indices


puzzle_map = dict()
puzzle_map[1] = 1
i = 1
while puzzle_map[i] < puzzle_input:
    i += 1
    puzzle_map[i] = sum(puzzle_map[a] for a in adjacent_indices(i))
    print(i,  adjacent_indices(i), puzzle_map[i])

print(puzzle_map[i])
