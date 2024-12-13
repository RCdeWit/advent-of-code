import argparse
import logging
import sys
import time


def parse_input(input: list, conversion_error: bool = False) -> (list, list):
    result = {}
    machine = {}

    current = 0
    for line in input:
        if len(line) == 0:
            result[current] = machine
            current += 1
            machine = {}
        elif line.startswith("Button"):
            button = line.split('Button ')[1].split(":")[0]
            x = int(line.split('X+')[1].split(",")[0])
            y = int(line.split('Y+')[1])
            machine[button] = (x, y)
        else:
            x = int(line.split('X=')[1].split(',')[0])
            y = int(line.split('Y=')[1])

            if conversion_error:
                x += 10000000000000
                y += 10000000000000
            machine['Target'] = (x, y)
    result[current] = machine

    return result

def solve_machine(machine: dict) -> tuple:
    ax, ay = machine['A']
    bx, by = machine['B']
    tx, ty = machine['Target']

    det = ax * by - ay * bx

    if det == 0:
        return None
    else:
        det_x = tx * by - ty * bx
        det_y = ax * ty - ay * tx

        a = det_x // det
        b = det_y // det

        if ax * a + bx * b == tx and ay * a + by * b == ty:
            return (a, b)
        else:
            return None

def calculate_cost(presses: tuple) -> int:
    a, b = presses
    return a * 3 + b

def solve_1(input: list) -> int:
    machines = parse_input(input)
    total_cost = 0
    for machine in machines.items():
        machine = machine[1]
        solution = solve_machine(machine)
        # logging.debug(solution)
        if solution is not None:
            total_cost += calculate_cost(solution)

    return total_cost


def solve_2(input: list) -> int:
    machines = parse_input(input, conversion_error=True)
    total_cost = 0
    logging.debug(machines)
    for machine in machines.items():
        machine = machine[1]
        solution = solve_machine(machine)
        # logging.debug(solution)
        if solution is not None:
            total_cost += calculate_cost(solution)

    return total_cost

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