#!/usr/bin/env python

'''

'''

SYNTAX_SCORE_MAPPING = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}
CLOSING_CHUNK_MAPPING = {
    ')': '(',
    ']': '[',
    '}': '{',
    '>': '<'
}
AUTOCOMPLETE_SCORE_MAPPING = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4
}
OPENING_CHUNKS = '([{<'
syntax_score = 0

# Set as a list and later can be sort.
# TODO update this structure to a binary tree where the root is the middle
# or two heap, one with the min and one with the max values for better performance
# too lazy to do that right now, gotta get the start
autocomplete_scores = []

with open('input_data.txt', 'r') as f:
    line = f.readline()
    while line:
        line = line.strip()

        syntax_queue = []

        for char in line:
            if char in OPENING_CHUNKS:
                # This is an opening chunk
                syntax_queue.append(char)
            else:
                # This is a closing chunk, it should match the last
                # opening
                # assume the charavter is one of the closing chars
                if len(syntax_queue) == 0:
                    # queue empty? consider this a corruption state
                    syntax_score += SYNTAX_SCORE_MAPPING[char]
                elif syntax_queue[-1] != CLOSING_CHUNK_MAPPING[char]:
                    # corruption, the last element does not match the closing chunk
                    syntax_score += SYNTAX_SCORE_MAPPING[char]

                    # empty the queue, no need for this other than get incomplete lines later
                    syntax_queue = []
                    break
                else:
                    # valid closing chunk, remove element from the queue
                    syntax_queue.pop()

        if len(syntax_queue) > 0:
            autocomplete_score = 0
            while syntax_queue:
                char = syntax_queue.pop()
                autocomplete_score *= 5
                autocomplete_score += AUTOCOMPLETE_SCORE_MAPPING[char]

            autocomplete_scores.append(autocomplete_score)

        line = f.readline()

# TODO use binary tree or heaps for better performance,
autocomplete_scores.sort()
autocomplete_score = autocomplete_scores[int(len(autocomplete_scores)/2)]

print(f"Answer part 1: {syntax_score}")
print(f"Answer for part 2: {autocomplete_score}")
