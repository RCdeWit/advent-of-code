import argparse
import logging
import sys
import math

def parse_input(input: list):
    directions = input[0]

    nodes = {}

    for line in input[2:]:
        line = "".join([char for char in line if char not in " ()"])
        start, destinations = line.split("=")
        left, right = destinations.split(",")

        nodes[start] = (left, right)

    return directions, nodes

def traverse_nodes(nodes: dict, start: str, directions: str):
    i = 0
    while start != "ZZZ":
        direction = directions[i % len(directions)]
        if direction == "L":
            destination = nodes[start][0]
        elif direction == "R":
            destination = nodes[start][1]
        start = destination
        i += 1

    return i

def traverse_nodes_2(nodes: dict, start: str, directions: str):
    i = 0
    while start[-1] != "Z":
        direction = directions[i % len(directions)]
        if direction == "L":
            destination = nodes[start][0]
        elif direction == "R":
            destination = nodes[start][1]
        start = destination
        i += 1

    return i

def solve_1(input):
    directions, nodes = parse_input(input)
    solution = traverse_nodes(nodes, "AAA", directions)
    return solution

def solve_2(input):
    directions, nodes = parse_input(input)

    steps_per_loop = []
    for key in nodes:
        logging.debug(key)
        if key[-1] == "A":
            length_loop = traverse_nodes_2(nodes, key, directions)
            steps_per_loop.append(length_loop)

    lcm = math.lcm(*steps_per_loop)
    return lcm

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