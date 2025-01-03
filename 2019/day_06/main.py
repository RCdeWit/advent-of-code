import argparse
import logging
import sys
import time

from collections import defaultdict

def parse_input(puzzle_input: list) -> list:
    output = []
    for line in puzzle_input:
        output.append(tuple(line.split(')')))
        if line.startswith('COM'):
            start = tuple(line.split(')'))
        elif line.endswith('YOU'):
            you = tuple(line.split(')'))
        elif line.endswith('SAN'):
            santa = tuple(line.split(')'))

    return output, start, you, santa

def count_indirect_orbits(orbits: list, start: tuple) -> list:
    counts = defaultdict(int)

    com, start = start
    counts[com] = 0
    counts[start] = 1

    queue = orbits.copy()
    queue.remove((com, start))

    while queue:
        for orbit in queue:
            if orbit[0] in counts.keys():
                counts[orbit[1]] += counts[orbit[0]] + 1
                queue.remove(orbit)

    return counts

def find_path_to_start(orbits: list, start: tuple, destination: tuple):
    path = []
    path.append(destination[1])
    path.append(destination[0])
    current = destination[0]
    while True:
        for orbit in orbits:
            if orbit[1] == current:
                current = orbit[0]
                path.append(current)
        if current == start[0]:
            return list(reversed(path))

def find_path_intersection(path_1: list, path_2: list):
    latest_common = 'COM'
    while path_2 or path_1:
        n1 = path_1.pop(0)
        n2 = path_2.pop(0)
        if n1 != n2:
            return [latest_common, n1] + path_1, [latest_common, n2] + path_2
        else:
            latest_common = n1

def solve_1(puzzle_input: list) -> str:
    orbits, start, you, santa = parse_input(puzzle_input)
    counts = count_indirect_orbits(orbits, start)
    # logging.debug(counts)
    return sum(counts.values())

def solve_2(puzzle_input: list) -> str:
    orbits, start, you, santa = parse_input(puzzle_input)
    # logging.debug(counts)
    # return sum(counts.values())

    path_you = find_path_to_start(orbits, start, you)
    path_santa = find_path_to_start(orbits, start, santa)

    path_you, path_santa = find_path_intersection(path_you, path_santa)
    return len(path_you) + len(path_santa) - 4 # Subtract destinations and common node

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
