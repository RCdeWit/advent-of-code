import argparse
import logging
import sys


def parse_input(input: list):
    time = [int(x) for x in input[0].split(" ")[1:] if x]
    distance = [int(x) for x in input[1].split(" ")[1:] if x]

    for i, t in enumerate(time):
        yield (t, distance[i])


def parse_input_2(input: list):
    time = int(input[0].split(":")[1].replace(" ", ""))
    distance = int(input[1].split(":")[1].replace(" ", ""))
    return (time, distance)


def calculate_distance(total_time: int, button_held: int):
    travel_time = total_time - button_held
    distance = travel_time * button_held
    return distance


def calculate_ways_to_win(total_time: int, target: int):
    ways_to_win = 0
    for i in range(total_time):
        distance = calculate_distance(total_time, i)
        if distance > target:
            ways_to_win += 1

    return ways_to_win


def calculate_boundary(total_time: int, target: int, search_start: int, direction: str):
    if direction == "left":
        boundary = int(search_start / 2)
    else:
        boundary = int(search_start + (search_start / 2))

    if calculate_distance(total_time, boundary) > target:
        return calculate_boundary(total_time, target, boundary, direction)
    else:
        if direction == "left":
            for i in range(boundary, search_start):
                # logging.debug(f"Try: {i}")
                if calculate_distance(total_time, i) > target:
                    # logging.debug(f"Found {direction} boundary: {i}")
                    return i
        else:
            for i in range(search_start, boundary):
                # logging.debug(f"Try: {i}")
                if calculate_distance(total_time, i) < target:
                    # logging.debug(f"Found {direction} boundary: {i-1}")
                    return i - 1


def solve_1(input):
    races = list(parse_input(input))
    result = 1
    for race in races:
        ways_to_win = calculate_ways_to_win(race[0], race[1])
        result = result * ways_to_win
    return result


def solve_2(input):
    race = parse_input_2(input)
    left_boundary = calculate_boundary(race[0], race[1], race[0] / 2, "left")
    right_boundary = calculate_boundary(race[0], race[1], race[0] / 2, "right")
    return right_boundary - left_boundary + 1


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

    if question == "1":
        solution = solve_1(input)
        logging.info(f"Found solution: {solution}")
    elif question == "2":
        solution = solve_2(input)
        logging.info(f"Found solution: {solution}")
    else:
        logging.error("Select either question 1 or 2")
