import argparse
import logging
import sys
import time
from collections import defaultdict


def parse_input(input: list) -> list:
    secrets = list(map(int, input))
    return secrets


def mix(secret: int, value: int) -> int:
    return secret ^ value


def prune(value: int) -> int:
    return value % 16777216


def calculate_next_secret(secret: int) -> int:
    # multiply 64
    mul64 = secret * 64
    secret = mix(secret, mul64)
    secret = prune(secret)

    # divide 32
    div32 = secret // 32
    secret = mix(secret, div32)
    secret = prune(secret)

    # multiply 2048
    mul2048 = secret * 2048
    secret = mix(secret, mul2048)
    secret = prune(secret)

    return secret


def solve_1(input: list) -> str:
    secrets = parse_input(input)

    result = 0
    for secret in secrets:
        for _ in range(2000):
            secret = calculate_next_secret(secret)
        result += secret

    return result


def solve_2(input: list) -> str:
    secrets = parse_input(input)

    all_prices = defaultdict(int)
    for secret in secrets:
        changes = []
        prices = defaultdict(int)
        for _ in range(2000):
            old_price = secret % 10
            secret = calculate_next_secret(secret)
            new_price = secret % 10
            price_diff = new_price - old_price

            changes.append(price_diff)

            if len(changes) >= 4:
                sequence = tuple(changes[-4:])
                if sequence not in prices:
                    prices[sequence] = new_price

        for sequence, price in prices.items():
            all_prices[sequence] += price

    top = 0
    for sequence, price in all_prices.items():
        if price > top:
            top = price
            winning = sequence

    logging.debug(winning)
    logging.debug(top)

    return top


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
