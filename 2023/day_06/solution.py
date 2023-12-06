import argparse
import logging
import sys

def parse_input(input: list):
    time = [int(x) for x in input[0].split(" ")[1:] if x]
    distance = [int(x) for x in input[1].split(" ")[1:] if x]

    for i, t in enumerate(time):
        yield (t, distance[i])

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


def solve_1(input):
    races = list(parse_input(input))
    result = 1
    for race in races:
        ways_to_win = calculate_ways_to_win(race[0], race[1])
        result = result * ways_to_win
    return result

def solve_2(input):
    return

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