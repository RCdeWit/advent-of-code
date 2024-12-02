import argparse
import logging
import sys

def parse_input(input: list):
    for line in input:
        yield list(map(int, line.split(" ")))

def check_report_safety(report: list[int]):
    if report[1] > report[0]:
        direction = "increasing"
    else:
        direction = "decreasing"

    for level, value in enumerate(report):
        if level == 0:
            continue
        
        if direction == "increasing" and value < report[level-1]:
            return False
        elif direction == "decreasing" and value > report[level-1]:
            return False
        else:
            distance = abs(value - report[level-1])
            if distance < 1 or distance > 3:
                return False

    # logging.info("Found safe report")
    return True
            
def solve_1(input: list) -> int:
    reports = map(check_report_safety, parse_input(input))
    result = sum(reports)

    return result


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

    if question == "1":
        solution = solve_1(input)
        logging.info(f"Found solution: {solution}")
    elif question == "2":
        solution = solve_2(input)
        logging.info(f"Found solution: {solution}")
    else:
        logging.error("Select either question 1 or 2")