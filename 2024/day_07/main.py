import argparse
import logging
import sys
import time
from itertools import product


def parse_input(input: list):
    output = []
    for line in input:
        test_value, components = line.split(": ")
        test_value = int(test_value)
        components = list(map(int, components.split(" ")))
        output.append((test_value, components))

    # logging.debug(output)
    return output


def test_calculation(calculation: tuple(), include_concat: bool = False) -> bool:
    test_value, components = calculation

    # if sum(components) > test_value:
    #     return False

    def generate_permutations(n, include_concat=False):
        if include_concat:
            return [list(p) for p in product(["add", "mul", "con"], repeat=n)]
        else:
            return [list(p) for p in product(["add", "mul"], repeat=n)]

    num_calculations = len(components) - 1
    permutations = generate_permutations(num_calculations, include_concat)

    for series in permutations:
        temp_components = components.copy()
        result = temp_components.pop(0)

        while len(temp_components) > 0:
            current_component = temp_components.pop(0)
            current_operation = series.pop(0)

            if current_operation == "add":
                result += current_component
            elif current_operation == "mul":
                result *= current_component
            elif current_operation == "con":
                result = int(str(result) + str(current_component))

            if result > test_value:
                continue

        if result == test_value:
            # logging.debug(f"Found result for {calculation}: {series}" )
            return True

    # logging.debug(f"No solution for {calculation}" )
    return False


def solve_1(input: list) -> int:
    puzzle_input = parse_input(input)

    output = 0
    for line in puzzle_input:
        test_result = test_calculation((line), include_concat=False)
        if test_result:
            output += line[0]

    return output


def solve_2(input: list) -> int:
    puzzle_input = parse_input(input)

    output = 0
    for line in puzzle_input:
        test_result = test_calculation((line), include_concat=True)
        if test_result:
            output += line[0]

    return output


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
