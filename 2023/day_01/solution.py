import argparse
import logging
import sys

def solve_1(input):
    digits_only = []
    for line in input:
        digits_only.append(''.join(char for char in line if char in "0123456789"))
    logging.debug(digits_only)

    calibrations = [int(line[0]+line[-1]) for line in digits_only]
    logging.debug(calibrations)

    result = sum(calibrations)
    return result

def solve_2(input):
    digits_only = []
    for line in input:
        digits_only.append(list(parse_digits(line)))
    logging.debug(digits_only)

    calibrations = [int(line[0]+line[-1]) for line in digits_only]
    logging.debug(calibrations)

    result = sum(calibrations)
    return result

def parse_digits(line: str):
    if len(line) == 0:
        return

    elif line.startswith("1") or line.startswith("one"):
        yield "1"
    elif line.startswith("2") or line.startswith("two"):
        yield "2"
    elif line.startswith("3") or line.startswith("three"):
        yield "3"
    elif line.startswith("4") or line.startswith("four"):
        yield "4"
    elif line.startswith("5") or line.startswith("five"):
        yield "5"
    elif line.startswith("6") or line.startswith("six"):
        yield "6"
    elif line.startswith("7") or line.startswith("seven"):
        yield "7"
    elif line.startswith("8") or line.startswith("eight"):
        yield "8"
    elif line.startswith("9") or line.startswith("nine"):
        yield "9"

    yield from parse_digits(line[1:])


if __name__ == '__main__':
     # Parse CLI arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--question", required=True)
    parser.add_argument("-i", "--input", required=False)
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

    if question == "1":
        solution = solve_1(input)
        logging.info(f"Found solution: {solution}")
    elif question == "2":
        solution = solve_2(input)
        logging.info(f"Found solution: {solution}")
    else:
        logging.error("Select either question 1 or 2")