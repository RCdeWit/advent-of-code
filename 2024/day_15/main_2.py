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
            for x, char in enumerate(line):
                if char == "#":
                    walls.append((x*2, y))
                    walls.append((x*2+1, y))
                elif char == "O":
                    crates.append(((x*2, y), (x*2+1, y)))
                elif char == "@":
                    robot = (x*2, y)
        elif section == 2:
            for char in line:
                if char == "^":
                    directions.append((0, -1))
                elif char == ">":
                    directions.append((1, 0))
                elif char == "<":
                    directions.append((-1, 0))
                elif char == "v":
                    directions.append((0, 1))
    
    return robot, walls, crates, directions

def get_object(location: tuple, crates: list, walls: list) -> str:
    x, y = location
    for crate in crates:
        (x1, y1), (x2, y2) = crate
        if y1 == y2 == y and x1 <= x <= x2:  # Check horizontal crate range
            return "crate"
    if location in walls:
        return "wall"
    return "empty"

def get_affected_objects(current: tuple, direction: tuple, crates: list, walls: list):
    affected = set()  # Use a set to avoid duplicates
    queue = [current]  # Initialize a queue with the current position

    dx, dy = direction

    while queue:
        pos = queue.pop(0)
        # logging.debug(f"POSITION {pos} pushing {direction}")
        x, y = pos
        new_x = x + dx
        new_y = y + dy

        # Check for walls at the current position
        if (new_x, new_y) in walls:
            return None

        # Check for crates that overlap the position
        for crate in crates:
            if (new_x, new_y) in crate:  # If the current position is part of the crate
                # logging.debug(f"CRATE {crate} collides")
                if crate not in affected:  # If we haven't processed this crate yet
                    affected.add(crate)  # Add it to affected
                    for coord in crate:
                        x, y = coord
                        queue.append((x, y))

    # logging.debug(f"AFFECTED: {list(affected)}")
    return list(affected)

def move_robot(robot: tuple, direction: tuple, crates: list, walls: list) -> (list, list):
    x, y = robot
    dx, dy = direction
    new_x = x + dx
    new_y = y + dy

    if get_object((new_x, new_y), crates, walls) == "empty":
        # logging.debug("Move into empty")
        return ((new_x, new_y), crates)
    elif get_object((new_x, new_y), crates, walls) == "wall":
        return (robot, crates)

    affected_objects = get_affected_objects(robot, direction, crates, walls)
    # logging.debug(f"AFFECTED: {affected_objects}")
    if affected_objects is None:
        return (robot, crates)

    # Everything can move, so let's move
    original_crates = [x for x in crates if x not in affected_objects]
    new_crates = []
    for obj in affected_objects:
        new_crates.append(tuple((x + dx, y + dy) for x, y in obj))

    # logging.debug(f"OG: {original_crates}")
    # logging.debug(f"NEW: {new_crates}")
    crates = original_crates + new_crates
    return ((new_x, new_y), crates)
    
def print_grid(robot: tuple, walls: list, crates: list) -> None:
    max_x = max(x for x, y in walls) + 1
    max_y = max(y for x, y in walls) + 1

    grid = [["." for _ in range(max_x)] for _ in range(max_y)]
    for x, y in walls:
        grid[y][x] = "#"
    for (x1, y1), (x2, y2) in crates:
        grid[y1][x1] = "["
        grid[y2][x2] = "]"

    x, y = robot
    grid[y][x] = "@"

    for row in grid:
        print("".join(row))

    print("\n")

def calculate_gps_score(crate: tuple) -> int:
    x, y = crate[0]
    return 100 * y + x

def solve_2(input: list) -> int:
    robot, walls, crates, directions = parse_input(input)
    # print_grid(robot, walls, crates)
    
    for i, direction in enumerate(directions):
        # logging.debug(f"BEFORE {i} ({direction}): {crates}")
        robot, crates = move_robot(robot, direction, crates, walls)
        # logging.debug(f"AFTER {i} ({direction}): {crates}")
    
    print_grid(robot, walls, crates)

    return sum(list(map(calculate_gps_score, crates)))

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
        logging.error("Run main.py instead")
    elif question == "2":
        solution = solve_2(input)
        logging.info(f"Found solution: {solution} (in {time.time()-start} seconds)")
    else:
        logging.error("Select either question 1 or 2")