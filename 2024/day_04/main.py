import argparse
import logging
import sys

def parse_input(input: list):
    grid = []
    for line in input:
        row = []
        for char in line:
            row.append(char)
        grid.append(row)
    return grid

def find_x(grid: list) -> list:
    results = []
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char == 'X':
                results.append((x, y))

    return results

def find_viable_directions(grid: list, coordinates: tuple) -> list:
    x, y = coordinates
    max_y = len(grid) - 1
    max_x = len(grid[0]) - 1

    directions = {"nw": (-1, -1), "n": (0, -1), "ne": (1, -1),
                  "w": (-1, 0), "e": (1, 0),
                  "sw": (-1, 1), "s": (0, 1), "se": (1, 1)}

    if x < 3:
        directions.pop("nw", None)
        directions.pop("w", None)
        directions.pop("sw", None)
    if x > max_x - 3:
        directions.pop("ne", None)
        directions.pop("e", None)
        directions.pop("se", None)
    if y < 3:
        directions.pop("nw", None)
        directions.pop("n", None)
        directions.pop("ne", None)
    if y > max_y - 3:
        directions.pop("sw", None)
        directions.pop("s", None)
        directions.pop("se", None)

    return directions

def count_xmas_from_x(grid: list, coordinates: tuple) -> int:
    viable_directions = find_viable_directions(grid, coordinates)
    x, y = coordinates
    count = 0

    for direction in viable_directions.values():
        dx, dy = direction

        if grid[y + dy][x + dx] == 'M' \
            and grid[y + 2*dy][x + 2*dx] == 'A' \
            and grid[y + 3*dy][x + 3*dx] == 'S':
            count += 1
            logging.debug(f"Found XMAS for {direction} from x={x}, y={y}")

    return count

def solve_1(input: list) -> int:
    grid = parse_input(input)
    x_coordinates = find_x(grid)

    result = sum(map(lambda x: count_xmas_from_x(grid, x), x_coordinates))
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