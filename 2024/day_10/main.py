import argparse
import logging
import sys
import time


def parse_input(input: list) -> (list, list):
    grid = []
    trail_heads = []
    for y, line in enumerate(input):
        row = []
        for x, char in enumerate(line):
            if char == ".":
                char = -1
            row.append(int(char))
            if char == "0":
                trail_heads.append((x, y))
        grid.append(row)

    return grid, trail_heads


def get_valid_neighbours(grid: list, coordinate: tuple) -> list:
    x, y = coordinate
    current_height = grid[y][x]
    neighbours = []

    offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for offset in offsets:
        new_x, new_y = x + offset[0], y + offset[1]
        if 0 <= new_x < len(grid[0]) and 0 <= new_y < len(grid):
            if grid[new_y][new_x] == current_height + 1:
                neighbours.append((new_x, new_y))

    return neighbours


def find_paths(grid: list, trail_head: tuple) -> list:
    paths = [[trail_head]]
    current_height = 0
    while current_height < 9:
        temp_paths = []
        for path in paths:
            neighbours = get_valid_neighbours(grid, path[-1])
            if len(neighbours) >= 1:
                for neighbour in neighbours:
                    temp_paths.append(path + [neighbour])

        paths = temp_paths
        current_height += 1

    # logging.debug(paths)
    return paths


def calculate_trail_score(paths: list) -> int:
    unique_peaks = []
    for path in paths:
        if path[-1] not in unique_peaks:
            unique_peaks.append(path[-1])

    return len(unique_peaks)


def solve_1(input: list) -> int:
    grid, trail_heads = parse_input(input)
    result = 0
    for trail_head in trail_heads:
        paths = find_paths(grid, trail_head)
        trail_score = calculate_trail_score(paths)
        result += trail_score

    return result


def solve_2(input: list) -> int:
    grid, trail_heads = parse_input(input)
    result = 0
    for trail_head in trail_heads:
        paths = find_paths(grid, trail_head)
        # trail_score = calculate_trail_score(paths)
        result += len(paths)

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
