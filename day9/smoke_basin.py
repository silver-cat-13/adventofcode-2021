#!/usr/bin/env python

'''
Day 9: Smoke Basin

These caves seem to be lava tubes. Parts are even still volcanically active; small hydrothermal
vents release smoke into the caves that slowly settles like rain.

If you can model how the smoke flows through the caves, you might be able to avoid it and be
that much safer. The submarine generates a heightmap of the floor of the nearby caves for you
(your puzzle input).

Smoke flows to the lowest point of the area it's in. For example, consider the following heightmap:

2199943210
3987894921
9856789892
8767896789
9899965678
Each number corresponds to the height of a particular location, where 9 is the highest and
0 is the lowest a location can be.

Your first goal is to find the low points - the locations that are lower than any of its adjacent
locations. Most locations have four adjacent locations (up, down, left, and right); locations
on the edge or corner of the map have three or two adjacent locations, respectively. (Diagonal
locations do not count as adjacent.)

In the above example, there are four low points, all highlighted: two are in the first row
(a 1 and a 0), one is in the third row (a 5), and one is in the bottom row (also a 5). All
other locations on the heightmap have some lower adjacent location, and so are not low points.

The risk level of a low point is 1 plus its height. In the above example, the risk levels of
the low points are 2, 1, 6, and 6. The sum of the risk levels of all low points in the heightmap
is therefore 15.

Find all of the low points on your heightmap. What is the sum of the risk levels of all low
points on your heightmap?

Your puzzle answer was 575.

--- Part Two ---
Next, you need to find the largest basins so you know what areas are most important to avoid.

A basin is all locations that eventually flow downward to a single low point. Therefore, every
low point has a basin, although some basins are very small. Locations of height 9 do not count
as being in any basin, and all other locations will always be part of exactly one basin.

The size of a basin is the number of locations within the basin, including the low point. The
example above has four basins.

The top-left basin, size 3:

2199943210
3987894921
9856789892
8767896789
9899965678
The top-right basin, size 9:

2199943210
3987894921
9856789892
8767896789
9899965678
The middle basin, size 14:

2199943210
3987894921
9856789892
8767896789
9899965678
The bottom-right basin, size 9:

2199943210
3987894921
9856789892
8767896789
9899965678

Find the three largest basins and multiply their sizes together. In the above example, this
is 9 * 14 * 9 = 1134.

What do you get if you multiply together the sizes of the three largest basins?

Your puzzle answer was 1019700.

Both parts of this puzzle are complete! They provide two gold stars: **

'''

heigh_map = []
with open('input_data.txt', 'r') as f:
    line = f.readline()
    while line:
        line = line.strip()
        heigh_map.append([int(p) for p in line])
        line = f.readline()


class HeightPoint:
    def __init__(self, point, left, right, up, down):
        self.point = point
        self.left  = left
        self.right = right
        self.up    = up
        self.down  = down

    def is_low_point(self):
        ''' return True if the point is a low point '''
        return self.point < self.left and self.point < self.right and \
                self.point < self.up and self.point < self.down

    def risk(self):
        return self.point + 1

    def __str__(self):
        return f"Point: {self.point} with up:{self.up} down:{self.down} left:{self.left} right:{self.right}"

low_points_sum_risk = 0
# Part 1
for current_row, row in enumerate(heigh_map):
    for current_column, p in enumerate(row):
        left  = float("inf") if current_column == 0             else row[current_column-1]
        right = float("inf") if current_column == len(row)-1    else row[current_column+1]
        up    = float("inf") if current_row == 0                else heigh_map[current_row-1][current_column]
        down  = float("inf") if current_row == len(heigh_map)-1 else heigh_map[current_row+1][current_column]

        hp = HeightPoint(p, left, right, up, down)
        if hp.is_low_point():
            # print(f"Low point found {hp}")
            low_points_sum_risk += hp.risk()
print(f"Sum of low risk is {low_points_sum_risk}")

# Part 2

class Basin:
    def __init__(self):
        self.size = 0

    def add_point(self):
        self.size += 1

    def current_size(self):
        return self.size

class LargeBasins:
    def __init__(self):
        self.basins_sizes   = []
        self.smallest_basin = float("-inf")

    def add_basin(self, size):
        if self.smallest_basin < size:
            while len(self.basins_sizes) >= 3:
                # remove smallest one, add the size and sort again
                self.basins_sizes.pop()
            # This list will always be size 3, no need for a high performance
            # structure if it is 3. A high number or variable is better to use
            # a minheap
            self.basins_sizes.append(size)
            # sort and keep smallest one in the last element
            self.basins_sizes.sort(reverse=True)
            self.smallest_basin = self.basins_sizes[-1]

    def all_basins_value(self):
        r = 1
        for b in self.basins_sizes:
            r *= b
        return r

def check_basin(heigh_map, current_basin, start_x, start_y):
    if start_x < 0 or start_y < 0 or start_y >= len(heigh_map) or start_x >= len(heigh_map[start_y]):
        # We are out of bound, return
        return

    if heigh_map[start_y][start_x] == 9:
        # End of the current basin, return
        return

    # Current point is not 9, increase basin size
    current_basin.add_point()

    # change value to 9, this is to not check the same value twice
    heigh_map[start_y][start_x] = 9

    # Check all adjacent points and call functions on those
    check_basin(heigh_map, current_basin, start_x+1, start_y)
    check_basin(heigh_map, current_basin, start_x-1, start_y)
    check_basin(heigh_map, current_basin, start_x, start_y+1)
    check_basin(heigh_map, current_basin, start_x, start_y-1)

def print_map(m):
    for c in m:
        c = [str(x) for x in c]
        print("".join(c))


current_y = 0
basins = LargeBasins()
while current_y < len(heigh_map):
    current_x = 0
    while current_x < len(heigh_map[current_y]):
        if heigh_map[current_y][current_x] == 9:
            # do not check
            current_x += 1
            continue

        basin = Basin()
        check_basin(heigh_map, basin, current_x, current_y)
        basins.add_basin(basin.size)
        current_x += 1
    current_y += 1

print(f"Largest basins values are: {basins.basins_sizes} answer is: {basins.all_basins_value()}")
