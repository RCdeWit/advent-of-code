import argparse
import logging
import sys

from functools import reduce
from operator import mul

def parse_input(input: list):
    puzzle_input = []
    operations = []

    for y, line in enumerate(input):
        line = line.split(' ')
        row = []

        for item in line:
            if item in ('', ' '):
                pass
            elif item in ('*', '+'):
                operations.append(item)
            else:
                row.append(int(item))

        if len(row) > 0:
            puzzle_input.append(row)
    
    return puzzle_input, operations

def parse_input_2(input: list):
    puzzle_input = []
    operations = []

    for y, line in enumerate(input):
        if y == len(input)-1:
            operations = [char for char in line if char in ('+', '*')]
        else:
            row = []
            for char in line:
                row.append(char)
            puzzle_input.append(row)
    
    # logging.debug(puzzle_input)
    # logging.debug(operations)

    parsed_groups = []
    components = []
    for x in range(len(puzzle_input[0])):
        column = ''
        for y in range(len(puzzle_input)):
            char = puzzle_input[y][x]
            if char in ('1234567890'):
                column += char

        logging.debug(column)
        if len(column) > 0:
            components.append(int(column))
        else:
            parsed_groups.append(components)
            components = []

    parsed_groups.append(components)

    logging.debug(parsed_groups)
    logging.debug(operations)

    return parsed_groups, operations


def solve_1(input: list) -> int:
    result = 0
    puzzle_input, operations = parse_input(input)

    for x in range(len(operations)):
        components = []

        for y in range(len(puzzle_input)):
            components.append(puzzle_input[y][x])

        if operations[x] == '+':
            outcome = sum(components)
            logging.debug(f"Sum of {components} == {outcome}")
        elif operations[x] == '*':
            outcome = reduce(mul, components, 1)
            logging.debug(f"Multiplication of {components} == {outcome}")

        result += outcome
    
    return result

def solve_2(input: list) -> int:
    result = 0
    puzzle_input, operations = parse_input_2(input)

    for x, components in enumerate(puzzle_input):
        if operations[x] == '+':
            outcome = sum(components)
            logging.debug(f"Sum of {components} == {outcome}")
        elif operations[x] == '*':
            outcome = reduce(mul, components, 1)
            logging.debug(f"Multiplication of {components} == {outcome}")

        result += outcome
    
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
