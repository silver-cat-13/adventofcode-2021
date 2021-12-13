#!/usr/bin/env python

'''

'''

class TransparentPaper:
    def __init__(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y
        self.number_of_dots = 0
        self.dots = set()

    def mark_dot(self, x, y):
        self.dots.add((x,y))

    def mirror_point(self, p, side):
        # Get the mirror point during the folding based on the max
        max_to_use = self.max_y if side == 'y' else self.max_x
        if p == max_to_use:
            return 0
        return max_to_use - ((max_to_use + p) % max_to_use)

    def __str__(self):
        r = ''
        dots = set()
        for y in range(self.max_y+1):
            for x in range(self.max_x+1):
                dot = (x,y)
                if dot in self.dots:
                    dots.add(dot)
                    r += '#'
                else:
                    r += '.'

            r += '\n'
        if self.dots - dots:
            r += 'There are dots outside\n'
        return r


    def fold_along(self, pos, side):
        if side == 'x':
            half = self.max_x // 2 - 1
            max_to_use = self.max_x
        if side == 'y':
            half = self.max_y // 2 - 1
            max_to_use = self.max_y

        if pos > max_to_use:
            Exception(f"Cannot fold, given {pos} is bigger than size {max_to_use}")

        if half + 1 != pos:
            Exception(f"It is expected folding is always half")

        # fold the paper by decreasing size by half
        dots_to_add = []
        dots_to_remove = []
        for dot in self.dots:
            x, y = dot
            fold_side = y if side == 'y' else x
            if fold_side > half:
                # Dot is in the folding side

                # Get the mirror position
                mirror = self.mirror_point(fold_side, side)
                new_dot = (x, mirror) if side == 'y' else (mirror, y)

                # print(f"half {half} old {dot} new {new_dot}")

                # cannot increase the size of self.dots in the middle of the loop
                if not new_dot in self.dots:
                    dots_to_add.append(new_dot)

                # Dot is outside the folding side, it has to be removed
                # do not change the size in the middle of the loop
                dots_to_remove.append((x, y))

        # Update the dots set accordingly
        for dot in dots_to_add:
            self.dots.add(dot)

        for dot in dots_to_remove:
            self.dots.remove(dot)

        # Decrease the size of the paper
        if side == 'x':
            self.max_x = half
        if side == 'y':
            self.max_y = half


    def total_dots(self):
        return len(self.dots)


class FoldingInstruction:
    def __init__(self, side, pos):
        # side = x|y
        # pos = where the folding will take place
        self.side = side
        self.pos = pos

    def __str__(self):
        return f"{self.side}={self.pos}"

    def __repr__(self):
        return str(self)

max_x = float("-inf")
max_y = float("-inf")
all_dots = []
folding_instructions_part = False
folding_instructions = []
with open('input_data.txt', 'r') as f:
    line = f.readline()
    while line:
        line = line.strip()

        if not line:
            # we are in the folding instructions
            folding_instructions_part = True
        else:
            if not folding_instructions_part:
                x, y = line.split(',')
                x = int(x)
                y = int(y)
                all_dots.append((x, y))

                # Update the max X and Y value found
                if x > max_x:
                    max_x = x
                if y > max_y:
                    max_y = y
            else:
                # instruction is something like: fold along y=7
                # get the y=7 part
                side, pos = line[11:].split('=')
                pos = int(pos)
                folding_instructions.append(FoldingInstruction(side, pos))

        line = f.readline()

paper = TransparentPaper(max_x, max_y)
for dot in all_dots:
    paper.mark_dot(dot[0], dot[1])

for i, fold in enumerate(folding_instructions):
    paper.fold_along(fold.pos, fold.side)
    if i == 0:
        # This is the first fold
        print(f"After first fold there are {paper.total_dots()} dots")

print(paper)
