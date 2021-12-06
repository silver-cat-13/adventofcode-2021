#!/usr/bin/env python

'''
--- Day 5: Hydrothermal Venture ---
You come across a field of hydrothermal vents on the ocean floor! These vents constantly produce
large, opaque clouds, so it would be best to avoid them if possible.

They tend to form in lines; the submarine helpfully produces a list of nearby lines of vents
(your puzzle input) for you to review. For example:

0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
Each line of vents is given as a line segment in the format x1,y1 -> x2,y2 where x1,y1 are
the coordinates of one end the line segment and x2,y2 are the coordinates of the other end.
These line segments include the points at both ends. In other words:

An entry like 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.
An entry like 9,7 -> 7,7 covers points 9,7, 8,7, and 7,7.
For now, only consider horizontal and vertical lines: lines where either x1 = x2 or y1 = y2.

So, the horizontal and vertical lines from the above list would produce the following diagram:

.......1..
..1....1..
..1....1..
.......1..
.112111211
..........
..........
..........
..........
222111....
In this diagram, the top left corner is 0,0 and the bottom right corner is 9,9. Each position
is shown as the number of lines which cover that point or . if no line covers that point. The top-left pair of 1s, for example, comes from 2,2 -> 2,1; the very bottom row is formed by the overlapping lines 0,9 -> 5,9 and 0,9 -> 2,9.

To avoid the most dangerous areas, you need to determine the number of points where at least
two lines overlap. In the above example, this is anywhere in the diagram with a 2 or larger
- a total of 5 points.

Consider only horizontal and vertical lines. At how many points do at least two lines overlap?

 --- Part Two ---
Unfortunately, considering only horizontal and vertical lines doesn't give you the full picture;
you need to also consider diagonal lines.

Because of the limits of the hydrothermal vent mapping system, the lines in your list will
only ever be horizontal, vertical, or a diagonal line at exactly 45 degrees. In other words:

An entry like 1,1 -> 3,3 covers points 1,1, 2,2, and 3,3.
An entry like 9,7 -> 7,9 covers points 9,7, 8,8, and 7,9.
Considering all lines from the above example would now produce the following diagram:

1.1....11.
.111...2..
..2.1.111.
...1.2.2..
.112313211
...1.2....
..1...1...
.1.....1..
1.......1.
222111....
You still need to determine the number of points where at least two lines overlap. In the above
example, this is still anywhere in the diagram with a 2 or larger - now a total of 12 points.

Consider all of the lines. At how many points do at least two lines overlap?
'''

class Coordinate:
    def __init__(self, start_x, start_y, end_x, end_y):
        self.start         = (start_x, start_y)
        self.end           = (end_x, end_y)

    def is_vertical(self):
        return self.start[1] != self.end[1]

    def is_horizontal(self):
        return self.start[0] != self.end[0]

    def is_diagonal(self):
        return self.is_vertical() and self.is_horizontal()

    def horizontal_mov(self):
        return abs(self.end[0] - self.start[0])

    def vertical_mov(self):
        return abs(self.end[1] - self.start[1])

    def lower_x(self):
        return self.start[0] if self.start[0] < self.end[0] else self.end[0]

    def lower_y(self):
        return self.start[1] if self.start[1] < self.end[1] else self.end[1]

    def lower(self):
        return self.start if self.start[1] < self.end[1] else self.end

    def high(self):
        return self.start if self.start[1] > self.end[1] else self.end

    def moving_right(self):
        return self.end[0] - self.start[0] < 0


    def __str__(self):
        return f"{self.start} -> {self.end}"

class Map:
    def __init__(self, max_x, max_y):
        self.map = []
        for _ in range(max_y+2):
            row = [0] * (max_x+2)
            self.map.append(row)

    # Add a coordinate, the coordinate must not be diagonal
    def add_line_coordinate(self, coordinate):
        overlap = 0
        if coordinate.is_diagonal():
            Exception("Coordinate {coordinate} is diagonal")

        start_x = coordinate.lower_x()
        start_y = coordinate.lower_y()

        # TODO we can check if start and end are already overlap (>=2) and return
        # no need do the for loop if all elements are already overlaped
        # If some elements are already overlap and other doesn't, we can only loop
        # around the ones that has not been overlap (0,1), improving performance
        if coordinate.is_vertical():
            mov = coordinate.vertical_mov()
            for i in range(mov+1):
                self.map[start_y+i][start_x] += 1
                if self.map[start_y+i][start_x] == 2:
                    overlap += 1

        else:
            mov = coordinate.horizontal_mov()
            for i in range(mov+1):
                self.map[start_y][start_x+i] += 1
                if self.map[start_y][start_x+i] == 2:
                    overlap += 1

        return overlap

    # TODO combine add_line_coordinate and add_diagonal_coordinate
    # into one function for better managment of the code
    def add_diagonal_coordinate(self, coordinate):
        overlap = 0
        if not coordinate.is_diagonal():
            Exception("Coordinate {coordinate} is not diagonal")


        mov_v = coordinate.vertical_mov()
        mov_h = coordinate.horizontal_mov()

        # Get the coordinates with the lowest Y
        start_x, start_y = coordinate.lower()

        # Get the coordinates with the highest Y
        end_x, end_y = coordinate.high()

        # move from top to bottom

        is_moving_right = end_x - start_x > 0

        if mov_v != mov_h:
            Exception("Coordinate {coordinate} is not 45 degrees")


        # TODO we can check if start and end are already overlap (>=2) and return
        # no need do the for loop if all elements are already overlaped
        # If some elements are already overlap and other doesn't, we can only loop
        # around the ones that has not been overlap (0,1), improving performance
        if is_moving_right:
            # move left to right
            for i in range(mov_h+1):
                self.map[start_y+i][start_x+i] += 1

                if self.map[start_y+i][start_x+i] == 2:
                    overlap += 1
        else:
            # move right to left
            for i in range(mov_h+1):
                self.map[start_y+i][start_x-i] += 1

                if self.map[start_y+i][start_x-i] == 2:
                    overlap += 1

        return overlap


coordinates = []
max_x = 0
max_y = 0

with open('input_data.txt', 'r') as f:
    line = f.readline()
    while line:
        start, end = line.split(' -> ')
        start_x, start_y = start.split(',')
        end_x, end_y = end.split(',')
        start_x = int(start_x)
        start_y = int(start_y)
        end_x = int(end_x)
        end_y = int(end_y)

        coordinates.append(Coordinate(start_x, start_y, end_x, end_y))
        if start_x > max_x:
            max_x = start_x
        if end_x > max_x:
            max_x = end_x

        if start_y > max_y:
            max_y = start_y
        if end_y > max_x:
            max_x = end_y

        line = f.readline()

hydro_map = Map(max_x, max_y)

line_overlaps = 0
diagonal_overlaps = 0
for coordinate in coordinates:
    if not coordinate.is_diagonal():
        line_overlaps += hydro_map.add_line_coordinate(coordinate)
    else:
        diagonal_overlaps += hydro_map.add_diagonal_coordinate(coordinate)


print(f"Straight lines overlaps {line_overlaps}")
print(f"Diagonal + straight lines overlaps {line_overlaps+diagonal_overlaps}")

