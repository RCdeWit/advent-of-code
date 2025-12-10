import argparse
import logging
import math
import sys

from collections import defaultdict
from itertools import combinations

from z3 import Int, Optimize, sat

def parse_input(input: list):
    puzzle_input = []

    for line in input:
        if not line.strip():
            continue

        # Extract grid pattern from brackets [.##.]
        grid_start = line.index('[')
        grid_end = line.index(']')
        grid = line[grid_start+1:grid_end]

        # Extract everything after the grid
        rest = line[grid_end+1:].strip()

        # Split by spaces and parse tuples and sets
        parts = []
        current = ""
        paren_depth = 0
        brace_depth = 0

        for char in rest + " ":
            if char == '(':
                paren_depth += 1
                current += char
            elif char == ')':
                paren_depth -= 1
                current += char
                if paren_depth == 0:
                    # Parse the tuple
                    nums = current[1:-1]  # Remove parentheses
                    if nums:
                        parts.append(tuple(int(x) for x in nums.split(',')))
                    else:
                        parts.append(())
                    current = ""
            elif char == '{':
                brace_depth += 1
                current += char
            elif char == '}':
                brace_depth -= 1
                current += char
                if brace_depth == 0:
                    # Parse as list to preserve order for joltage requirements
                    nums = current[1:-1]  # Remove braces
                    if nums:
                        parts.append([int(x) for x in nums.split(',')])
                    else:
                        parts.append([])
                    current = ""
            elif char == ' ' and paren_depth == 0 and brace_depth == 0:
                continue
            else:
                current += char

        # Last element should be the joltage list in braces
        joltage = parts[-1] if parts and isinstance(parts[-1], list) else []
        tuples = [p for p in parts if isinstance(p, tuple)]

        puzzle_input.append((grid, tuples, joltage))

    return puzzle_input

def press_buttons(state, buttons):
    state_list = list(state)
    for button in buttons:
        for light in button:
            if state_list[light] == '#':
                state_list[light] = '.'
            else:
                state_list[light] = '#'
    return ''.join(state_list)

def find_min_presses(target, buttons):
    n_buttons = len(buttons)
    initial_state = '.' * len(target)

    min_presses = float('inf')

    for mask in range(1 << n_buttons):
        state = initial_state
        presses = 0

        for i in range(n_buttons):
            if mask & (1 << i):
                state = press_buttons(state, [buttons[i]])
                presses += 1

        if state == target:
            min_presses = min(min_presses, presses)

    return min_presses if min_presses != float('inf') else -1

def solve_1(input: list) -> int:
    puzzle_input = parse_input(input)

    logging.debug(puzzle_input)

    total_presses = 0
    for grid, buttons, _ in puzzle_input:
        min_presses = find_min_presses(grid, buttons)
        logging.debug(f"Grid {grid}: {min_presses} presses")
        total_presses += min_presses

    return total_presses


def solve_with_z3(target_joltage, buttons):
    """
    Solve using Z3 constraint solver.
    We want to find button_presses[i] >= 0 such that:
    sum(button_presses[i] * button_affects[i][j]) = target_joltage[j] for all j
    And minimize: sum(button_presses[i])
    """
    

    n_counters = len(target_joltage)
    n_buttons = len(buttons)

    # Create optimizer
    opt = Optimize()

    # Create integer variables for button presses
    button_presses = [Int(f'button_{i}') for i in range(n_buttons)]

    # Add constraints: each button press >= 0
    for bp in button_presses:
        opt.add(bp >= 0)

    # Add constraints: for each counter, sum of button presses affecting it = target
    for counter_idx in range(n_counters):
        counter_sum = 0
        for button_idx, button in enumerate(buttons):
            if counter_idx in button:
                counter_sum += button_presses[button_idx]
        opt.add(counter_sum == target_joltage[counter_idx])

    # Minimize total button presses
    total_presses = sum(button_presses)
    opt.minimize(total_presses)

    # Solve
    if opt.check() == sat:
        model = opt.model()
        result = sum(model[bp].as_long() for bp in button_presses)
        return result


def find_min_presses_joltage(target_joltage, buttons):
    """Find minimum button presses - try constraint solvers first, then BFS."""

    n_counters = len(target_joltage)
    target_tuple = tuple(target_joltage)
    initial_state = tuple([0] * n_counters)

    if initial_state == target_tuple:
        return 0

    z3_result = solve_with_z3(target_joltage, buttons)
    if z3_result is not None:
        logging.debug(f"Z3 found solution: {z3_result}")
        return z3_result

    return -1

def solve_2(input: list) -> int:
    puzzle_input = parse_input(input)

    logging.debug(puzzle_input)

    total_presses = 0
    for _, buttons, joltage in puzzle_input:
        min_presses = find_min_presses_joltage(joltage, buttons)
        logging.debug(f"Joltage {joltage}: {min_presses} presses")
        if min_presses == -1:
            logging.error(f"No solution found for {joltage}")
            return -1
        total_presses += min_presses

    return total_presses

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

    if question == "1":
        solution = solve_1(input)
        logging.info(f"Found solution: {solution}")
    elif question == "2":
        solution = solve_2(input)
        logging.info(f"Found solution: {solution}")
    else:
        logging.error("Select either question 1 or 2")
