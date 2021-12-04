#!/usr/bin/env python

'''
--- Day 4: Giant Squid ---
You're already almost 1.5km (almost a mile) below the surface of the ocean, already so deep
that you can't see any sunlight. What you can see, however, is a giant squid that has attached
itself to the outside of your submarine.

Maybe it wants to play bingo?

Bingo is played on a set of boards each consisting of a 5x5 grid of numbers. Numbers are chosen
at random, and the chosen number is marked on all boards on which it appears. (Numbers may
not appear on all boards.) If all numbers in any row or any column of a board are marked, that
board wins. (Diagonals don't count.)

The submarine has a bingo subsystem to help passengers (currently, you and the giant squid)
pass the time. It automatically generates a random order in which to draw numbers and a random
set of boards (your puzzle input). For example:

7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
After the first five numbers are drawn (7, 4, 9, 5, and 11), there are no winners, but the
boards are marked as follows (shown here adjacent to each other to save space):

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
After the next six numbers are drawn (17, 23, 2, 0, 14, and 21), there are still no winners:

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
Finally, 24 is drawn:

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
At this point, the third board wins because it has at least one complete row or column of marked
numbers (in this case, the entire top row is marked: 14 21 17 24 4).

The score of the winning board can now be calculated. Start by finding the sum of all unmarked
numbers on that board; in this case, the sum is 188. Then, multiply that sum by the number
that was just called when the board won, 24, to get the final score, 188 * 24 = 4512.

To guarantee victory against the giant squid, figure out which board will win first. What will
your final score be if you choose that board?

 --- Part Two ---
On the other hand, it might be wise to try a different strategy: let the giant squid win.

You aren't sure how many bingo boards a giant squid could play at once, so rather than waste
time counting its arms, the safe thing to do is to figure out which board will win last and choose that one. That way, no matter which boards it picks, it will win for sure.

In the above example, the second board is the last to win, which happens after 13 is eventually
called and its middle column is completely marked. If you were to keep playing until this point
, the second board would have a sum of unmarked numbers equal to 148 for a final score of 148
* 13 = 1924.

Figure out which board will win last. Once it wins, what would its final score be?

'''

import sys

if len(sys.argv) == 2:
    part = sys.argv[1]
    if part == '1' or part == '2':
        print(f"Running part {part}")
    else:
        Exception("Argument can either be 1 or 2")
else:
    Exception("Pass argument 1 or 2")

class Board:
    WINNING_ROW = ['x']*5
    def __init__(self):
        self.board = []
        self.match_per_column = [0]*5
        self.winning_board = False

    def append_row(self, row):
        self.board.append(row.split())

    def draw_number(self, number):
        if self.winning_board:
            # Board is not playing
            return False
        for col_i, row in enumerate(self.board):
            if number in row:
                row_i = row.index(number)
                row[row_i] = 'x'

                if row == Board.WINNING_ROW:
                    # This is a winning board
                    self.winning_board = True
                    if part == '1':
                        # part 1 is to find the 1st winner, print here only in part 1
                        print(f"{self} is a winning board")
                    return True

                self.match_per_column[row_i] += 1
                if self.match_per_column[row_i] == 5:
                    # This is a winning board
                    self.winning_board = True
                    if part == '1':
                        # part 1 is to find the 1st winner, print here only in part 1
                        print(f"{self} is a winning board")
                    return True
        return False

    def calculate_unmatch_numbers(self):
        result = 0
        for row in self.board:
            for v in row:
                if v != 'x':
                    result += int(v)
        return result

    def __str__(self):
        s = ''
        for r in self.board:
            s += ' '.join(r)
            s += '\n'
        return s

boards = []

# Read all the boards and the draws numbers
with open('input_data.txt', 'r') as f:
    line = f.readline()
    first_line = True
    next_board = False

    board = Board()

    while line:

        if first_line:
            # Read the draws numbers
            first_line = False
            draws_numbers = line
        else:
            if line == '\n':
                # End of a board
                boards.append(board)
                board = Board()
            else:
                board.append_row(line)

        line = f.readline()

# Add last board
boards.append(board)

win = False
winning_draw = 0
unmatched_sum = 0
winning_board = None

for draw in draws_numbers.split(','):
    for board in boards:
        if board.draw_number(draw):
            win = True
            winning_board = board
            winning_draw = int(draw)
            unmatched_sum = board.calculate_unmatch_numbers()

            if part == '1' and win:
                break

    if part == '1' and win:
        break

if part == '2':
    print(f"winning board {winning_board}")

print(f"result={winning_draw}x{unmatched_sum}={winning_draw*unmatched_sum}")
