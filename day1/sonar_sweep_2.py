#!/usr/bin/env python

# https://adventofcode.com/2021/day/1

# -- Part Two ---
# Considering every single measurement isn't as useful as you expected: there's just too much
# noise in the data.
#
# Instead, consider sums of a three-measurement sliding window. Again considering the above
# example:
#
# 199  A
# 200  A B
# 208  A B C
# 210    B C D
# 200  E   C D
# 207  E F   D
# 240  E F G
# 269    F G H
# 260      G H
# 263        H
# Start by comparing the first and second three-measurement windows. The measurements in the
# first window are marked A (199, 200, 208); their sum is 199 + 200 + 208 = 607. The second
# window is marked B (200, 208, 210); its sum is 618. The sum of measurements in the second
# window is larger than the sum of the first, so this first comparison increased.
#
# Your goal now is to count the number of times the sum of measurements in this sliding window
# increases from the previous sum. So, compare A with B, then compare B with C, then C with
# D, and so on. Stop when there aren't enough measurements left to create a new three-measurement
# sum.
#
# In the above example, the sum of each three-measurement window is as follows:
#
# A: 607 (N/A - no previous sum)
# B: 618 (increased)
# C: 618 (no change)
# D: 617 (decreased)
# E: 647 (increased)
# F: 716 (increased)
# G: 769 (increased)
# H: 792 (increased)
# In this example, there are 5 sums that are larger than the previous sum.
#

class Window:
    def __init__(self):
        self.window = []
    def add(self, value):
        if len(self.window) == 3:
            raise Exception("Window has reached limit")
        self.window.append(value)
    def is_window_full(self):
        return len(self.window) == 3
    def total_sum(self):
        s = sum(self.window)
        self.flush()
        return s
    def capacity(self):
        return 3 - len(self.window)
    def flush(self):
        self.window = []

increase_count = 0
previous_measurement = -1

windows = (Window(), Window(), Window(), Window())

with open('input.txt', 'r') as f:
    line = f.readline()
    current_window = 0
    while line:
        current_window_cap = windows[current_window].capacity()
        v = int(line)

        if current_window_cap == 3:
            # Current window is empty, only add here
            windows[current_window].add(v)
        if current_window_cap == 2:
            # Add in this window and the next one
            windows[current_window].add(v)
            windows[(current_window + 1) % 4].add(v)
        if current_window_cap == 1:
            # Add in this window and the next 2
            windows[current_window].add(v)
            windows[(current_window + 1) % 4].add(v)
            windows[(current_window + 2) % 4].add(v)
        if current_window_cap == 0:
            # Window is full, calculate total sum
            if previous_measurement == -1:
                # First measurement
                previous_measurement = windows[current_window].total_sum()
            else:
                current_measurement = windows[current_window].total_sum()
                if previous_measurement < current_measurement:
                    print(f"Depth increased from {previous_measurement} to {current_measurement}")
                    increase_count += 1
                previous_measurement = current_measurement

            # increase current window and add the value to the next 3 windows
            current_window = (current_window + 1) % 4
            windows[current_window].add(v)
            windows[(current_window + 1) % 4].add(v)
            windows[(current_window + 2) % 4].add(v)


        line = f.readline()

print(f"Current window {current_window}")
for w in windows:
    print(f"Last total {w.total_sum()}")
print(f"Total times the depth increased {increase_count}")
