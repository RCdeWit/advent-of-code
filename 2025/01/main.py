import argparse
import logging
import sys


def parse_input(input: list):
    puzzle_input = []

    for line in input:
        direction = line[0]
        distance = int(line[1:])
        puzzle_input.append([direction, distance])

    return puzzle_input

def find_new_position(current_position, direction, distance):
    if direction == "L":
        current_position -= distance
    else:
        current_position += distance

    while current_position < 0:
        current_position += 100

    current_position = current_position % 100

    return current_position

def find_new_position_2(current_position, direction, distance):
    clicks = 0

    if direction == "L":
        for _ in range(distance):
            current_position -= 1
            if current_position < 0:
                current_position = 99
            if current_position == 0:
                clicks += 1
    else:
        for _ in range(distance):
            current_position += 1
            if current_position > 99:
                current_position = 0
            if current_position == 0:
                clicks += 1

    return current_position, clicks

def solve_1(input: list) -> int:
    puzzle_input = parse_input(input)
    current_position = 50

    result = 0

    for move in puzzle_input:
        direction, distance = move
        current_position = find_new_position(current_position, direction, distance)

        if current_position == 0:
            result += 1

    return result


def solve_2(input: list) -> int:
    puzzle_input = parse_input(input)
    current_position = 50

    result = 0

    for move in puzzle_input:
        direction, distance = move
        current_position, clicks = find_new_position_2(current_position, direction, distance)

        result += clicks

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
