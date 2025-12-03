import argparse
import logging
import sys


def parse_input(input: list):
    puzzle_input = []

    for line in input:
        bank = [int(char) for char in line]
        puzzle_input.append(bank)

    return puzzle_input

def find_voltage(bank: list) -> int:
    cell_1 = 0
    cell_2 = 0

    for cell in reversed(bank):
        if cell >= cell_1 and cell_2 != 0:
            if cell_1 > cell_2:
                cell_2 = cell_1
            cell_1 = cell
        elif cell > cell_2 and cell_1 == 0:
            cell_2 = cell

    return cell_1 * 10 + cell_2

def find_voltage_2(bank: list, num_cells: int = 2) -> int:
    result = []
    remaining = bank[:]
    
    for _ in range(num_cells):
        cells_left = num_cells - len(result) - 1
        candidates = remaining[:len(remaining) - cells_left]
        max_val = max(candidates)
        max_idx = candidates.index(max_val)
        result.append(max_val)
        remaining = remaining[max_idx + 1:]
    
    return int(''.join(map(str, result)))

def solve_1(input: list) -> int:
    banks = parse_input(input)

    result = 0
    for bank in banks:
        voltage = find_voltage(bank)
        logging.debug(f"Voltage {voltage} for {bank}")
        result += voltage
    return result

def solve_2(input: list) -> int:
    banks = parse_input(input)

    result = 0
    for bank in banks:
        voltage = find_voltage_2(bank, 12)
        logging.debug(f"Voltage {voltage} for {bank}")
        result += voltage
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

    if question == "1":
        solution = solve_1(input)
        logging.info(f"Found solution: {solution}")
    elif question == "2":
        solution = solve_2(input)
        logging.info(f"Found solution: {solution}")
    else:
        logging.error("Select either question 1 or 2")
