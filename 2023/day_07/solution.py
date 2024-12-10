import argparse
import logging
import sys


def parse_input(input: list, assignment: int):
    for line in input:
        hand, score = line.split(" ")
        score = int(score)
        hand_parsed = ""
        for char in hand:
            if char.isdigit():
                hand_parsed += char
            else:
                match char:
                    case "A":
                        hand_parsed += "Z"
                    case "K":
                        hand_parsed += "Y"
                    case "Q":
                        hand_parsed += "X"
                    case "J":
                        if assignment == 1:
                            hand_parsed += "W"
                        elif assignment == 2:
                            hand_parsed += "0"
                        else:
                            logging.error("Provide assignment")
                    case "T":
                        hand_parsed += "V"

        yield (hand_parsed, score)


def evaluate_hand(hand: tuple):
    hand = sorted(hand[0])
    count_distinct_cards = len(set(hand))

    if count_distinct_cards == 1:
        return (6, "five_of_a_kind")
    elif count_distinct_cards == 2:
        if hand[1] == hand[2] == hand[3]:
            # Four of a kind
            return (5, "four_of_a_kind")
        else:
            # Full house
            return (4, "full_house")
    elif count_distinct_cards == 5:
        # High card
        return (0, "high_card")
    else:
        distinct_cards = set(hand)
        aggregate = {}
        for card in distinct_cards:
            aggregate[card] = hand.count(card)
        aggregate = [
            v
            for k, v in sorted(
                aggregate.items(), key=lambda item: item[1], reverse=True
            )
        ]
        if aggregate[0] == 3:
            # Three of a kind
            return (3, "three_of_a_kind")
        elif aggregate[0] == aggregate[1] == 2:
            # Two pair
            return (2, "two_pair")
        elif aggregate[0] == 2:
            # One pair
            return (1, "one_pair")
        else:
            logging.error("Mistake in hand parsing")
            return None


def calculate_winnings(hands: list):
    winnings = 0
    for i, hand in enumerate(hands):
        winnings += hand[1] * (i + 1)
    return winnings


def assign_joker(hand: tuple):
    hand = hand[0]

    if "0" in hand:
        distinct_cards = set(hand)
        joker = (0, "0")
        for card in distinct_cards:
            count = hand.count(card)
            if count > joker[0] and card != "0":
                joker = (count, card)
            elif count == joker[0] and card > joker[1] and card != "0":
                joker = (count, card)

        return joker[1]
    else:
        return None


def solve_1(input):
    hands = list(parse_input(input, 1))
    parsed_hands = []
    for hand in hands:
        parsed_hands.append((str(evaluate_hand(hand)[0]) + "-" + hand[0], hand[1]))
    parsed_hands.sort()
    # logging.debug(parsed_hands)
    return calculate_winnings(parsed_hands)


def solve_2(input):
    hands = list(parse_input(input, 2))
    parsed_hands = []
    for hand in hands:
        if "0" in hand[0]:
            joker = assign_joker(hand)
            joker_hand = hand[0].replace("0", joker)
            rank = evaluate_hand((joker_hand, hand[1]))[0]
        else:
            rank = evaluate_hand(hand)[0]

        parsed_hands.append((str(rank) + "-" + hand[0], hand[1]))

    parsed_hands.sort()
    return calculate_winnings(parsed_hands)


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
