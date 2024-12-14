import argparse
import logging
import sys
import time


def parse_input(input: list, conversion_error: bool = False) -> (list, list):
    result = []
    for line in input:
        px = int(line.split("p=")[1].split(",")[0])
        py = int(line.split("p=")[1].split(",")[1].split(" ")[0])
        vx = int(line.split("v=")[1].split(",")[0])
        vy = int(line.split("v=")[1].split(",")[1])

        result.append((px, py, vx, vy))

    return result

def calculate_movement(robot: tuple, grid_size: tuple, steps: int = 100):
    px, py, vx, vy = robot
    movement_x = vx * steps
    movement_y = vy * steps

    max_x, max_y = grid_size

    px += movement_x
    py += movement_y

    px = px % max_x
    py = py % max_y

    return (px, py)

def count_robots_per_quadrant(robots: list, grid_size: tuple) -> tuple:
    q1 = 0
    q2 = 0
    q3 = 0
    q4 = 0

    max_x, max_y = grid_size
    half_x = max_x // 2
    half_y = max_y // 2

    for robot in robots:
        x, y = robot
        if x < half_x and y < half_y:
            q1 += 1
        elif x > half_x and y < half_y:
            q2 += 1
        elif x < half_x and y > half_y:
            q3 += 1
        elif x > half_x and y > half_y:
            q4 += 1

    return (q1, q2, q3, q4)


def solve_1(input: list) -> int:
    robots = parse_input(input)
    # logging.debug(robots)
    # grid_size = (101, 103)
    grid_size = (101, 103)
    robots = list(map(lambda robot: calculate_movement(robot, grid_size), robots))

    quadrants = count_robots_per_quadrant(robots, grid_size)

    result = 1
    for q in quadrants:
        result *= q
    
    return result

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