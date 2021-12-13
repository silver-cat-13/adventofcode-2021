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

class PassageMap:
    def __init__(self, part_1):
        self.graph                   = {}
        self.small_caves             = {}
        self.paths_to_end            = 0
        self.small_cave_travel_twice = False
        self.part_1                  = part_1

    def add_node(self, start, end):
        # Add the start and end node in the graph, these are bi-directional graphs
        if start not in self.graph:
            self.graph[start] = []

        if end not in self.graph:
            self.graph[end] = []

        if start.islower():
            if start not in self.small_caves:
                self.small_caves[start] = 0
        if end.islower():
            if end not in self.small_caves:
                self.small_caves[end] = 0

        self.graph[start].append(end)
        self.graph[end].append(start)

    def depth_first_search_to_end(self, current_cave='start'):
        # using depth first search find all the paths to end
        # current_cave = last_path[-1]
        for cave in self.graph[current_cave]:
            if cave == 'start':
                # ignore start cave
                continue

            if cave == 'end':
                # we are at the end of the path
                self.paths_to_end += 1
                continue

            # Check the small caves we have traverse
            if cave in self.small_caves:
                if self.small_caves[cave] >= 1:
                    if self.part_1 or self.small_cave_travel_twice:
                        continue
                    self.small_cave_travel_twice = True
                self.small_caves[cave] += 1


            # Go deeper
            self.depth_first_search_to_end(cave)

            if cave in self.small_caves:
                # decrease the number of small caves
                self.small_caves[cave] -= 1
                if self.small_caves[cave] == 1:
                    self.small_cave_travel_twice = False

    def number_paths_to_end(self):
        return self.paths_to_end

    def reset(self, part_1):
        self.paths_to_end = 0
        self.part_1 = part_1

passage_map = PassageMap(part_1=True)

with open('input_data.txt', 'r') as f:
    line = f.readline()
    while line:
        start, end = line.strip().split('-')

        passage_map.add_node(start, end)

        line = f.readline()


passage_map.depth_first_search_to_end()
print(f"number of paths to end for part-1: {passage_map.number_paths_to_end()}")

passage_map.reset(part_1=False)
passage_map.depth_first_search_to_end()
print(f"number of paths to end for part-2: {passage_map.number_paths_to_end()}")

