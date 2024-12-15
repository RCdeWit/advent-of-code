import argparse
import logging
import sys
import time


def parse_input(input: list, conversion_error: bool = False) -> (tuple, list, list, list):
    walls = []
    crates = []
    directions = []
    section = 1

    for y, line in enumerate(input):
        if len(line) == 0:
            section = 2
            continue
        elif section == 1:
            row = []
            for x, char in enumerate(line):
                if char == "#":
                    walls.append((x, y))
                elif char == "O":
                    crates.append((x, y))
                elif char == "@":
                    robot = (x, y)
        elif section == 2:
            for char in line:
                if char == "^":
                    directions.append("U")
                elif char == ">":
                    directions.append("R")
                elif char == "<":
                    directions.append("L")
                elif char == "v":
                    directions.append("D")
    
    return robot, walls, crates, directions

def get_object(location: tuple, crates: list, walls: list) -> str:
    x, y = location
    if location in crates:
        return "crate"
    elif location in walls:
        return "wall"
    else:
        return "empty"

def can_move(location: tuple, direction: str, crates: list, walls: list) -> bool:
    x, y = location
    offsets = {"U": (0, -1), "D": (0, 1), "L": (-1, 0), "R": (1, 0)}
    new_x = x + offsets[direction][0]
    new_y = y + offsets[direction][1]
    
    obj = get_object((new_x, new_y), crates, walls)
    if obj == "wall":
        return False
    elif obj == "crate":
        return can_move((new_x, new_y), direction, crates, walls)
    return True
    

def move_objects(location: tuple, direction: str, crates: list, walls: list):
    offsets = {"U": (0, -1), "D": (0, 1), "L": (-1, 0), "R": (1, 0)}
    x, y = location
    new_x = x + offsets[direction][0]
    new_y = y + offsets[direction][1]

    if get_object((new_x, new_y), crates, walls) == "crate":
        if not move_objects((new_x, new_y), direction, crates, walls):
            return False
    
    if can_move(location, direction, crates, walls):
        if location in crates:
            crates.remove(location)
            crates.append((new_x, new_y))
        return True
    return False

def move_robot(location: tuple, direction: str, crates: list, walls: list):
    if not can_move(location, direction, crates, walls):
        return location, crates

    offsets = {"U": (0, -1), "D": (0, 1), "L": (-1, 0), "R": (1, 0)}
    x, y = location
    new_x = x + offsets[direction][0]
    new_y = y + offsets[direction][1]

    if get_object((new_x, new_y), crates, walls) == "crate":
        if not move_objects((new_x, new_y), direction, crates, walls):
            return location, crates

    return (new_x, new_y), crates

def print_grid(robot: tuple, walls: list, crates: list) -> None:
    max_x = max(x for x, y in walls) + 1
    max_y = max(y for x, y in walls) + 1

    grid = [["." for _ in range(max_x)] for _ in range(max_y)]
    
    x, y = robot
    grid[y][x] = "@"
    for wall in walls:
        x, y = wall
        grid[y][x] = "#"
    for crate in crates:
        x, y = crate
        grid[y][x] = "O"

    for row in grid:
        print("".join(row))

    print("\n")

def calculate_gps_score(crate: tuple) -> int:
    x, y = crate
    return 100 * y + x

def solve_1(input: list) -> int:
    robot, walls, crates, directions = parse_input(input)
    
    for direction in directions:
        robot, crates = move_robot(robot, direction, crates, walls)
        # print_grid(robot, walls, crates)

    return sum(list(map(calculate_gps_score, crates)))

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