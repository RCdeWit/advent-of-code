import argparse
import logging
import math
import sys

from collections import defaultdict
from itertools import combinations

def parse_input(input: list):
    boxes = []

    for line in input:
        boxes.append(tuple(map(int, line.split(','))))

    return boxes

def calculate_distance(box_1: tuple, box_2: tuple) -> int:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(box_1, box_2, strict=True)))

def calculate_all_distances(boxes: list) -> list:
    distances = [(box1, box2, calculate_distance(box1, box2)) for box1, box2 in combinations(boxes, 2)]
    return sorted(distances, key=lambda x: x[2])

def find_circuits(connections, boxes, n=3):
    circuits = []
    seen = set()
    
    for box in boxes:  # Iterate through ALL boxes, not just connections keys
        if box not in seen:
            circuit = frozenset(connections[box] + [box])
            circuits.append(circuit)
            seen.update(circuit)
    
    logging.debug(f"Total circuits: {len(circuits)}")
    return sorted(circuits, key=len, reverse=True)[:n]

def solve_1(input: list) -> int:
    result = 0
    boxes = parse_input(input)

    # logging.debug(boxes)

    distances = calculate_all_distances(boxes)
    # logging.debug(distances)

    connections = defaultdict(list)

    remaining_connections = 1000
    while remaining_connections > 0:
        possible_connection = distances.pop(0)
        box1, box2, distance = possible_connection

        circuit1 = frozenset(connections[box1] + [box1])
        circuit2 = frozenset(connections[box2] + [box2])
        
        if circuit1 != circuit2:
            merged = list(circuit1 | circuit2)
            
            for box in merged:
                connections[box] = [b for b in merged if b != box]
            
            logging.debug(f"Connected {box1} and {box2}, circuit sizes now: {len(circuit1)}, {len(circuit2)} -> {len(merged)}")
        else:
            logging.debug(f"Skipped {box1} and {box2} - already in same circuit")
        
        remaining_connections -= 1

    largest_circuits = find_circuits(connections, boxes, 3)
    logging.debug(largest_circuits)

    result = 1
    for c in largest_circuits:
        logging.debug(f"Circuit length: {len(c)}")
        result *= len(c)

    return result

def solve_2(input: list) -> int:
    result = 0
    boxes = parse_input(input)

    # logging.debug(boxes)

    distances = calculate_all_distances(boxes)
    # logging.debug(distances)

    connections = defaultdict(list)

    while True:
        possible_connection = distances.pop(0)
        box1, box2, distance = possible_connection

        circuit1 = frozenset(connections[box1] + [box1])
        circuit2 = frozenset(connections[box2] + [box2])
        
        if circuit1 != circuit2:
            merged = list(circuit1 | circuit2)
            
            for box in merged:
                connections[box] = [b for b in merged if b != box]
            
            logging.debug(f"Connected {box1} and {box2}, circuit sizes now: {len(circuit1)}, {len(circuit2)} -> {len(merged)}")
        else:
            logging.debug(f"Skipped {box1} and {box2} - already in same circuit")


        if len(merged) == len(input):
            return box1[0] * box2[0]
        

    largest_circuits = find_circuits(connections, boxes, 3)
    logging.debug(largest_circuits)

    result = 1
    for c in largest_circuits:
        logging.debug(f"Circuit length: {len(c)}")
        result *= len(c)

    return result

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
