import argparse
import logging
import re
import sys


def parse_input(input: list):
    puzzle_input = []

    ranges = input[0].split(",")

    for range in ranges:
        start, end = range.split("-")
        puzzle_input.append((int(start), int(end)))

    return puzzle_input

def expand_range(range_tuple):
    start, end = range_tuple
    return set(range(start, end + 1))

def check_validty(id: int) -> bool:
    str_id = str(id)
    half_1 = str_id[:len(str_id)//2]
    half_2 = str_id[len(str_id)//2:]

    if half_1 == half_2:
        # logging.debug(f"ID {id} is invalid: {half_1} == {half_2}")
        return False
    return True

def check_validty_regex(id: int) -> bool:
    pattern = r'^(.+)\1+$'
    if re.search(pattern, str(id)) is not None:
        # logging.debug(f"ID {id} is invalid: repeating pattern")
        return False
    return True

def solve_1(input: list) -> int:
    puzzle_input = parse_input(input)
    ids = set()

    for range in puzzle_input:
        expanded = expand_range(range)
        ids.update(expanded)

    result = 0
    for id in ids:
        if not check_validty(id):
            result += id

    return result

def solve_2(input: list) -> int:
    puzzle_input = parse_input(input)
    ids = set()

    for range in puzzle_input:
        expanded = expand_range(range)
        ids.update(expanded)

    result = 0
    for id in ids:
        if not check_validty_regex(id):
            result += id

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
