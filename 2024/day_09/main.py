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

def parse_input_2(input: list) -> list:
    input = input[0]
    result = []

    file_id = 0
    for i, value in enumerate(input):
        if i % 2 == 0:
            result.append((file_id, int(value)))
            file_id += 1
        else:
            result.append((None, int(value)))
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

def print_blocks(blocks: list):
    result = ""
    for block in blocks:
        for _ in range(block[1]):
            if block[0] is None:
                result += "."
            else:
                result += str(block[0])
    print(result)

def flatten_blocks(blocks: list) -> list:
    i = 0
    while i < len(blocks) - 1:
        if blocks[i][0] == blocks[i + 1][0]:  # Check if the value is the same
            # Merge counts
            merged_count = blocks[i][1] + blocks[i + 1][1]
            # Replace current tuple with the merged one
            blocks[i] = (blocks[i][0], merged_count)
            # Remove the next tuple
            blocks.pop(i + 1)
        else:
            i += 1  # Only increment if no merge happened

    return blocks

def compact_file_2(blocks: list) -> list:
    queue = reversed(blocks.copy())

    # print_blocks(blocks)

    for q in queue:
        if q[0] is None:
            continue
        # logging.debug(q)
        value = q[0]
        required_length = q[1]
        for i, available in enumerate(blocks):
            if available[0] is None and available[1] >= required_length:
                remaining_space = available[1] - required_length
                blocks.pop(i)
                blocks.insert(i, (value, required_length))
                if remaining_space > 0:
                    blocks.insert(i+1, (None, remaining_space))
                for j in range(len(blocks) - 1, -1, -1):  # Iterate in reverse
                    if blocks[j] == q:
                        blocks[j] = (None, required_length)
                        break
                break
        # print_blocks(blocks)
        flatten_blocks(blocks)

    return blocks


def calculate_checksum(blocks: list) -> int:
    result = 0
    for i, value in enumerate(blocks):
        block_sum = i * value
        # logging.debug(f"Adding {i} * {value} = {block_sum}")
        result += block_sum
    return result

def calculate_checksum_2(blocks: list) -> int:
    result = 0
    i = 0
    for block in blocks:
        if block[0] is None:
            i += block[1]
            continue
        else:
            for _ in range(block[1]):
                result += (i * block[0])
                i += 1
    return result

def solve_1(input: list) -> int:
    blocks = parse_input(input)
    # logging.debug(blocks)

    compacted = compact_file(blocks)
    # logging.debug(compacted)

    result = calculate_checksum(compacted)
    return result

def solve_2(input: list) -> int:
    blocks = parse_input_2(input)
    # logging.debug(blocks)

    compacted = compact_file_2(blocks)
    # logging.debug(compacted)

    result = calculate_checksum_2(compacted)
    return result


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