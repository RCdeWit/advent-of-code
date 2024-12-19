import argparse
import logging
import sys
import time

from collections import deque


def parse_input(input: list) -> (list, list):
    towels = input[0].split(", ")

    patterns = []

    for line in input[2:]:
        patterns.append(line)

    return towels, patterns

def parse_pattern(pattern: str, towels: list) -> list:
    pattern_length = len(pattern)
    matches = [False] * (pattern_length + 1)
    matches[0] = True  # Empty pattern always works
    
    # Store which towel was used to reach each position
    prev_towel = [None] * (pattern_length + 1)
    
    # For each position in the pattern
    for i in range(pattern_length):
        if matches[i]:
            for towel in towels:
                end = i + len(towel)
                if end <= pattern_length and pattern[i:end] == towel:
                    matches[end] = True
                    prev_towel[end] = (i, towel)
    
    if not matches[pattern_length]:
        return None
    
    # Reconstruct solution
    result = []
    pos = pattern_length
    while pos > 0:
        prev_pos, towel = prev_towel[pos]
        result.append(towel)
        pos = prev_pos
    
    return result[::-1]


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
    pass

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
