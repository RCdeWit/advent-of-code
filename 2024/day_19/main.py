import argparse
import logging
import sys
import time

from collections import defaultdict


def parse_input(input: list) -> (list, list):
    towels = input[0].split(", ")

    patterns = []

    for line in input[2:]:
        patterns.append(line)

    return towels, patterns

def count_paths_to_pattern(pattern: str, towels: list) -> int:
    subpatterns = defaultdict(int)
    subpatterns[""] = 1
    
    for i in range(len(pattern)):
        prefix = pattern[:i]
        for towel in towels:
            new_prefix = prefix + towel
            if pattern.startswith(new_prefix):
                subpatterns[new_prefix] += subpatterns[prefix]
    
    return subpatterns[pattern]

def solve_1(input: list) -> str:
    towels, patterns = parse_input(input)
    # logging.debug(towels)
    # logging.debug(patterns)

    count = 0
    for pattern in patterns:
        sequence = parse_pattern(pattern, towels)
        logging.debug(f"Pattern {pattern} possible with: {sequence}")

        if sequence is not None:
            count += 1

    return count

    

def solve_2(input: list) -> int:
    towels, patterns = parse_input(input)
    result = 0
    for i, pattern in enumerate(patterns):
        paths = count_paths_to_pattern(pattern, towels)
        # logging.debug(f"Found {paths} paths to pattern {i} ({pattern}) \n")
        result += paths

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
    start = time.time()

    if question == "1":
        solution = solve_1(input)
        logging.info(f"Found solution: {solution} (in {time.time()-start} seconds)")
    elif question == "2":
        solution = solve_2(input)
        logging.info(f"Found solution: {solution} (in {time.time()-start} seconds)")
    else:
        logging.error("Select either question 1 or 2")
