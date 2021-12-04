#!/usr/bin/env python

'''
--- Day 3: Binary Diagnostic ---
The submarine has been making some odd creaking noises, so you ask it to produce a diagnostic
report just in case.

The diagnostic report (your puzzle input) consists of a list of binary numbers which, when
decoded properly, can tell you many useful things about the conditions of the submarine. The
first parameter to check is the power consumption.

You need to use the binary numbers in the diagnostic report to generate two new binary numbers
(called the gamma rate and the epsilon rate). The power consumption can then be found by multiplying
the gamma rate by the epsilon rate.

Each bit in the gamma rate can be determined by finding the most common bit in the corresponding
position of all numbers in the diagnostic report. For example, given the following diagnostic
report:

00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010

Considering only the first bit of each number, there are five 0 bits and seven 1 bits. Since
the most common bit is 1, the first bit of the gamma rate is 1.

The most common second bit of the numbers in the diagnostic report is 0, so the second bit
of the gamma rate is 0.

The most common value of the third, fourth, and fifth bits are 1, 1, and 0, respectively, and
so the final three bits of the gamma rate are 110.

So, the gamma rate is the binary number 10110, or 22 in decimal.

The epsilon rate is calculated in a similar way; rather than use the most common bit, the least
common bit from each position is used. So, the epsilon rate is 01001, or 9 in decimal. Multiplying
the gamma rate (22) by the epsilon rate (9) produces the power consumption, 198.

Use the binary numbers in your diagnostic report to calculate the gamma rate and epsilon rate,
then multiply them together. What is the power consumption of the submarine? (Be sure to
represent your answer in decimal, not binary.)
'''
# Bits are size 110001101000
# If I see a 1 I will add +1 to the value in the dict depending on the position
total_1s_found_per_position = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0,
        10: 0,
        11: 0
        }
total_values = 0

with open('input_data.txt', 'r') as f:
    line = f.readline()

    while line:

        if len(line) != 11:
            Exception(f"Len of line {line} is expected to be 11 bits")

        total_values += 1

        # I'll asume the line is a bin number (only 0s and 1s)
        # Look all the 1s and update the dict
        for i, l in enumerate(line):
            if l == '1':
                total_1s_found_per_position[i] += 1

        line = f.readline()

# Check each position if most common value was 1 or 0
# no need to round-up
half_values = total_values/2
gamna = ''
epsilon = ''
for p in total_1s_found_per_position:
    if total_1s_found_per_position[p] >= half_values:
        # There has been more 1s in position p than half of the values
        # The task did not say what to do if they are equal, asume gamna will be 1
        gamna = gamna + '1'
        epsilon = epsilon + '0'
    else:
        # There has been more 0s in position p than half of the values
        # The task did not mention if they are equal. A
        gamna = gamna + '0'
        epsilon = epsilon + '1'

epsilon_val = int(epsilon,2)
gamna_val = int(gamna,2)
print(f"Gamna is {gamna}={gamna_val} and epsilon {epsilon}={epsilon_val}. Total={gamna_val*epsilon_val}")
