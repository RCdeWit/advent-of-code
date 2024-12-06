import argparse
import logging
import sys

def parse_input(input: list):
    grid = []
    for y, line in enumerate(input):
        x = []
        for char in line:
            if char in ".#":
                x.append(char)
            else:
                x.append("U")
                position_guard = (len(x)-1, y)
        grid.append(x)
    return grid, position_guard

def check_out_of_bounds(grid: list, position: tuple) -> bool:
    x, y = position
    direction = grid[y][x]
    if x + 1 >= len(grid[0]) and direction == "R":
        return True
    elif x - 1 < 0 and direction == "L":
        return True
    elif y + 1 >= len(grid) and direction == "D":
        return True
    elif y - 1 < 0 and direction == "U":
        return True
    
    return False

def move_guard(grid: list, position: tuple) -> (list, tuple):
    x, y = position
    direction = grid[y][x]

    if check_out_of_bounds(grid, position):
        logging.debug(f"Guard walks out of bounds (x={x}, y={y}, dir={direction})")
        grid[y][x] = "."
        return grid, (None, None)

    logging.debug(f"Guard is at x={x}, y={y}, dir={direction}")
    
    if direction == "U":
        if grid[y-1][x] == "#":
            direction = "R"
            grid[y][x] = direction
            return grid, (x, y)
        else:
            grid[y][x] = "."
            grid[y-1][x] = direction
            return grid, (x, y-1)
    elif direction == "R":
        if grid[y][x+1] == "#":
            direction = "D"
            grid[y][x] = direction
            return grid, (x, y)
        else:
            grid[y][x] = "."
            grid[y][x+1] = direction
            return grid, (x+1, y)
    elif direction == "D":
        if grid[y+1][x] == "#":
            direction = "L"
            grid[y][x] = direction
            return grid, (x, y)
        else:
            grid[y][x] = "."
            grid[y+1][x] = direction
            return grid, (x, y+1)
    elif direction == "L":
        if grid[y][x-1] == "#":
            direction = "U"
            grid[y][x] = direction
            return grid, (x, y)
        else:
            grid[y][x] = "."
            grid[y][x-1] = direction
            return grid, (x-1, y)

def solve_1(input: list) -> int:
    grid, position = parse_input(input)

    out_of_bounds = False
    steps = 0
    visited = {}
    visited[position] = True

    while not out_of_bounds:
        grid, position = move_guard(grid, position)
        steps += 1
        if position[0] is None:
            out_of_bounds = True
        else:
            visited[position] = True

    return len(visited)


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