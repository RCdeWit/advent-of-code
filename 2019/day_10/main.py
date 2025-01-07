import argparse
import logging
import math
import sys
import time

def parse_input(puzzle_input: list) -> list:
    asteroids = []
    for y, line in enumerate(puzzle_input):
        for x, char in enumerate(line):
            if char == "#":
                asteroids.append((x, y))

    return asteroids

def find_lines_of_sight(asteroids: list, base: tuple) -> list:
    base_x, base_y = base
    result = []
    for asteroid in asteroids:
        if asteroid == base:
            continue

        view = True
        ast_x, ast_y = asteroid
        for obstacle in asteroids:
            if obstacle == asteroid or obstacle == base:
                continue

            obs_x, obs_y = obstacle
            cross_product = (obs_y - base_y) * (ast_x - base_x) - (ast_y - base_y) * (obs_x - base_x)
            if (
                cross_product == 0 and 
                min(base_x, ast_x) <= obs_x <= max(base_x, ast_x) and 
                min(base_y, ast_y) <= obs_y <= max(base_y, ast_y)
            ):
                # Obstacles interferes with base and asteroid
                view = False
                break

        if view:
            result.append(asteroid)

    return result

def vaporize_asteroids(asteroids: list, base: tuple) -> list:
    base_x, base_y = base

    def generate_clockwise_aims(grid: list, base: tuple) -> list:
        base_x, base_y = base
        points = []

        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if (x, y) != base:  # Exclude the base itself
                    # Calculate angle relative to "north" (positive y-axis)
                    angle = (math.atan2(x - base_x, base_y - y) + 2 * math.pi) % (2 * math.pi)
                    points.append(((x, y), angle))

        # Sort points by angle in clockwise order starting from north
        clockwise_aims = [point for point, _ in sorted(points, key=lambda item: item[1])]
        return clockwise_aims

    clockwise_aims = generate_clockwise_aims(puzzle_input, base)


    lines_of_sight = {}
    for step in clockwise_aims:
        obstacles = {}
        ast_x, ast_y = step

        for obstacle in asteroids:
            if obstacle == base:
                continue

            obs_x, obs_y = obstacle
            cross_product = (obs_y - base_y) * (ast_x - base_x) - (ast_y - base_y) * (obs_x - base_x)
            if (
                cross_product == 0 and 
                min(base_x, ast_x) <= obs_x <= max(base_x, ast_x) and 
                min(base_y, ast_y) <= obs_y <= max(base_y, ast_y)
            ):
                # Obstacles interferes with base and asteroid
                obstacles[obstacle] = ((obs_x - base_x) ** 2 + (obs_y - base_y) ** 2) ** 0.5

        lines_of_sight[step] = [k for k, v in sorted(obstacles.items(), key=lambda item: item[1])]
    # logging.debug(lines_of_sight)

    vaporized_count = 0
    step = 0
    vaped_asteroids = []
    while vaporized_count < 200:
        aim = clockwise_aims[step]
        if aim in lines_of_sight and len(lines_of_sight[aim]) > 0:
            vaped = lines_of_sight[aim].pop(0)
            if vaped not in vaped_asteroids:
                vaped_asteroids.append(vaped)
                logging.debug(f"Vaporized {vaporized_count+1}: {vaped} with aim {aim} (step {step})")
                vaporized_count += 1

        if all(len(asteroids) == 0 for asteroids in lines_of_sight.values()):
            break

        step = (step + 1) % len(clockwise_aims)

    return vaped_asteroids
        


def solve_1(puzzle_input: list) -> str:
    asteroids = parse_input(puzzle_input)
    
    high_score = 0
    for asteroid in asteroids:
        score = len(find_lines_of_sight(asteroids, asteroid))
        if score > high_score:
            high_score = score
            winner = asteroid

    logging.debug(f"Winner: {winner}")
    return high_score


def solve_2(puzzle_input: list) -> str:
    asteroids = parse_input(puzzle_input)
    # # base = (8, 16)
    # base = (11, 13)

    high_score = 0
    for asteroid in asteroids:
        score = len(find_lines_of_sight(asteroids, asteroid))
        if score > high_score:
            high_score = score
            base = asteroid

    vaporized = vaporize_asteroids(asteroids, base)
    result_x, result_y = vaporized[-1]
    return result_x * 100 + result_y

    # return high_score



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
