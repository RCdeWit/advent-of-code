import argparse
import logging
import sys
import time


def parse_input(input: list) -> list:
    wires = []
    for line in input:
        wires.append(line.split(","))

    return wires

def convert_directions_to_coordinates(wire: list) -> set:
    coordinates = [(0, 0, 0)]
    for instruction in wire:
        direction = instruction[0]
        distance = int(instruction[1:])

        for _ in range(distance):
            if direction == "R":
                coordinates.append((coordinates[-1][0] + 1, coordinates[-1][1], coordinates[-1][2] + 1))
            elif direction == "L":
                    coordinates.append((coordinates[-1][0] - 1, coordinates[-1][1], coordinates[-1][2] + 1))
            elif direction == "D":
                    coordinates.append((coordinates[-1][0], coordinates[-1][1] + 1, coordinates[-1][2] + 1))
            elif direction == "U":
                    coordinates.append((coordinates[-1][0], coordinates[-1][1] - 1, coordinates[-1][2] + 1))

    return set(coordinates)

def solve_1(input: list) -> str:
    wires = parse_input(input)
    intersections = convert_directions_to_coordinates(wires[0]) & convert_directions_to_coordinates(wires[1])
    intersections.remove((0, 0, 0))
    
    lowest = min(abs(x) + abs(y) for (x, y, d) in intersections)
    return lowest


def solve_2(input: list) -> str:
    wires = parse_input(input)

    wire_1 = {(x, y): d for x, y, d in convert_directions_to_coordinates(wires[0])}
    wire_2 = {(x, y): d for x, y, d in convert_directions_to_coordinates(wires[1])}

    wire_1.pop((0, 0))
    wire_2.pop((0, 0))

    intersections = set(wire_1.keys()) & set(wire_2.keys())
    result = [(x, y, wire_1[(x, y)] + wire_2[(x, y)]) for x, y in intersections]

    return min(result, key=lambda x: x[2])[2]

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
