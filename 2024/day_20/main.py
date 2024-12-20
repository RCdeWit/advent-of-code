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
                    row.append(float("inf"))
                case "#":
                    row.append(-1)
                case "S":
                    start = (x, y)
                    row.append(0)
                case "E":
                    end = (x, y)
                    row.append(float("inf"))

        grid.append(row)

    return grid, start, end


def find_viable_shortcuts(grid: list) -> list:
    results = []
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if y == 0 or y == len(grid) - 1 or x == 0 or x == len(row) - 1:
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


def find_viable_shortcuts_2(base_path: list) -> list:
    # Create grid-based buckets
    grid_size = 20
    buckets = defaultdict(list)

    # Assign coordinates to grid buckets
    for x, y in base_path.keys():
        grid_key = (x // grid_size, y // grid_size)
        buckets[grid_key].append((x, y))

    def manhattan(x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    # Find all valid pairs
    results = []
    for (gx, gy), points in buckets.items():
        # Check points in the same and neighboring buckets
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                neighbor_key = (gx + dx, gy + dy)
                if neighbor_key in buckets:
                    for x1, y1 in points:
                        for x2, y2 in buckets[neighbor_key]:
                            dist = manhattan(x1, y1, x2, y2)
                            if dist <= 20:
                                results.append(((x1, y1), (x2, y2), dist))
    return results


def dijkstra(grid: list, start: tuple = (0, 0), end: tuple = (70, 70)) -> tuple:
    cols, rows = len(grid[0]), len(grid)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # left, right, up, down

    # Priority queue for Dijkstra
    priority_queue = []
    heapq.heappush(priority_queue, (0, start))  # (cost, position)
    grid[start[1]][start[0]] = 0  # Accessing grid[y][x]

    # Track the shortest path
    prev = {start: None}
    shortest_cost = {start: 0}

    while priority_queue:
        cost, current = heapq.heappop(priority_queue)
        if current == end:
            break

        for d in directions:
            nx, ny = current[0] + d[0], current[1] + d[1]
            if 0 <= ny < rows and 0 <= nx < cols and grid[ny][nx] != -1:
                new_cost = cost + 1  # All edges have a weight of 1
                if (nx, ny) not in shortest_cost or new_cost < shortest_cost[(nx, ny)]:
                    shortest_cost[(nx, ny)] = new_cost
                    heapq.heappush(priority_queue, (new_cost, (nx, ny)))
                    prev[(nx, ny)] = current

    # Reconstruct the optimal path
    path_with_costs = {}
    node = end
    if node in shortest_cost:  # Ensure the end node is reachable
        while node is not None:
            path_with_costs[node] = shortest_cost[node]
            node = prev.get(node)

    # If no path exists, return an empty path and infinity
    if not path_with_costs or (
        start not in path_with_costs or end not in path_with_costs
    ):
        return float("inf"), {}

    return shortest_cost.get(end, float("inf")), path_with_costs


def detract_shortcut(base_path: list, shortcut: tuple) -> int:
    (x1, y1), (x2, y2), shortcut_cost = shortcut
    base_cost = base_path[(x2, y2)] - base_path[(x1, y1)]
    savings = base_cost - shortcut_cost

    return savings


def solve_1(input: list) -> str:
    grid, start, end = parse_input(input)
    base_length, base_path = dijkstra(deepcopy(grid), start, end)
    valid_shortcuts = find_viable_shortcuts(grid)

    shortcuts = defaultdict(int)

    for i, shortcut in enumerate(valid_shortcuts):
        logging.debug(f"Shortcut {i+1}/{len(valid_shortcuts)}")
        temp_grid = deepcopy(grid)
        x, y = shortcut
        temp_grid[y][x] = float("inf")
        length, path = dijkstra(temp_grid, start, end)
        savings = base_length - length

        shortcuts[savings] += 1

    # for k, v in sorted(shortcuts.items()):
    #     logging.debug(f"There are {v} cheats that save {k} picoseconds")

    result = 0
    for key, value in shortcuts.items():
        logging.debug(f"Shortcuts saving {key} picoseconds: {value}")
        if key >= 100:
            result += value

    return result


def solve_2(input: list) -> int:
    grid, start, end = parse_input(input)
    base_length, base_path = dijkstra(grid, start, end)
    logging.debug(f"Base path length: {base_length}")
    logging.debug(f"Base path: {base_path}")

    valid_shortcuts = list(find_viable_shortcuts_2(base_path))
    # logging.debug(valid_shortcuts)

    savings = defaultdict(int)

    for i, shortcut in enumerate(valid_shortcuts):
        logging.debug(f"Shortcut {i+1}/{len(valid_shortcuts)}: {shortcut}")
        saving = detract_shortcut(base_path, shortcut)

        savings[saving] += 1

    # for k, v in sorted(savings.items()):
    #     if k >= 50:
    #         logging.debug(f"There are {v} cheats that save {k} picoseconds")

    result = 0
    for key, value in savings.items():
        if key >= 100:
            result += value

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
