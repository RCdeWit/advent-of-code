import argparse
import logging
import sys
import time

def parse_input(puzzle_input: list, width: int, height: int) -> list:
    layers = []
    layer = []
    row = []
    row_num = 0
    for i, char in enumerate(puzzle_input):
        if i % width == 0 and i != 0:
            layer.append(row)
            row = []
            row_num += 1
            if row_num % height == 0:
                layers.append(layer)
                layer = []

        row.append(int(char))

    layer.append(row)
    layers.append(layer)

    return layers

def compress_image(layers: list) -> list:
    image = layers[0].copy()

    for layer in layers:
        for y, row in enumerate(layer):
            for x, char in enumerate(row):
                if image[y][x] == 2:
                    image[y][x] = char


    return image

def print_image(image: list) -> None:
    for row in image:
        line = ''
        for char in row:
            if char == 0:
                line += ' '
            else:
                line += '#'
        print(line)

def solve_1(puzzle_input: list) -> str:
    layers = parse_input(puzzle_input[0], 25, 6)

    fewest_0 = {0: float('inf'), 1: 0, 2: 0}
    for layer in layers:
        counts = {0: 0, 1: 0, 2: 0}

        for row in layer:
            for char in row:
                counts[char] += 1

        if counts[0] < fewest_0[0]:
            fewest_0 = counts

    return fewest_0[1] * fewest_0[2]


def solve_2(puzzle_input: list) -> str:
    layers = parse_input(puzzle_input[0], 25, 6)
    image = compress_image(layers)
    print_image(image)



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
        puzzle_input = list(f.read().splitlines())

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
        solution = solve_1(puzzle_input)
        logging.info(f"Found solution: {solution} (in {time.time()-start} seconds)")
    elif question == "2":
        solution = solve_2(puzzle_input)
        logging.info(f"Found solution: {solution} (in {time.time()-start} seconds)")
    else:
        logging.error("Select either question 1 or 2")
