import argparse
import logging
import sys

def parse_line(line: str):
    game_id = int(line.split(":")[0].split("Game ")[1])
    # logging.debug(f"Game ID: {game_id}")

    sets = line.split(":")[1].split(";")
    # logging.debug(f"Sets: {sets}")

    result = []
    for s in sets:
        sub_result = {}
        balls = s.split(',')
        for b in balls:
            amount = int(''.join([char for char in b.split() if char.isdigit()]))
            colour = ''.join([char for char in b.split() if char.isalpha()])
            sub_result[colour] = amount
        result.append(sub_result)

    # logging.debug(f"Game: {game_id}: {result}")
    return game_id, result

def game_is_possible(game: list):
    for sets in game:
        for colour, amount in sets.items():
            if colour == "red" and amount > 12:
                # logging.debug(f"Found {amount} {colour} balls; impossible game")
                return False
            elif colour == "green" and amount > 13:
                # logging.debug(f"Found {amount} {colour} balls; impossible game")
                return False
            elif colour == "blue" and amount > 14:
                # logging.debug(f"Found {amount} {colour} balls; impossible game")
                return False
    return True

def solve_1(input: list):
    games = {}
    for line in input:
        game_id, sets = parse_line(line)
        games[game_id] = sets
    # logging.debug(games)

    result = 0
    for game_id, game in games.items():
        if game_is_possible(game):
            # logging.debug(f"Game {game_id} is possible")
            result = result + game_id
    
    return result


def solve_2(input: list):
    return 

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