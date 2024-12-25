import argparse
import logging
import sys
import time

def parse_input(input: list) -> list:
    locks = []
    keys = []
    current = [-1, -1, -1, -1, -1]
    current_type = None

    for ln, line in enumerate(input):
        if len(line) == 0:
            if current_type == 'lock':
                locks.append(current)
            elif current_type == 'key':
                current = [x - 1 for x in current]
                keys.append(current)
            current = [-1, -1, -1, -1, -1]
        elif sum(current) < 0:
            current = [0, 0, 0, 0, 0]
            if line[0] == '#':
                current_type = 'lock'
            elif line[0] == '.':
                current_type = 'key'
            else:
                raise ValueError(f'Unexpected value at {line}')
        else:
            for i, char in enumerate(line):
                if char == '#':
                    current[i] += 1

    if current_type == 'lock':
        locks.append(current)
    elif current_type == 'key':
        current = [x - 1 for x in current]
        keys.append(current)

    return locks, keys

def match_lock_key(lock: list, key: list) -> bool:
    for i in range(0, 5):
        if lock[i] + key[i] > 5:
            # logging.debug(f"Lock {lock} and key {key}: overlap in the column {i}.")
            return False
    
    # logging.debug(f"Lock {lock} and key {key}: all columns fit.")
    return True


def solve_1(input: list) -> str:
    locks, keys = parse_input(input)
    result = 0
    for lock in locks:
        for key in keys:
            result += match_lock_key(lock, key)

    return result

def solve_2(input: list) -> str:
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
