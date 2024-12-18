import argparse
import logging
import sys
import time

import heapq


def parse_input(input: list) -> (list, list):
    pairs = []

    for line in input:
        pairs.append(tuple(map(int, line.split(","))))

    return pairs

def dijkstra(obstacles: list, start: tuple = (0, 0), end: tuple = (70, 70)) -> list:
    rows, cols = end
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # left, right, up, down

    grid = []
    for _ in range(rows+1):
        row = []
        for _ in range(cols+1):
            row.append(float('inf'))
        grid.append(row)
    
    for dropped_byte in obstacles:
        x, y = dropped_byte
        grid[y][x] = -1

    # Priority queue for Dijkstra
    priority_queue = []
    heapq.heappush(priority_queue, (0, start))  # (cost, position)
    grid[start[0]][start[1]] = 0

    # Track the shortest path
    prev = {start: None}

    while priority_queue:
        cost, current = heapq.heappop(priority_queue)
        if current == end:
            break

        for d in directions:
            nx, ny = current[0] + d[0], current[1] + d[1]
            if 0 <= nx <= rows and 0 <= ny <= cols and grid[nx][ny] != -1:
                new_cost = cost + 1  # All edges have a weight of 1
                if new_cost < grid[nx][ny]:
                    grid[nx][ny] = new_cost
                    heapq.heappush(priority_queue, (new_cost, (nx, ny)))
                    prev[(nx, ny)] = current

    # Reconstruct the path
    path = []
    step = end
    while step:
        path.append(step)
        step = prev.get(step)

    return path[::-1] if grid[end[0]][end[1]] != float('inf') else []

def solve_1(input: list) -> str:
    dropped_bytes = parse_input(input)
    dropped_bytes = dropped_bytes[:1024]
    path = dijkstra(dropped_bytes, start=(0,0), end=(70,70))
    # logging.debug(path)
    return len(path) - 1 # Don't count start node

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
