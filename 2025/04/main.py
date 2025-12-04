import argparse
from collections import defaultdict
import logging
import sys


def parse_input(input: list):
    puzzle_input = defaultdict(str)

    for y, line in enumerate(input):
        for x, char in enumerate(line):
            # puzzle_input.append((x, y, char))
            puzzle_input[(x, y)] = char if char == "@" else ""

    return puzzle_input

def find_adjacent_rolls(map: dict, position: tuple) -> int:
    current_x, current_y = position
    result = 0
    for y in range(current_y - 1, current_y + 2):
        for x in range(current_x - 1, current_x + 2):
            if (x, y) != position and map.get((x, y)) == "@":
                result += 1
    return result

def solve_1(input: list) -> int:
    puzzle_input = parse_input(input)
    result = 0

    for position, value in puzzle_input.items():
        if value == "@":
            surrounding = find_adjacent_rolls(puzzle_input, position)
            if surrounding < 4:
                result += 1

    return result


def solve_2(input: list) -> int:
    puzzle_input = parse_input(input)
    result = 0

    while True:
        result_thus_far = result
        for position, value in puzzle_input.items():
            if value == "@":
                surrounding = find_adjacent_rolls(puzzle_input, position)
                if surrounding < 4:
                    result += 1
                    puzzle_input[(position)] = ""

        if result_thus_far == result:
            break

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
