import argparse
import logging
import re
import sys


def parse_input(input: list):
    pattern = r"mul\(\d{1,3},\d{1,3}\)"

    calculations = []
    for line in input:
        calculations += re.findall(pattern, line)

    # logging.debug(calculations)
    return calculations


def split_do_dont(program: list) -> str:
    # Add explicit do at start
    program = "do()" + "".join(program)
    # Split on don't so start of all segments have 1 don't max
    program = program.split("don't()")
    # Remove all don'ts that are not followed by do
    program = [x for x in program if "do()" in x]
    # Remove all don't substrings at start, retain everything after do
    program = [x.split("do()", 1)[1] for x in program]

    return "".join(program)


def execute_calculation(calculation: str) -> int:
    instruction = calculation.split("(")[0]
    param_1 = calculation.split("(")[1].split(",")[0]
    param_2 = calculation.split("(")[1].split(",")[1].split(")")[0]

    if instruction == "mul":
        return int(param_1) * int(param_2)


def solve_1(input: list) -> int:
    calculations = parse_input(input)
    return sum(map(execute_calculation, calculations))


def solve_2(input: list) -> int:
    dont_removed = [split_do_dont(input)]
    calculations = parse_input(dont_removed)
    # logging.debug(calculations)
    return sum(map(execute_calculation, calculations))


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
