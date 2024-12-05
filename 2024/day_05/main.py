import argparse
import logging
import sys

from collections import defaultdict
from math import floor

def parse_input(input: list):
    rules = []
    updates = []
    part_1 = True
    for line in input:
        if line == "":
            part_1 = False
        elif part_1:
            rules.append(tuple(map(int, line.split("|"))))
        else:
            updates.append(list(map(int, line.split(","))))
        
    return rules, updates

def aggregate_rules(rules: list) -> dict:
    output = defaultdict(list)
    for rule in rules:
        output[rule[0]].append(rule[1])

    return output

def check_if_matches_rules(rules: list, update: list) -> bool:
    rules = aggregate_rules(rules)
    for i, value in enumerate(update):
        if len(set(update[:i]) & set(rules[value])) > 0:
            return False

    return True

def check_if_matches_order(order: list, update: list) -> bool:
    index_page_1 = order.index(update[0])
    order_slice_1 = order[:index_page_1]
    order_slice_2 = order[index_page_1:]
    order = order_slice_2 + order_slice_1

    current_index = -1

    for i in update:
        if order.index(i) > current_index:
            current_index = order.index(i)
        else:
            return False

    return True

def solve_1(input: list) -> int:
    rules, updates = parse_input(input)
    # order = calculate_topological_order(rules)

    # logging.debug(rules)
    # logging.debug(updates)
    # logging.debug(order)

    # matches = list(map(lambda x: check_if_matches_order(order, x), updates))
    matches = list(map(lambda x: check_if_matches_rules(rules, x), updates))
    middle_pages = list(map(lambda x: x[floor(len(x)/2)], updates))

    result = 0
    for i, match in enumerate(matches):
        if match:
            result += middle_pages[i]

    return result

def solve_2(input: list) -> int:
    pass

if __name__ == '__main__':
     # Parse CLI arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--question", required=True)
    parser.add_argument("-i", "--input", required=False, default='input.txt')
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

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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