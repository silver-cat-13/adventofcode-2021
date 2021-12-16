#!/usr/bin/env python

'''

'''

from queue import PriorityQueue

class Node:
    def __init__(self, x, y, val):
        self.__x = x
        self.__y = y
        self.__val = val

    def __str__(self):
        return f"({self.x}, {self.y} -> {self.val})"

    def __repr__(self):
        return f"Node({self.x, self.y, self.val})"

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def val(self):
        return self.__val

    def __eq__(self, other):
        return self.x == other.x and self.y == self.y

    def __ne__(self, other):
        return self.x != other.x or self.y != self.y

    def __lt__(self, other):
        return self.val < other.val

    def __le__(self, other):
        return self.val <= other.val

    def __gt__(self, other):
        return self.val > other.val

    def __ge__(self, other):
        return self.val >= other.val

    def __hash__(self):
        return hash((self.x, self.y))


class Map:
    def __init__(self):
        # The map is set as a dict with each elemement is a node with the nodes connected to it
        # For example:
        # {
        #     Node(0,0,1): [Node(1,0,1), Node(0,1,1)],
        #     Node(1,0,1): [Node(0,0,1), Node(1,1,3), Node(0,2,6)],
        # }
        self.__map = []
        self.__visited = set()
        self.__distances = {}
        self.__max_x = 0
        self.__max_y = 0

        # use during the add row function
        self.__previous_row = None


    def __str__(self):
        return f"Map of size {self.max_x}X{self.max_y}"


    @property
    def max_y(self):
        return self.__max_y

    @property
    def max_x(self):
        return self.__max_x

    def add_row(self, row):
        row_values = []
        current_values = len(self.__map)
        for index, value in enumerate(row):
            value = int(value)
            row_values.append(value)
            self.__distances[(index, self.__max_y)] = float("inf")
        self.__map.append(row_values)

        self.__max_y += 1



    def find_shortest_path(self, start_x, start_y):
        # find the shortest path for all nodes using Dijkstra
        start = (start_x, start_y)
        if start not in self.__distances:
            Exception("Invalid starting point")

        self.__distances[start] = 0

        queue = PriorityQueue()
        queue.put((0, start))

        while not queue.empty():
            dist, cur_pos = queue.get()
            self.__visited.add(cur_pos)

            neighbors = [(cur_pos[0]-1, cur_pos[1]), (cur_pos[0], cur_pos[1]-1),
                         (cur_pos[0]+1, cur_pos[1]), (cur_pos[0], cur_pos[1]+1)]

            for neighbor in neighbors:
                if neighbor[0] < 0 or neighbor[1] < 0 or \
                    neighbor[0] >= len(self.__map[0]) or neighbor[1] >= len(self.__map):
                        # out of bound
                        continue

                if neighbor not in self.__visited:
                    self.__visited.add(neighbor)
                    old_cost = self.__distances[neighbor]
                    new_cost = self.__distances[cur_pos] + self.__map[neighbor[0]][neighbor[1]]
                    if new_cost < old_cost:
                        queue.put((new_cost, neighbor))
                        self.__distances[neighbor] = new_cost

        return self.__distances


    def print_map(self):
        for row in self.__map:
            for v in row:
                print(v, end="")
            print()


chiton_map = Map()

initial_map = []
with open('input_data.txt', 'r') as f:
    line = f.readline()
    while line:
        line = line.strip()
        row = []
        for value in line:
            row.append(int(value))
        initial_map.append(row)
        line = f.readline()

for extra_y in range(5):
    for row in initial_map:
        long_row = []
        for extra_x in range(5):
            sub_row = []
            for value in row:
                value = value + extra_x + extra_y
                if value >= 10:
                    value = value % 10 + 1
                sub_row.append(value)

            long_row += sub_row

        chiton_map.add_row(long_row)

distances = chiton_map.find_shortest_path(0, 0)
print(distances[(499, 499)])
