#!/usr/bin/env python

'''
--- Part Two ---
Next, you should verify the life support rating, which can be determined by multiplying the
oxygen generator rating by the CO2 scrubber rating.

Both the oxygen generator rating and the CO2 scrubber rating are values that can be found in
your diagnostic report - finding them is the tricky part. Both values are located using a similar
process that involves filtering out values until only one remains. Before searching for either
rating value, start with the full list of binary numbers from your diagnostic report and consider
just the first bit of those numbers. Then:

Keep only numbers selected by the bit criteria for the type of rating value for which you are
searching. Discard numbers which do not match the bit criteria.

If you only have one number left, stop; this is the rating value for which you are searching.

Otherwise, repeat the process, considering the next bit to the right.

The bit criteria depends on which type of rating value you want to find:

To find oxygen generator rating, determine the most common value (0 or 1) in the current bit

position, and keep only numbers with that bit in that position. If 0 and 1 are equally common
, keep values with a 1 in the position being considered.

To find CO2 scrubber rating, determine the least common value (0 or 1) in the current bit position
, and keep only numbers with that bit in that position. If 0 and 1 are equally common, keep
values with a 0 in the position being considered.

For example, to determine the oxygen generator rating value using the same example diagnostic
report from above:

Start with all 12 numbers and consider only the first bit of each number. There are more 1
bits (7) than 0 bits (5), so keep only the 7 numbers with a 1 in the first position: 11110,
10110, 10111, 10101, 11100, 10000, and 11001.

Then, consider the second bit of the 7 remaining numbers: there are more 0 bits (4) than 1
bits (3), so keep only the 4 numbers with a 0 in the second position: 10110, 10111, 10101,
and 10000.

In the third position, three of the four numbers have a 1, so keep those three: 10110, 10111
, and 10101.

In the fourth position, two of the three numbers have a 1, so keep those two: 10110 and 10111.

In the fifth position, there are an equal number of 0 bits and 1 bits (one each). So, to find
the oxygen generator rating, keep the number with a 1 in that position: 10111.

As there is only one number left, stop; the oxygen generator rating is 10111, or 23 in decimal.

Then, to determine the CO2 scrubber rating value from the same example above:

Start again with all 12 numbers and consider only the first bit of each number. There are fewer
0 bits (5) than 1 bits (7), so keep only the 5 numbers with a 0 in the first position: 00100
, 01111, 00111, 00010, and 01010.

Then, consider the second bit of the 5 remaining numbers: there are fewer 1 bits (2) than 0
bits (3), so keep only the 2 numbers with a 1 in the second position: 01111 and 01010.

In the third position, there are an equal number of 0 bits and 1 bits (one each). So, to find
the CO2 scrubber rating, keep the number with a 0 in that position: 01010.

As there is only one number left, stop; the CO2 scrubber rating is 01010, or 10 in decimal.

Finally, to find the life support rating, multiply the oxygen generator rating (23) by the
CO2 scrubber rating (10) to get 230.


Use the binary numbers in your diagnostic report to calculate the oxygen generator rating and
CO2 scrubber rating, then multiply them together. What is the life support rating of the submarine
? (Be sure to represent your answer in decimal, not binary.)
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

lines                = []
total_1s_found       = 0
current_pos_to_count = 0

# Read the input data + get the total 1s in the first position
with open('input_data.txt', 'r') as f:
    line = f.readline()
    while line:

        if line[current_pos_to_count] == '1':
            total_1s_found += 1

        lines.append(line)
        line = f.readline()

# Utility class to manage O2 and CO2 rating
# Based on the input list and the amount of 1s, it is possible to know
# which elements of the inputs have to take for the rating.
#   For O2 rating keep the values with highest values
#   For CO2 rating, keep the values with lowest values
#
# Loop thoughtout the values and:
#   Take the next elements for the rating (based on the numner of 1s calculated)
#   Count the number of 1s for the next round
class Rating:
    def __init__(self, type, values, total_1s_found):
        '''
        Initialize the class variables
        '''

        # Indicate which bit we have to keep in the next round
        if type == 'o2':
            self.bit_to_keep_with_more_1s = '1'
            self.bit_to_keep_with_less_1s = '0'
        elif type == 'co2':
            self.bit_to_keep_with_more_1s = '0'
            self.bit_to_keep_with_less_1s = '1'
        else:
            Exception(f"Failure with type {type}")

        self.type                      = type
        self.values                    = values
        self.next_values_total         = 0
        self.next_values               = []
        self.total_1s_found_next_round = 0
        self.current_pos               = len(self.values) - 1
        self.current_pos_to_count      = 0

        self.more_1s  = True if total_1s_found >= len(self.values)/2 else False
        self.keep_bit = self.bit_to_keep_with_more_1s if self.more_1s else self.bit_to_keep_with_less_1s
        print(f"Starting {self.type} with already {total_1s_found} 1s "\
                f"over {len(self.values)}. Keeping {self.keep_bit}")

    def end_of_list(self):
        ''' Check if the round has finalized '''
        return self.current_pos == -1

    def is_final_value(self):
        ''' Check if we have the final value for the rating '''
        return len(self.values) == 1

    def get_rating(self):
        ''' Get the rating '''
        if not self.is_final_value():
            return None
        else:
            r_bin = self.values[0].strip()
            r_int = int(r_bin, 2)
            print(f"Getting {self.type} rating {r_bin}={r_int}")
            return r_int

    def wrap_up(self):
        ''' Function call only at the end of the round
        Get the next bit to keep based on the number of 1s calculated and reset variables
        '''
        if not self.end_of_list():
            return

        self.more_1s  = True if self.total_1s_found_next_round >= self.next_values_total/2 else False
        self.keep_bit = self.bit_to_keep_with_more_1s if self.more_1s else self.bit_to_keep_with_less_1s

        print(f"Wraping up {self.type} with {self.total_1s_found_next_round} 1s " \
                f"with {self.next_values_total} values, Value to keep={self.keep_bit}")

        self.current_pos_to_count      = (self.current_pos_to_count + 1) % 12
        self.values                    = self.next_values
        self.next_values               = []
        self.current_pos               = len(self.values) - 1
        self.next_values_total         = 0
        self.total_1s_found_next_round = 0

    def check_next_bit(self):
        ''' Check the next value in the round. If the bit is equal to the bit
        to keep, this value will be check in the next round. Store it in a list and
        increase counter if it is a  '1'
        '''
        if self.values[self.current_pos][self.current_pos_to_count] == self.keep_bit:
            self.next_values.append(self.values[self.current_pos])
            self.next_values_total += 1

            # Count 1 in the current position for the next position
            if self.values[self.current_pos][(self.current_pos_to_count+1)%12] == '1':
                self.total_1s_found_next_round += 1
        self.current_pos -= 1

o2_rating  = Rating('o2', lines, total_1s_found)
co2_rating = Rating('co2', lines.copy(), total_1s_found)

while True:
    if o2_rating.is_final_value() and co2_rating.is_final_value():
        # We are at the end of the list
        break

    if not o2_rating.is_final_value():
        if o2_rating.end_of_list():
            # Start again, get which element we have to remove
            o2_rating.wrap_up()

        o2_rating.check_next_bit()

    if not co2_rating.is_final_value():
        if co2_rating.end_of_list():
            # Start again, get which element we have to remove
            co2_rating.wrap_up()

        co2_rating.check_next_bit()

o2_rating_v = o2_rating.get_rating()
co2_rating_v = co2_rating.get_rating()
print(f"result={o2_rating_v*co2_rating_v}")
