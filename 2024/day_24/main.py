import argparse
import logging
import sys
import time
from collections import defaultdict, deque


def parse_input(input: list) -> list:
    initials = {}
    combinations = {}

    section = 0
    for line in input:
        if len(line) == 0:
            section = 1
        elif section == 0:
            wire, value = line.split(": ")
            initials[wire] = int(value)
        elif section == 1:
            wire_1, operation, wire_2, _, output = line.split(" ")
            combinations[output] = (wire_1, operation, wire_2)

    return initials, combinations

def build_dependency_graph(wires: dict, combinations: dict) -> dict:
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    
    for output, inputs in combinations.items():
        inputs = [inputs[0], inputs[2]]
        for node in inputs:
            graph[node].append(output)
            in_degree[output] += 1
    
    queue = deque(wires.keys())
    sorted_order = []
    
    # Topological sort
    while queue:
        current = queue.popleft()
        sorted_order.append(current)
        
        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Return sorted combinations in calculation order
    sorted_combinations = [{'wire': node, 'components': combinations[node]} for node in sorted_order if node in combinations]
    return sorted_combinations

def get_value(wire_1: int, wire_2: int, operation: str) -> int:
    if operation == "AND":
        return int(wire_1 == wire_2 == 1)
    elif operation == "OR":
        return int(wire_1 == 1 or wire_2 == 1)
    elif operation == "XOR":
        return int(wire_1 != wire_2)

def solve_1(input: list) -> str:
    wires, combinations = parse_input(input)
    # logging.debug(initials)
    # logging.debug(combinations)
    dependency_graph = build_dependency_graph(wires, combinations)
    logging.debug(dependency_graph)

    while dependency_graph:
        current = dependency_graph.pop(0)
        wire = current['wire']
        components = current['components']

        logging.debug(wire)
        logging.debug(components)

        input0 = wires[components[0]]
        operation = components[1]
        input1 = wires[components[2]]

        wires[wire] = get_value(input0, input1, operation)

    wires = dict(sorted(wires.items()))

    result = ""
    for w, value in wires.items():
        if w.startswith('z'):
            logging.debug(f"Key {w}: {value}")
            result = str(value) + result

    return int(result, 2)
            





def solve_2(input: list) -> str:
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
