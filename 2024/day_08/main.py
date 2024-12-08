import argparse
import itertools
import logging
import sys
import time

from collections import defaultdict

def parse_input(input: list) -> (list, defaultdict):
    antennas = defaultdict(list)
    grid = []

    for y, row in enumerate(input):
        y_values = []
        for x, char in enumerate(row):
            y_values.append(char)
            if char.isalnum():
                antennas[char].append((x, y))
        grid.append(y_values)

    return grid, dict(antennas)

def find_antinodes(coordinates: list, grid_size: tuple, harmonics: bool = False) -> list:
    combinations = list(itertools.combinations(coordinates, 2))
    max_x, max_y = grid_size
    max_x -= 1
    max_y -= 1

    antinodes = defaultdict(bool)
    for antenna in coordinates:
        antinodes[antenna] = True

    for combination in combinations:
        node_1, node_2 = combination
        nx1, ny1 = node_1
        nx2, ny2 = node_2

        dx = nx2 - nx1
        dy = ny2 - ny1

        dx_original = dx
        dy_original = dy

        # logging.debug(f"COMBINATION: {combination}")

        while -max_x <= dx <= max_x and -max_y <= dy <= max_y:
            antinode_1x = nx1 - dx
            antinode_1y = ny1 - dy

            antinode_2x = nx2 + dx
            antinode_2y = ny2 + dy

            # logging.debug(f"DELTA: {(dx, dy)}")
            # logging.debug(f"Checking {(antinode_1x, antinode_1y)} and {(antinode_2x, antinode_2y)}")

            if 0 <= antinode_1x <= max_x and 0 <= antinode_1y <= max_y:
                antinodes[(antinode_1x, antinode_1y)] = True
                # logging.debug(f"Found antinode at {(antinode_1x, antinode_1y)}")

            if 0 <= antinode_2x <= max_x and 0 <= antinode_2y <= max_y:
                antinodes[(antinode_2x, antinode_2y)] = True
                # logging.debug(f"Found antinode at {(antinode_2x, antinode_2y)}")

            if not harmonics:
                break

            dx += dx_original
            dy += dy_original

    return antinodes

def solve_1(input: list) -> int:
    grid, antennas = parse_input(input)
    grid_size = (len(grid[0]), len(grid))
    result = defaultdict(bool)
    for antenna_type in antennas.keys():
        antinodes = find_antinodes(antennas[antenna_type], grid_size)

        result = result | antinodes

    # logging.debug(antinodes)
    return len(result)


def solve_2(input: list) -> int:
    grid, antennas = parse_input(input)
    grid_size = (len(grid[0]), len(grid))
    result = defaultdict(bool)
    for antenna_type in antennas.keys():
        antinodes = find_antinodes(antennas[antenna_type], grid_size, True)

        result = result | antinodes

    # logging.debug(antinodes)
    return len(result)


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