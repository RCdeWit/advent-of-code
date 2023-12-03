import argparse
import logging
import sys

def pad_map(input: list):
    padding_line = "".join(["." for n in range(len(input[0]))]) + ".."
    padded_map = [padding_line]

    for line in input:
        line = "." + line + "."
        padded_map.append(line)

    padded_map.append(padding_line)

    # logging.debug(padded_map)

    return padded_map

def digit_with_adjacent_symbol(input_map: list, coordinate: list):
    ignored_chars = "0123456789."
    y, x = coordinate
    if input_map[y][x] not in "0123456789":
        return False
    elif input_map[y-1][x-1] not in ignored_chars:
        return True
    elif input_map[y-1][x] not in ignored_chars:
        return True
    elif input_map[y-1][x+1] not in ignored_chars:
        return True
    elif input_map[y][x-1] not in ignored_chars:
        return True
    elif input_map[y][x+1] not in ignored_chars:
        return True
    elif input_map[y+1][x-1] not in ignored_chars:
        return True
    elif input_map[y+1][x] not in ignored_chars:
        return True
    elif input_map[y+1][x+1] not in ignored_chars:
        return True
    else:
        return False

def mapped_engine_adjacencies(input_map: list):
    padded_map = pad_map(input_map)
    mapped_engine_adjacencies = []
    for x in range(1, len(padded_map[0])-1):
        row = []
        for y in range(1, len(padded_map)-1):
            row.append(digit_with_adjacent_symbol(padded_map, [x, y]))
        mapped_engine_adjacencies.append(row)
    
    return mapped_engine_adjacencies



def solve_1(input: list):
    adjacencies = mapped_engine_adjacencies(input)

    result = []
    for y, line in enumerate(input):
        part = ""
        has_adjaceny = False
        for x, char in enumerate(line):
            if char.isdigit():
                part += char
                has_adjaceny = max(adjacencies[y][x], has_adjaceny)
            else:
                if has_adjaceny:
                    result.append(int(part))
                part = ""
                has_adjaceny = False
        
        if has_adjaceny:
            result.append(int(part))

    return sum(result)


def solve_2(input: list):
    return


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