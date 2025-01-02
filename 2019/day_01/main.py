import argparse
import logging
import sys
import time


def parse_input(input: list) -> list:
    modules = [int(module) for module in input]
    return modules


def calculate_fuel(module: int) -> int:
    return module // 3 - 2


def solve_1(input: list) -> str:
    modules = parse_input(input)
    fuels = [calculate_fuel(module) for module in modules]
    return sum(fuels)


def solve_2(input: list) -> str:
    modules = parse_input(input)
    fuels = []
    for module in modules:
        fuel = calculate_fuel(module)
        while fuel > 0:
            fuels.append(fuel)
            fuel = calculate_fuel(fuel)
    return sum(fuels)


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
