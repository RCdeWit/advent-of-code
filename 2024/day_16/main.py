import argparse
import logging
import sys
import time

import heapq


def parse_input(input: list) -> (list, list):
    output = []
    for line in input:
        output.append(list(line))
        for char in line:
            if char == "S":
                start = (line.index(char), output.index(list(line)))
            elif char == "E":
                end = (line.index(char), output.index(list(line)))

    return output, start, end

def get_direction(prev, current):
    return current[0] - prev[0], current[1] - prev[1]

def dijkstra_with_turns_and_directions(grid, start, end):
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # Right, Down, Left, Up

    def find_valid_neighbours(pos: tuple) -> tuple:
        x, y = pos
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and grid[ny][nx] != '#':
                yield (nx, ny)

    # Priority queue: (cost, current_position, previous_direction)
    initial_direction = (1, 0)  # Fixed starting direction
    priority_queue = [(0, start, initial_direction)]
    visited = {}  # Track the minimum cost per (x, y, direction)
    previous_nodes = {}  # For path reconstruction
    best_path = []
    min_cost = float('inf')

    while priority_queue:
        cost, current, direction = heapq.heappop(priority_queue)

        # Skip if we have already visited this (x, y, direction) with a lower cost
        if (current, direction) in visited and visited[(current, direction)] <= cost:
            continue
        visited[(current, direction)] = cost

        # If we reach the end, check and update the minimum cost
        if current == end:
            if cost < min_cost:
                min_cost = cost
                # Reconstruct the path
                best_path = []
                node, dir = current, direction
                while node:
                    best_path.insert(0, node)
                    node_info = previous_nodes.get((node, dir))
                    if node_info is None:
                        break
                    node, dir = node_info
            continue

        # Explore neighbors
        for neighbor in find_valid_neighbours(current):
            new_dir = get_direction(current, neighbor)
            
            # Turn cost calculation: 1000 for turns, 1 for continuing
            turn_cost = 1001 if direction != new_dir else 1
            total_cost = cost + turn_cost

            # Only push neighbors if we haven't visited them with a lower cost
            if (neighbor, new_dir) not in visited or visited[(neighbor, new_dir)] > total_cost:
                heapq.heappush(priority_queue, (total_cost, neighbor, new_dir))
                previous_nodes[(neighbor, new_dir)] = (current, direction)

    return min_cost, best_path


def print_grid(grid: list, best_path: list):
    for i, step in enumerate(best_path):
        grid[step[1]][step[0]] = str(i % 10)

    for row in grid:
        print("".join(row).replace(".", " "))

    logging.debug(best_path)


def solve_1(input: list) -> int:
    grid, start, end = parse_input(input)
    # logging.debug(grid)
    # valid_steps = find_valid_steps(grid)
    # logging.debug(valid_steps)

    min_cost, best_path = dijkstra_with_turns_and_directions(grid, start, end)
    print_grid(grid, best_path)

    return min_cost


def solve_2(input: list) -> int:
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
