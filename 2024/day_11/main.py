import argparse
import logging
import sys
import time

from collections import defaultdict


def parse_input(input: list) -> (list, list):
    stones = list(map(int, input[0].split(" ")))
    result = defaultdict(int)

    for stone in stones:
        result[stone] += 1

    return result

def blink(stone: int) -> tuple():
    if stone == 0:
        return (1,)
    elif len(str(stone)) % 2 == 0:
        half = len(str(stone)) // 2
        return (int(str(stone)[:half]), int(str(stone)[half:]))
    else:
        return (stone * 2024,)

def process_stones(stones: dict) -> dict:
    result = defaultdict(int)
    for stone, count in stones.items():
        resulting_stones = blink(stone)
        for resulting_stone in resulting_stones:
            result[resulting_stone] += count

    return result

def solve_1(input: list) -> int:
    stones = parse_input(input)
    # logging.debug(stones)

    steps = 25
    while steps > 0:
        stones = process_stones(stones)
        steps -= 1
        # logging.debug(stones)

    return sum(stones.values())


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
