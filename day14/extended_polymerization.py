#!/usr/bin/env python

'''
--- Day 14: Extended Polymerization ---
The incredible pressures at this depth are starting to put a strain on your submarine. The
submarine has polymerization equipment that would produce suitable materials to reinforce the
submarine, and the nearby volcanically-active caves should even have the necessary input elements
in sufficient quantities.

The submarine manual contains instructions for finding the optimal polymer formula; specifically
, it offers a polymer template and a list of pair insertion rules (your puzzle input). You
just need to work out what polymer would result after repeating the pair insertion process
a few times.

For example:

NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
The first line is the polymer template - this is the starting point of the process.

The following section defines the pair insertion rules. A rule like AB -> C means that when
elements A and B are immediately adjacent, element C should be inserted between them. These
insertions all happen simultaneously.

So, starting with the polymer template NNCB, the first step simultaneously considers all three
pairs:

The first pair (NN) matches the rule NN -> C, so element C is inserted between the first N
and the second N.
The second pair (NC) matches the rule NC -> B, so element B is inserted between the N and the
C.
The third pair (CB) matches the rule CB -> H, so element H is inserted between the C and the
B.
Note that these pairs overlap: the second element of one pair is the first element of the next
pair. Also, because all pairs are considered simultaneously, inserted elements are not considered
to be part of a pair until the next step.


After the first step of this process, the polymer becomes NCNBCHB.

Here are the results of a few steps using the above rules:

Template:     NNCB
After step 1: NCNBCHB
After step 2: NBCCNBBBCBHCB
After step 3: NBBBCNCCNBBNBNBBCHBHHBCHB
After step 4: NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB
This polymer grows quickly. After step 5, it has length 97; After step 10, it has length 3073
. After step 10, B occurs 1749 times, C occurs 298 times, H occurs 161 times, and N occurs
865 times; taking the quantity of the most common element (B, 1749) and subtracting the quantity
of the least common element (H, 161) produces 1749 - 161 = 1588.

Apply 10 steps of pair insertion to the polymer template and find the most and least common
elements in the result. What do you get if you take the quantity of the most common element
and subtract the quantity of the least common element?

Your puzzle answer was 2170.

--- Part Two ---
The resulting polymer isn't nearly strong enough to reinforce the submarine. You'll need to
run more steps of the pair insertion process; a total of 40 steps should do it.

In the above example, the most common element is B (occurring 2192039569602 times) and the
least common element is H (occurring 3849876073 times); subtracting these produces 2188189693529.

Apply 40 steps of pair insertion to the polymer template and find the most and least common
elements in the result. What do you get if you take the quantity of the most common element
and subtract the quantity of the least common element?

Your puzzle answer was 2422444761283.

Both parts of this puzzle are complete! They provide two gold stars: **
'''

polymers = {}
polymer_pairs = {}
pairs_insertion = {}
first_line = True

with open('test_input_data.txt', 'r') as f:
    line = f.readline()
    while line:
        line = line.strip()

        if first_line:
            first_line = False
            # This is the initial polymer, separate in pairs
            for i in range(len(line)-1):
                pair = line[i:i+2]
                if pair not in polymer_pairs:
                    polymer_pairs[pair] = 0
                polymer_pairs[pair] += 1

            # Get the polymers in individual letters
            for p in line:
                if p not in polymers:
                    polymers[p] = 0
                polymers[p] += 1
        else:
            # insertion rules
            if line:
                pair, result = line.strip().split(" -> ")
                pairs_insertion[pair] = result
        line = f.readline()

def print_polymer(polymer):
    for p in polymer:
        for _ in range(polymer[p]):
            print(p, end="")
    print()


# steps_to_run = 10 # PART-1
steps_to_run = 40 # PART-2
# run steps
for _ in range(steps_to_run):
    polymers_update = {}
    for pair_insertion in pairs_insertion:

        if pair_insertion in polymer_pairs and polymer_pairs[pair_insertion] > 0:
            # pair exist in the polymer
            # add the result
            polymer_result = pairs_insertion[pair_insertion]

            # Generate the new 2 pairs to add in the polymer
            pair_1 = pair_insertion[0] + polymer_result
            pair_2 = polymer_result + pair_insertion[1]

            # do not update the pairs_insertion yet, do it after the step is over
            if pair_1 not in polymers_update:
                polymers_update[pair_1] = 0
            polymers_update[pair_1] += polymer_pairs[pair_insertion]

            if pair_2 not in polymers_update:
                polymers_update[pair_2] = 0
            polymers_update[pair_2] += polymer_pairs[pair_insertion]

            if pair_insertion not in polymers_update:
                polymers_update[pair_insertion] = 0
            polymers_update[pair_insertion] -= polymer_pairs[pair_insertion]

            # increase the counter per polymer letter
            # TODO have variables to detect the highest and lowest polymers here
            # no need to loop around this dict after the steps are over
            if polymer_result not in polymers:
                polymers[polymer_result] = 0
            polymers[polymer_result] += polymer_pairs[pair_insertion]

    # end of the step, update the polymer
    for polymer_update in polymers_update:
        if polymer_update not in polymer_pairs:
            polymer_pairs[polymer_update] = 0
        polymer_pairs[polymer_update] += polymers_update[polymer_update]

def get_polymer_info(polymer):
    highest_polymer = ''
    lowest_polymer = ''
    for p in polymer:
        if not highest_polymer or polymer[highest_polymer] < polymer[p]:
            highest_polymer = p
        if not lowest_polymer or polymer[lowest_polymer] > polymer[p]:
            lowest_polymer = p

    print(f"Higest Polymer {highest_polymer} with {polymer[highest_polymer]}")
    print(f"Lowest Polymer {lowest_polymer} with {polymer[lowest_polymer]}")
    print(f"diff {polymer[highest_polymer]-polymer[lowest_polymer]}")

get_polymer_info(polymers)
