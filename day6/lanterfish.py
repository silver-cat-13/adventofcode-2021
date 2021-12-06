#!/usr/bin/env python

'''

--- Day 6: Lanternfish ---
The sea floor is getting steeper. Maybe the sleigh keys got carried this way?

A massive school of glowing lanternfish swims past. They must spawn quickly to reach such large
numbers - maybe exponentially quickly? You should model their growth rate to be sure.

Although you know nothing about this specific species of lanternfish, you make some guesses
about their attributes. Surely, each lanternfish creates a new lanternfish once every 7 days.

However, this process isn't necessarily synchronized between every lanternfish - one lanternfish
might have 2 days left until it creates another lanternfish, while another might have 4. So
, you can model each fish as a single number that represents the number of days until it creates
a new lanternfish.

Furthermore, you reason, a new lanternfish would surely need slightly longer before it's capable
of producing more lanternfish: two more days for its first cycle.

So, suppose you have a lanternfish with an internal timer value of 3:

After one day, its internal timer would become 2.
After another day, its internal timer would become 1.
After another day, its internal timer would become 0.
After another day, its internal timer would reset to 6, and it would create a new lanternfish
with an internal timer of 8.
After another day, the first lanternfish would have an internal timer of 5, and the second
lanternfish would have an internal timer of 7.
A lanternfish that creates a new fish resets its timer to 6, not 7 (because 0 is included as
a valid timer value). The new lanternfish starts with an internal timer of 8 and does not start
counting down until the next day.

Realizing what you're trying to do, the submarine automatically produces a list of the ages
of several hundred nearby lanternfish (your puzzle input). For example, suppose you were given
the following list:

3,4,3,1,2
This list means that the first fish has an internal timer of 3, the second fish has an internal
timer of 4, and so on until the fifth fish, which has an internal timer of 2. Simulating these
fish over several days would proceed as follows:

Initial state: 3,4,3,1,2
After  1 day:  2,3,2,0,1
After  2 days: 1,2,1,6,0,8
After  3 days: 0,1,0,5,6,7,8
After  4 days: 6,0,6,4,5,6,7,8,8
After  5 days: 5,6,5,3,4,5,6,7,7,8
After  6 days: 4,5,4,2,3,4,5,6,6,7
After  7 days: 3,4,3,1,2,3,4,5,5,6
After  8 days: 2,3,2,0,1,2,3,4,4,5
After  9 days: 1,2,1,6,0,1,2,3,3,4,8
After 10 days: 0,1,0,5,6,0,1,2,2,3,7,8
After 11 days: 6,0,6,4,5,6,0,1,1,2,6,7,8,8,8
After 12 days: 5,6,5,3,4,5,6,0,0,1,5,6,7,7,7,8,8
After 13 days: 4,5,4,2,3,4,5,6,6,0,4,5,6,6,6,7,7,8,8
After 14 days: 3,4,3,1,2,3,4,5,5,6,3,4,5,5,5,6,6,7,7,8
After 15 days: 2,3,2,0,1,2,3,4,4,5,2,3,4,4,4,5,5,6,6,7
After 16 days: 1,2,1,6,0,1,2,3,3,4,1,2,3,3,3,4,4,5,5,6,8
After 17 days: 0,1,0,5,6,0,1,2,2,3,0,1,2,2,2,3,3,4,4,5,7,8
After 18 days: 6,0,6,4,5,6,0,1,1,2,6,0,1,1,1,2,2,3,3,4,6,7,8,8,8,8
Each day, a 0 becomes a 6 and adds a new 8 to the end of the list, while each other number
decreases by 1 if it was present at the start of the day.

In this example, after 18 days, there are a total of 26 fish. After 80 days, there would be
a total of 5934.

Find a way to simulate lanternfish. How many lanternfish would there be after 80 days?

Your puzzle answer was 353274.

--- Part Two ---
Suppose the lanternfish live forever and have unlimited food and space. Would they take over
the entire ocean?

After 256 days in the example above, there would be a total of 26984457539 lanternfish!

How many lanternfish would there be after 256 days?

Your puzzle answer was 1609314870967.

'''

with open('input_data.txt', 'r') as f:
    lines = f.readlines()

lantern_fish_ages = lines[0].split(',')

# TODO move this into a class object
previous_lanternfish = {}

class Lanternfish:
    def __init__(self, age):
        self.age = age

    # simulate the days and returns the number of days the fish would
    # have spaws and how many times eahc kid would have spawn
    # for example, for 16 days and age 3 a fish would have spawn 2 times
    # and the first kid would have spawn 1, the return would be 3
    def simulate(self, days):
        if days <= self.age:
            # Not enought days for a spawn
            return 0

        # Age is the number of days until the first spawn
        spawns = 1
        days -= (self.age+1)

        # Increase the number of spawn based on the total days for the original fish
        spawns += int(days/7)

        # There is a small set of combinations of spawns+days
        # No need to recalculate over and over again the same combinations
        # Store past combinations to keep it with better performance O(spawns+days)
        spawns_days = str(spawns) +"-"+ str(days)

        if spawns_days not in previous_lanternfish:
            for i in range(spawns):
                spawns += Lanternfish(8).simulate(days-i*7)
            previous_lanternfish[spawns_days] = spawns
            return spawns
        else:
            return previous_lanternfish[spawns_days]

        return spawns

class LanternfishSchool:
    def __init__(self):
        self.school = []

    # Add a lanternfish into the school
    def add(self, lanternfish):
        if not isinstance(lanternfish, Lanternfish):
            raise Exception("Input lanternfish is not a Lanternfish")
        self.school.append(lanternfish)

    def school_size(self):
        return len(self.school)

    def simulate_days(self, days):
        size = self.school_size()

        # Keep the past sizes in a dict to improve performance.
        # There are only 6 possible 6 possible sizes, no need to recalculate the same
        # size for the same giving of days
        past_sizes = {}
        for i, l in enumerate(self.school):
            if l.age not in past_sizes:
                _size = l.simulate(days)
                past_sizes[l.age] = _size
                size += _size
            else:
                size += past_sizes[l.age]
        print(f"After {days} days the size of the school is {size}")

lanternfish_school = LanternfishSchool()
for age in lantern_fish_ages:
    lanternfish_school.add(Lanternfish(int(age)))


lanternfish_school.simulate_days(80)
lanternfish_school.simulate_days(256)

