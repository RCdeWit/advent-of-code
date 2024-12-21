import argparse
import logging
import sys
import time

from collections import deque

from functools import lru_cache

def parse_input(input: list) -> list:
    sequences = []
    for line in input:
        sequence = []
        for char in line:
            sequence.append(char)

        sequences.append(sequence)

    return sequences

def optimize_path_segment(path: str, schema: list, current_position: str) -> str:
    if ("A", "W") in schema:
        schema = "dirpad"
    elif ("A", "0") in schema:
        schema = "numpad"
    else:
        raise ValueError("Unknown control schema")

    if schema == "dirpad":
        # logging.debug(f"Trying to optimize {path} from {current_position}")
        match current_position:
            case "W":
                priority = {"E": 0, "N": 0, "A": 0}
            case "N":
                priority = {"S": 0, "W": 0, "E": 0, "A": 0}
            case "S":
                priority = {"N": 0, "W": 0, "E": 0, "A": 0}
            case "E":
                priority = {"N": 0, "W": 0, "A": 0}
            case "A":
                priority = {"S": 0, "W": 0, "A": 0}

        for char in path:
            priority[char] += 1

        optimized = ""
        for key, value in priority.items():
            for _ in range(value):
                optimized += key

        return optimized
    
    elif schema == "numpad":
        # logging.debug(f"Trying to optimize {path} from {current_position}")
        if current_position in ("0", "A"):
            priority = {"N": 0, "W": 0, "E": 0, "A": 0}
        elif current_position in ("9", "6", "3"):
            priority = {"W": 0, "S": 0, "N": 0, "A": 0}
        elif current_position in ("8", "5", "2"):
            priority = {"W": 0, "S": 0, "N": 0, "E": 0, "A": 0}
        elif current_position in ("7", "4", "1"):
            priority = {"E": 0, "S": 0, "N": 0, "A": 0}
            
        for char in path:
            priority[char] += 1

        optimized = ""
        if current_position == "A":
            if priority["W"] == 1:
                optimized += "W"
                priority["W"] = 0

        for key, value in priority.items():
            for _ in range(value):
                optimized += key

        return optimized
    

def bfs(grid, start):
    rows, cols = len(grid), len(grid[0])
    directions = [(1, 0, "S"), (0, -1, "W"), (0, 1, "E"), (-1, 0, "N")]
    distances_and_paths = {}
    queue = deque([(start, 0, "")])  # (current position, distance, path)
    visited = set()
    visited.add(start)
    
    while queue:
        (x, y), dist, path = queue.popleft()
        distances_and_paths[(x, y)] = (dist, path + "A")
        
        # Explore neighbors
        for dx, dy, dir_char in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited and grid[nx][ny] is not None:
                visited.add((nx, ny))
                queue.append(((nx, ny), dist + 1, path + dir_char))
    
    return distances_and_paths

def get_graph(schema: list) -> list:

    button_positions = [
        (x, y) for x, row in enumerate(schema)
        for y, val in enumerate(row) if val is not None
    ]
    all_distances_and_paths = {}
    
    for start in button_positions:
        start_value = schema[start[0]][start[1]]
        distances_and_paths = bfs(schema, start)
        
        for end, (dist, path) in distances_and_paths.items():
            if end != start:
                end_value = schema[end[0]][end[1]]
                all_distances_and_paths[(start_value, end_value)] = (dist + 1, path) # +1 for the press on the button
    
    return all_distances_and_paths

def calculate_remote_sequence(sequence: str, control_schema: list) -> (int, str):
    total_cost = 0
    start = 'A'

    remote_button_path = ""

    for button in sequence:
        if start == button:
            button_cost = 1
            button_path = 'A'
        else:
            button_cost, button_path = control_schema[(start, button)]
            button_path = optimize_path_segment(button_path, control_schema, start)
        # logging.debug(f"From button {start} to {button}: {button_path} costs {button_cost} movements")
        
        total_cost += button_cost
        remote_button_path += button_path
        start = button

    return total_cost, remote_button_path


def solve_1(input: list) -> str:
    sequences = parse_input(input)
    numpad = get_graph([['7', '8', '9'], ['4', '5', '6'], ['1', '2', '3'], [None, '0', "A"]])
    directional_pad = get_graph([[None, 'N', 'A'], ['W', 'S', 'E']])

    # logging.debug(sequences)
    # logging.debug(numpad)
    # logging.debug(directional_pad)

    result = 0

    for sequence in sequences:
        # Original numpad
        cost, new_sequence = calculate_remote_sequence(sequence, numpad)
        # logging.debug(f"Press {new_sequence} to achieve {sequence} at cost {cost}")

        # Directionalpad 1
        cost, new_sequence = calculate_remote_sequence(new_sequence, directional_pad)
        # logging.debug(f"Press {new_sequence} to achieve {sequence} at cost {cost}")

        # Directionalpad 2 (player)
        cost, new_sequence = calculate_remote_sequence(new_sequence, directional_pad)
        # logging.debug(f"Press {new_sequence} to achieve {sequence} at cost {cost}")

        logging.debug(f"Result for {sequence}: {cost} * {int(''.join(sequence)[:-1])} = {cost * int(''.join(sequence)[:-1])}")
        result += cost * int("".join(sequence)[:-1])

    return result

def solve_1(input: list) -> str:
    sequences = parse_input(input)
    numpad = get_graph([['7', '8', '9'], ['4', '5', '6'], ['1', '2', '3'], [None, '0', "A"]])
    directional_pad = get_graph([[None, 'N', 'A'], ['W', 'S', 'E']])

    # logging.debug(sequences)
    # logging.debug(numpad)
    # logging.debug(directional_pad)

    result = 0

    for j, sequence in enumerate(sequences):
        # Original numpad
        cost, new_sequence = calculate_remote_sequence(sequence, numpad)
        # logging.debug(f"Press {new_sequence} to achieve {sequence} at cost {cost}")

        # Directionalpad 1
        for i in range(25):
            cost, new_sequence = calculate_remote_sequence(new_sequence, directional_pad)
            logging.debug(f"Sequence {j}, depth {i}")
        # logging.debug(f"Press {new_sequence} to achieve {sequence} at cost {cost}")

        logging.debug(f"Result for {sequence}: {cost} * {int(''.join(sequence)[:-1])} = {cost * int(''.join(sequence)[:-1])}")
        result += cost * int("".join(sequence)[:-1])

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
    start = time.time()

    if question == "1":
        solution = solve_1(input)
        logging.info(f"Found solution: {solution} (in {time.time()-start} seconds)")
    elif question == "2":
        solution = solve_2(input)
        logging.info(f"Found solution: {solution} (in {time.time()-start} seconds)")
    else:
        logging.error("Select either question 1 or 2")
