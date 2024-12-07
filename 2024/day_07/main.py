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

def test_calculation(calculation: tuple()) -> bool:
    test_value, components = calculation

    # if sum(components) > test_value:
    #     return False

    def generate_permutations(n):
        return [list(p) for p in product(["add", "mul"], repeat=n)]

    num_calculations = len(components) - 1
    permutations = generate_permutations(num_calculations)

    for series in permutations:
        result = components[0]
        current_component = 1
        for operation in series:
            if operation == "add":
                result += components[current_component]
            elif operation == "mul":
                result *= components[current_component]
            current_component += 1
            if result > test_value:
                continue

        if result == test_value:
            logging.debug(f"Found result for {calculation}: {series}" )
            return True
    
    logging.debug(f"No solution for {calculation}" )
    return False

def solve_1(input: list) -> int:
    puzzle_input = parse_input(input)

    output = 0
    for line in puzzle_input:
        test_result = test_calculation((line))
        if test_result:
            output += line[0]

    return output


def solve_2(input: list) -> int:
    pass


if __name__ == '__main__':
     # Parse CLI arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--question", required=True)
    parser.add_argument("-i", "--input", required=False, default='input.txt')
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

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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