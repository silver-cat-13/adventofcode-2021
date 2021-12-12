#!/usr/bin/env python


'''
--- Day 12: Passage Pathing ---
With your submarine's subterranean subsystems subsisting suboptimally, the only way you're getting
out of this cave anytime soon is by finding a path yourself. Not just a path - the only way to
know if you've found the best path is to find all of them.

Fortunately, the sensors are still mostly working, and so you build a rough map of the remaining caves
(your puzzle input). For example:

start-A
start-b
A-c
A-b
b-d
A-end
b-end
This is a list of how all of the caves are connected. You start in the cave named start, and your
destination is the cave named end. An entry like b-d means that cave b is connected to cave d
- that is, you can move between them.

So, the above cave system looks roughly like this:

    start
    /   \
c--A-----b--d
    \   /
     end
Your goal is to find the number of distinct paths that start at start, end at end, and don't
visit small caves more than once. There are two types of caves: big caves (written in uppercase,
like A) and small caves (written in lowercase, like b). It would be a waste of time to visit any
small cave more than once, but big caves are large enough that it might be worth visiting them multiple
times. So, all paths you find should visit small caves at most once, and can visit big caves any
number of times.

Given these rules, there are 10 paths through this example cave system:

start,A,b,A,c,A,end
start,A,b,A,end
start,A,b,end
start,A,c,A,b,A,end
start,A,c,A,b,end
start,A,c,A,end
start,A,end
start,b,A,c,A,end
start,b,A,end
start,b,end
(Each line in the above list corresponds to a single path; the caves visited by that path are listed
in the order they are visited and separated by commas.)

Note that in this cave system, cave d is never visited by any path: to do so, cave b would need
to be visited twice (once on the way to cave d and a second time when returning from cave d),
and since cave b is small, this is not allowed.

Here is a slightly larger example:

dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
The 19 paths through it are as follows:

start,HN,dc,HN,end
start,HN,dc,HN,kj,HN,end
start,HN,dc,end
start,HN,dc,kj,HN,end
start,HN,end
start,HN,kj,HN,dc,HN,end
start,HN,kj,HN,dc,end
start,HN,kj,HN,end
start,HN,kj,dc,HN,end
start,HN,kj,dc,end
start,dc,HN,end
start,dc,HN,kj,HN,end
start,dc,end
start,dc,kj,HN,end
start,kj,HN,dc,HN,end
start,kj,HN,dc,end
start,kj,HN,end
start,kj,dc,HN,end
start,kj,dc,end
Finally, this even larger example has 226 paths through it:

fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
How many paths through this cave system are there that visit small caves at most once?

Your puzzle answer was 3485.

--- Part Two ---
After reviewing the available paths, you realize you might have time to visit a single small cave
twice. Specifically, big caves can be visited any number of times, a single small cave can be
visited at most twice, and the remaining small caves can be visited at most once. However, the
caves named start and end can only be visited exactly once each: once you leave the start cave,
you may not return to it, and once you reach the end cave, the path must end immediately.

Now, the 36 possible paths through the first example above are:

start,A,b,A,b,A,c,A,end
start,A,b,A,b,A,end
start,A,b,A,b,end
start,A,b,A,c,A,b,A,end
start,A,b,A,c,A,b,end
start,A,b,A,c,A,c,A,end
start,A,b,A,c,A,end
start,A,b,A,end
start,A,b,d,b,A,c,A,end
start,A,b,d,b,A,end
start,A,b,d,b,end
start,A,b,end
start,A,c,A,b,A,b,A,end
start,A,c,A,b,A,b,end
start,A,c,A,b,A,c,A,end
start,A,c,A,b,A,end
start,A,c,A,b,d,b,A,end
start,A,c,A,b,d,b,end
start,A,c,A,b,end
start,A,c,A,c,A,b,A,end
start,A,c,A,c,A,b,end
start,A,c,A,c,A,end
start,A,c,A,end
start,A,end
start,b,A,b,A,c,A,end
start,b,A,b,A,end
start,b,A,b,end
start,b,A,c,A,b,A,end
start,b,A,c,A,b,end
start,b,A,c,A,c,A,end
start,b,A,c,A,end
start,b,A,end
start,b,d,b,A,c,A,end
start,b,d,b,A,end
start,b,d,b,end
start,b,end
The slightly larger example above now has 103 paths through it, and the even larger example now
has 3509 paths through it.

Given these new rules, how many paths through this cave system are there?

Your puzzle answer was 85062.
'''

graph_map = {}

class Path:
    def __init__(self, path):
        self.path        = path
        self.lower_caves = {}
        for c in path:
            if c.islower():
                if not c in self.lower_caves:
                    self.lower_caves[c] = 0
                self.lower_caves[c] += 1

    def is_lower_cave_duplicate_part_1(self, cave):
        # return True if input cave is part of the lower_caves list
        if cave in self.lower_caves:
            return self.lower_caves[cave] > 1
        return False


    def is_lower_cave_duplicate_part_2(self, cave):
        # return True if a lower case cave has been visited twice and no other cave has been visited once
        if cave in self.lower_caves:
            if self.lower_caves[cave] == 2:
                # Cave has been seeing 2 times, check no other cave has been seeing more than
                # once
                for c in self.lower_caves:
                    if c == cave:
                        continue
                    if self.lower_caves[c] == 2:
                        return True
                return False
            elif self.lower_caves[cave] > 2:
                return True
        return False

    def is_duplicate(self, cave_start, cave_end):
        # Check if the path has already been done
        path_str = ','.join(self.path)
        return f"{cave_start},{cave_end}" in path_str

    def last_cave(self):
        return self.path[-1]

    def __repr__(self):
        return f"Path({self.path})"

    def __str__(self):
        if self.path:
            return ",".join(self.path)
        return ""

class PassageMap:
    def __init__(self):
        self.graph        = {}
        # Store all the paths from 'start' to 'end' cave
        # NOTE: This might not be needed for part2, (created in part1)
        # we might only store the amount of paths instead as a counter
        # for more efficient memory and performance
        # self.paths_to_end = []
        self.paths_to_end = 0

        self.paths        = []

    def add_node(self, start, end):
        # Add the start and end node in the graph, these are bi-directional graphs
        if start not in self.graph:
            self.graph[start] = []

        if end not in self.graph:
            self.graph[end] = []

        self.graph[start].append(end)
        self.graph[end].append(start)

    def depth_first_search_to_end(self, current_cave='start'):
        # using depth first search find all the paths to end

        if len(self.paths) == 0:
            self.paths.append(Path([current_cave]))
            last_path = self.paths[-1]
        else:
            # add the cave to the last path
            last_path = self.paths[-1]

            if last_path.is_lower_cave_duplicate_part_2(current_cave):
                # current cave is a small cave that has already been seen
                self.paths.pop()
                return

        for cave in self.graph[last_path.last_cave()]:
            if cave == 'start':
                # ignore start cave
                continue

            if cave == 'end':
                # we are at the end of the path
                self.paths_to_end += 1
                p = self.paths[-1]
                p.path.append('end')
                # print(",".join(p.path))
                continue

            # Go deeper
            new_path = last_path.path.copy()
            new_path.append(cave)
            self.paths.append(Path( new_path))
            self.depth_first_search_to_end(cave)

    def number_paths_to_end(self):
        return self.paths_to_end

passage_map = PassageMap()

with open('input_data.txt', 'r') as f:
    line = f.readline()
    while line:
        start, end = line.strip().split('-')

        passage_map.add_node(start, end)

        line = f.readline()


paths_to_end = 0
start_key = 'start'
passage_map.depth_first_search_to_end()

print(f"Number of paths to end: {passage_map.number_paths_to_end()}")


