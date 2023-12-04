import argparse
import logging
import sys

def parse_input(input: list):
    cards = {}
    for line in input:
        line = line.split("Card ")[1]
        card_id, line = line.split(":")
        winning, haves = line.split("|")

        card_id = card_id.strip()

        winning = list(filter(None, winning.split(" ")))
        haves = list(filter(None, haves.split(" ")))

        winning.sort()
        haves.sort()

        cards[card_id] = [winning, haves]
    
    # logging.debug(cards)
    return cards

def compare_card(card: list):
    winning, haves = card
    for w in winning:
        # logging.debug(w)
        if w in haves:
            yield w

def calculate_score(matches: list):
    if len(matches) == 0:
        return 0
    elif len(matches) == 1:
        return 1
    else:
        return 2 ** (len(matches)-1)

def find_cards_won(card_id: str, all_cards: dict):
    score = len(list(compare_card(all_cards[card_id])))

    i = 1
    while i <= score:
        yield str(int(card_id) + i)
        i += 1

def solve_1(input):
    cards = parse_input(input)
    
    result = 0
    for card_id in cards:
        compared = list(compare_card(cards[card_id]))
        score = calculate_score(compared)
        result += score

    return result

def solve_2(input):
    cards = parse_input(input)
    stash = {}
    for i in range(len(cards)):
        stash[str(i+1)] = 1

    for key, count in stash.items():
        cards_won = list(find_cards_won(key, cards))
        for c in cards_won:
            stash[c] += count

    # logging.debug(stash)
    return sum(stash.values())

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