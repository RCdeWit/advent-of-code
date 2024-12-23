import argparse
import logging
import sys
import time
from collections import defaultdict


def parse_input(input: list) -> list:
    connections = []
    for line in input:
        source, dest = line.split("-")
        connections.append(tuple((source, dest)))
        # computers.append(tuple((dest, source)))

    return list(set(connections))

def find_networks(connections: list) -> dict:
    networks = defaultdict(list)
    for connection in connections:
        source, dest = connection
        if dest not in networks[source]:
            networks[source].append(dest)
        if source not in networks[dest]:
            networks[dest].append(source)

    return networks
       
def find_interconnections(networks: dict, computers: int = 3) -> dict:
    interconnections = []
    for source, destinations in networks.items():
        for hop_1 in destinations:
            for hop_2 in destinations:
                if hop_1 != hop_2 and hop_1 in networks[hop_2]:
                    interconnection = tuple(sorted([source, hop_1, hop_2]))
                    if interconnection not in interconnections:
                        interconnections.append(interconnection)

    return interconnections

def solve_1(input: list) -> str:
    connections = parse_input(input)
    # logging.debug(connections)
    networks = find_networks(connections)
    # logging.debug(networks)
    interconnections = find_interconnections(networks)

    result = 0
    for interconnection in interconnections:
        valid = False
        for computer in interconnection:
            if computer.startswith("t"):
                valid = True
        
        result += valid

    return result


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
