import argparse
import logging
import sys

from functools import reduce

def parse_input(input: list):
    ranges = []
    ingredients = []

    for line in input:
        if '-' in line:
            ranges.append((int(line.split('-')[0]), int(line.split('-')[1])))
        elif len(line) > 0:
            ingredients.append(int(line))

    return ranges, ingredients

def merge_ranges(ranges: list) -> list:
    def merge_step(merged, curr):
        if merged and merged[-1][1] >= curr[0]:
            last_start, last_end = merged[-1]
            return merged[:-1] + [(last_start, max(last_end, curr[1]))]
        return merged + [curr]
    
    merged_ranges = reduce(merge_step, sorted(ranges), [])
    return merged_ranges

def check_freshness(ingredient: int, ranges: list) -> bool:
    for range in ranges:
        if ingredient >= range[0] and ingredient <= range[1]:
            return True
        
    return False

def solve_1(input: list) -> int:
    ranges, ingredients = parse_input(input)

    ranges = merge_ranges(ranges)

    result = 0
    for ingredient in ingredients:
        result += int(check_freshness(ingredient, ranges))

    return result


def solve_2(input: list) -> int:
    ranges, ingredients = parse_input(input)

    ranges = merge_ranges(ranges)

    result = 0
    for range in ranges:
        result += range[1] - range[0] + 1

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
