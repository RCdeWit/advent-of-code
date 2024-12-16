import argparse
import heapq
import logging
import sys
import time


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


def get_direction(prev, current) -> tuple:
    return current[0] - prev[0], current[1] - prev[1]


def dijkstra_with_turns_and_directions(grid: list, start: tuple, end: tuple) -> (int, list):
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def find_valid_neighbours(pos: tuple) -> tuple:
        x, y = pos
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and grid[ny][nx] != "#":
                yield (nx, ny)

    initial_direction = (1, 0)
    priority_queue = [(0, start, initial_direction, [start])]

    state_costs = {}
    equivalent_paths = []
    min_cost = float("inf")

    while priority_queue:
        cost, current, direction, path = heapq.heappop(priority_queue)

        # Update state costs
        if (current, direction) in state_costs and state_costs[
            (current, direction)
        ] < cost:
            continue
        state_costs[(current, direction)] = cost

        # Reached end
        if current == end:
            if cost < min_cost:
                min_cost = cost
                equivalent_paths = [path]
            elif cost == min_cost:
                equivalent_paths.append(path)
            continue

        # Explore neighbors
        for neighbor in find_valid_neighbours(current):
            new_dir = get_direction(current, neighbor)

            turn_cost = 1001 if direction != new_dir else 1
            total_cost = cost + turn_cost
            new_path = path + [neighbor]

            # Update priority queue
            if (neighbor, new_dir) not in state_costs or state_costs[
                (neighbor, new_dir)
            ] >= total_cost:
                heapq.heappush(
                    priority_queue, (total_cost, neighbor, new_dir, new_path)
                )
                state_costs[(neighbor, new_dir)] = total_cost

    return min_cost, equivalent_paths


def count_visited_nodes_in_paths(paths: list) -> int:
    visited = set()
    for path in paths:
        visited.update(path)
        logging.debug(visited)
    return len(visited)


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
    print_grid(grid, best_path[0])

    return min_cost


def solve_2(input: list) -> int:
    grid, start, end = parse_input(input)
    # logging.debug(grid)
    # valid_steps = find_valid_steps(grid)
    # logging.debug(valid_steps)

    min_cost, best_paths = dijkstra_with_turns_and_directions(grid, start, end)
    # print_grid(grid, best_paths[0])

    # for path in best_paths:
    #     print_grid(grid, path)
    #     print()

    return count_visited_nodes_in_paths(best_paths)


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
