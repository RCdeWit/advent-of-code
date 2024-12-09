import argparse
import logging
import sys
import time

def parse_input(input: list) -> list:
    input = input[0]
    result = []

    file_id = 0
    for i, value in enumerate(input):
        if i % 2 == 0:
            for _ in range(int(value)):
                result.append(file_id)
            file_id += 1
        else:
            for _ in range(int(value)):
                result.append(None)
    return result

def compact_file(blocks: list) -> list:
    result = []
    while len(blocks) > 0:
        block = blocks.pop(0)
        if block is None:
            last_block = blocks.pop()
            while last_block is None:
                last_block = blocks.pop()
            result.append(last_block)
        else:
            result.append(block)
    return result

def calculate_checksum(blocks: list) -> int:
    result = 0
    for i, value in enumerate(blocks):
        block_sum = i * value
        # logging.debug(f"Adding {i} * {value} = {block_sum}")
        result += block_sum
    return result

def solve_1(input: list) -> int:
    blocks = parse_input(input)
    # logging.debug(blocks)

    compacted = compact_file(blocks)
    # logging.debug(compacted)

    result = calculate_checksum(compacted)
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
    start = time.time()

    if question == "1":
        solution = solve_1(input)
        logging.info(f"Found solution: {solution} (in {time.time()-start} seconds)")
    elif question == "2":
        solution = solve_2(input)
        logging.info(f"Found solution: {solution} (in {time.time()-start} seconds)")
    else:
        logging.error("Select either question 1 or 2")