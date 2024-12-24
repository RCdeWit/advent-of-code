import argparse
import logging
import sys
import time
from collections import defaultdict, deque
from copy import deepcopy

from itertools import permutations


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

def set_wires(x: int, y: int) -> dict:
    # Max int = 2 ** 45 = 35184372088832 - 1
    x = format(x, '#047b')
    y = format(y, '#047b')

    wires = {}
    for i in range(45):
        index = str(i).zfill(2)
        wires['x' + index] = x[i+2]
        wires['y' + index] = y[i+2]

    return wires

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

def solve_addition(wires: dict, graph: dict) -> int:
    graph = deepcopy(graph)
    wires = deepcopy(wires)
    while graph:
        current = graph.pop(0)
        wire = current['wire']
        components = current['components']
        input0 = wires[components[0]]
        operation = components[1]
        input1 = wires[components[2]]

        wires[wire] = get_value(int(input0), int(input1), operation)

    wires = dict(sorted(wires.items()))

    result = ""
    for w, value in wires.items():
        if w.startswith('z'):
            # logging.debug(f"Key {w}: {value}")
            result = str(value) + result

    return int(result, 2)

def find_wrong_bits(graph: dict) -> None:
    mismatches = []
    for i in range(45):
        wires = set_wires(0, 0)
        wires['x' + str(i).zfill(2)] = '1'
        wires['y' + str(i).zfill(2)] = '1'

        output = solve_addition(wires, graph)
        output = format(output, '#047b')

        if str(output)[46-i] != '0' and str(output)[45-i] not in ('1', 'b'):

            # logging.debug(f"{output} - wrong bit at {i}")
            mismatches.append(i)

    return mismatches


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
    wires, combinations = parse_input(input)
    dependency_graph = build_dependency_graph(wires, combinations)

    logging.debug(find_wrong_bits(dependency_graph))

    # These should be XOR but aren't
    z_swaps = {
        'z07': ('x07', 'AND', 'y07'),
        'z13': ('skt', 'OR', 'wpp'),
        'z31': ('kqk', 'AND', 'djr'),
        # 'z45': ('hsd', 'OR', 'sng'),
    }

    candidate_swaps = {}
    for combination in combinations.items():
        key, value = combination
        if value[1] == 'XOR' and not key.startswith('z'):
            # candidate_swaps[key] = value
            candidate_swaps[key] = value

    logging.debug(find_wrong_bits(dependency_graph))

    new_combinations = deepcopy(combinations)

    result = []

    new_combinations['z13'] = candidate_swaps['pqc']
    new_combinations['pqc'] = z_swaps['z13']
    dependency_graph = build_dependency_graph(wires, new_combinations)
    logging.debug(find_wrong_bits(dependency_graph))
    result.extend(['z13', 'pqc'])

    new_combinations['z31'] = candidate_swaps['bgs']
    new_combinations['bgs'] = z_swaps['z31']
    dependency_graph = build_dependency_graph(wires, new_combinations)
    logging.debug(find_wrong_bits(dependency_graph))
    result.extend(['z31', 'bgs'])

    new_combinations['swt'] = z_swaps['z07']
    new_combinations['z07'] = candidate_swaps['swt']
    dependency_graph = build_dependency_graph(wires, new_combinations)
    logging.debug(find_wrong_bits(dependency_graph))
    result.extend(['swt', 's07'])

    new_combinations['wsv'] = combinations['rjm']
    new_combinations['rjm'] = combinations['wsv']
    dependency_graph = build_dependency_graph(wires, new_combinations)
    logging.debug(find_wrong_bits(dependency_graph))
    result.extend(['wsv', 'rjm'])

    input1 = 35184372088831
    input2 = 0
    wires = set_wires(input1, input2)

    assert solve_addition(wires, dependency_graph) == input1 + input2
    return ",".join(sorted(result))


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
