import argparse
import logging
import sys
import time


def parse_input(input: list) -> list:
    return [int(x) for x in input[0].split('-')]

def check_validity(password: int) -> bool:
    password = str(password)
    has_double = False

    for i, char in enumerate(password):
        if i == 0:
            continue
        elif char < password[i-1]:
            return False
        elif char == password[i-1]:
            has_double = True

    return has_double


def check_validity_p2(password: int) -> bool:
    password = str(password)
    has_double = False
    has_closed_double = False

    for i, char in enumerate(password):
        if i == 0:
            continue
        elif char < password[i-1]:
            return False
        elif i > 1 and char == password[i-1] == password[i-2]:
            has_double = False
        elif char == password[i-1]:
            has_double = True
        elif has_double:
            has_closed_double = True

    return has_double or has_closed_double

def solve_1(input: list) -> str:
    restraints = parse_input(input)
    logging.debug(restraints)

    result = 0
    for i in range(restraints[0], restraints[1]):
        result += check_validity(i)

    return result


def solve_2(input: list) -> str:
    restraints = parse_input(input)

    result = 0
    for i in range(restraints[0], restraints[1]):
        result += check_validity_p2(i)

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
