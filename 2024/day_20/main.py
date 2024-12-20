import argparse
import heapq
import logging
import sys
import time

from collections import defaultdict

from copy import deepcopy


def parse_input(input: list) -> (list, tuple, tuple):
    grid = []
    for y, line in enumerate(input):
        row = []
        for x, char in enumerate(line):
            match char:
                case ".":
                    row.append(float('inf'))
                case "#":
                    row.append(-1)
                case "S":
                    start = (x, y)
                    row.append(0)
                case "E":
                    end = (x, y)
                    row.append(float('inf'))

        grid.append(row)
    
    return grid, start, end

def find_viable_shortcuts(grid: list) -> list:
    results = []
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if y == 0 or y == len(grid)-1 or x == 0 or x == len(row)-1:
                continue
            elif cell == -1:
                directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                adjacent_walls = 0
                for d in directions:
                    nx, ny = x + d[0], y + d[1]
                    if grid[ny][nx] == -1:
                        adjacent_walls += 1
                if adjacent_walls < 3:
                    results.append((x, y))

    return results    

def dijkstra(grid: list, start: tuple = (0, 0), end: tuple = (70, 70)) -> list:
    cols, rows = end
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # left, right, up, down

    # Priority queue for Dijkstra
    priority_queue = []
    heapq.heappush(priority_queue, (0, start))  # (cost, position)
    grid[start[1]][start[0]] = 0

    # Track the shortest path
    prev = {start: None}

    while priority_queue:
        cost, current = heapq.heappop(priority_queue)
        if current == end:
            break

        for d in directions:
            nx, ny = current[0] + d[0], current[1] + d[1]
            if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]) and grid[ny][nx] != -1:
                new_cost = cost + 1
                if new_cost < grid[ny][nx]:
                    grid[ny][nx] = new_cost
                    heapq.heappush(priority_queue, (new_cost, (nx, ny)))
                    prev[(nx, ny)] = current

    return grid[end[1]][end[0]]

def solve_1(input: list) -> str:
    grid, start, end = parse_input(input)
    base_length = dijkstra(deepcopy(grid), start, end)
    valid_shortcuts = find_viable_shortcuts(grid)

    shortcuts = defaultdict(int)

    # for shortcut in valid_shortcuts:
    for i, shortcut in enumerate(valid_shortcuts):
        logging.debug(f"Shortcut {i+1}/{len(valid_shortcuts)}")
        temp_grid = deepcopy(grid)
        x, y = shortcut
        temp_grid[y][x] = float('inf')
        length = dijkstra(temp_grid, start, end)
        savings = base_length - length

        shortcuts[savings] += 1

    # for k, v in sorted(results.items()):
    #     logging.debug(f"There are {v} cheats that save {k} picoseconds")

    result = 0
    for key, value in shortcuts.items():
        if key >= 100:
            result += value

    return result

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
