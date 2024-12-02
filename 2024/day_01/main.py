import argparse
import collections
import logging
import sys

def parse_input(input: list):
    list_1 = []
    list_2 = []

    for line in input:
        numbers = line.split("   ")
        list_1.append(int(numbers[0]))
        list_2.append(int(numbers[1]))

    # logging.debug(f"List 1: {list_1}")
    list_1.sort()
    list_2.sort()

    return list_1, list_2

def compare_list(list_1: list, list_2: list):
    for i, value in enumerate(list_1):
        distance = abs(value - list_2[i])
        yield distance

def group_by_count(input_list: list) -> dict:
    counter = collections.Counter(input_list)
    return counter

def calculate_similarity_score(input_list: list, reference_list: list) -> int:

    grouped_reference_list = group_by_count(reference_list)

    similarity_score = 0
    for value in input_list:
        if value in grouped_reference_list:
            similarity_score += grouped_reference_list[value] * value

    return similarity_score

def solve_1(input: list) -> int:
    list_1, list_2 = parse_input(input)
    distances = compare_list(list_1, list_2)

    return sum(distances)

def solve_2(input: list) -> int:
    list_1, list_2 = parse_input(input)
    similarity_score = calculate_similarity_score(list_1, list_2)

    return similarity_score

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