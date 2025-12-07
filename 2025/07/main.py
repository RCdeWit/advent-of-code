import argparse
import logging
import sys

from collections import defaultdict

def parse_input(input: list):
    puzzle_input = defaultdict(str)

    for y, line in enumerate(input):
        for x, char in enumerate(line):
            if char != '.':
                puzzle_input[(x, y)] = char

            if char == 'S':
                start = (x, y)

    return puzzle_input, start

def continue_beam(puzzle_field, start, boundary = 15):
    x, y = start

    if puzzle_field[(x, y+1)] == '^':
        puzzle_field[(x, y+1)] = '*'
        return [(x-1, y+1), (x+1, y+1)]
    elif puzzle_field[(x, y+1)] == '*':
        return []
    elif y >= boundary:
        return []
    else:
        return [(x, y+1)]

def solve_1(input: list) -> int:
    result = 0
    puzzle_input, start = parse_input(input)

    queue = [start]

    while queue:
        position = queue.pop()
        new_positions = continue_beam(puzzle_input, position, len(input) - 1)

        if len(new_positions) == 2:
            result += 1

        queue += new_positions

        logging.debug(queue)

    return result

def solve_2(input: list) -> int:
    puzzle_input, start = parse_input(input)
    
    beam_count = defaultdict(int)
    beam_count[start] = 1
    result = 1
    
    for y in range(len(input) - 1):
        for x in range(len(input[0])):
            pos = (x, y)
            count = beam_count[pos]
            
            if count == 0:
                continue
            
            next_pos = (x, y + 1)
            next_val = puzzle_input[next_pos]
            
            if next_val == '^':
                result += count
                beam_count[(x - 1, y + 1)] += count
                beam_count[(x + 1, y + 1)] += count
            else:
                beam_count[next_pos] += count
    
    return result

if __name__ == "__main__":
    # Parse CLI arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--question", required=True)
    parser.add_argument("-i", "--input", required=False, default="input.txt")
    args = parser.parse_args()

    input_file = args.input
    question = args.question

    # Read input
    with open(input_file) as f:
        input = list(f.read().splitlines())

    # Set up logging
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    root.addHandler(handler)

    logging.info(f"Question {question} with input {input_file}")

    if question == "1":
        solution = solve_1(input)
        logging.info(f"Found solution: {solution}")
    elif question == "2":
        solution = solve_2(input)
        logging.info(f"Found solution: {solution}")
    else:
        logging.error("Select either question 1 or 2")
