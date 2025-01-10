import argparse
import logging
import sys
import time

from collections import defaultdict


def parse_input(puzzle_input: list) -> list:
    recipes = {}

    for line in puzzle_input:
        output = line.split(" => ")[1]
        output_qty = int(output.split(" ")[0])
        output_name = output.split(" ")[1]

        components = line.split(" => ")[0]
        recipe = []
        for comp in components.split(", "):
            comp_qty = int(comp.split(" ")[0])
            comp_name = comp.split(" ")[1]
            recipe.append((comp_qty, comp_name))

        recipes[output_name] = (output_qty, recipe)

    return recipes

def calculate_ore(recipes: dict, fuel_qty: int = 1) -> int:
    to_produce = defaultdict(int)
    leftovers = defaultdict(int)
    to_produce['FUEL'] = fuel_qty

    result = 0

    while to_produce:
        current, current_qty = to_produce.popitem()

        if current == "ORE":
            result += current_qty
            continue

        if leftovers[current] > 0:
            used = min(leftovers[current], current_qty)
            current_qty -= used
            leftovers[current] -= used

        if current_qty == 0:
            continue

        output_qty, ingredients = recipes[current]
        batches = (current_qty + output_qty - 1) // output_qty
        produced = batches * output_qty

        if produced > current_qty:
            leftovers[current] += produced - current_qty

        for ing_qty, ing_name in ingredients:
            to_produce[ing_name] += ing_qty * batches

    return result

def binary_search(recipes: dict, total_ore: int = 1000000000000) -> int:
    low = 0
    ore_per_fuel = calculate_ore(recipes, 1)
    high = total_ore // ore_per_fuel * 2

    while low + 1 < high:
        mid = (low + high) // 2
        ore_needed = calculate_ore(recipes, mid)
        
        if ore_needed <= total_ore:
            low = mid
        else:
            high = mid

    return low

def solve_1(puzzle_input: list) -> str:
    recipes = parse_input(puzzle_input)
    required_ore = calculate_ore(recipes)

    return required_ore

def solve_2(puzzle_input: list) -> str:
    recipes = parse_input(puzzle_input)
    return binary_search(recipes, 1000000000000)


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
        puzzle_input = list(f.read().splitlines())

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
        solution = solve_1(puzzle_input)
        logging.info(f"Found solution: {solution} (in {time.time()-start} seconds)")
    elif question == "2":
        solution = solve_2(puzzle_input)
        logging.info(f"Found solution: {solution} (in {time.time()-start} seconds)")
    else:
        logging.error("Select either question 1 or 2")
