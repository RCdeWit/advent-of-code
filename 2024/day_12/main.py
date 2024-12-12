import argparse
import logging
import sys
import time

from collections import defaultdict
from itertools import product

def parse_input(input: list) -> (list, list):
    grid = []
    coordinates = defaultdict(str)
    for y, line in enumerate(input):
        row = []
        for x, char in enumerate(line):
            row.append(char)
            coordinates[(x, y)] = char
        grid.append(row)

    return grid, coordinates

def find_valid_neighbours(grid: list, current: tuple) -> (set, int):
    x, y = current
    neighbours = []
    fences = 0
    candidates = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]

    for candidate in candidates:
        new_x, new_y = candidate

        # Out of bounds
        if new_x < 0 or new_x >= len(grid[0]) or new_y < 0 or new_y >= len(grid):
            fences += 1
            continue

        if grid[y][x] == grid[new_y][new_x]:
            neighbours.append((new_x, new_y))
        else:
            fences += 1

    # logging.debug(f"Finding neighbours for {current}: {neighbours}")
    return set(neighbours), fences

def find_regions(grid: list) -> list:
    global_queue = set(product(range(len(grid[0])), range(len(grid))))
    visited = set()
    regions = []

    while len(global_queue) > 0:
        current = global_queue.pop()
        region = []
        perimeter = 0
        region_queue = set([current])
        while len(region_queue) > 0:
            current = region_queue.pop()
            visited.update([current])
            region.append(current)
            neighbours, fences = find_valid_neighbours(grid, current)
            perimeter += fences
            neighbours = neighbours - visited
            if len(neighbours) == 0:
                continue
            else:
                region_queue.update(neighbours)

        crop = grid[current[1]][current[0]]
        regions.append({'crop': crop, 'perimeter': perimeter, 'plots': region})
        global_queue = global_queue - visited

    return regions

def calculate_fence_price(region: dict) -> int:
    return region['perimeter'] * len(region['plots'])

def solve_1(input: list) -> int:
    grid, coordinates = parse_input(input)
    regions = find_regions(grid)

    # for region in regions:
    #     logging.debug(f"Region {region['crop']} with perimeter {region['perimeter']}: {region['plots']}")

    total_price = sum([calculate_fence_price(region) for region in regions])
    return total_price

def solve_2(input: list) -> int:
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
