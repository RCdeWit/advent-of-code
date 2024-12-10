import argparse

# Parse CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True)
parser.add_argument("-q", "--question", required=True)
args = parser.parse_args()

input_file = args.input
question = args.question

# Read input
with open(input_file) as f:
    input = list(f.read().splitlines())


def find_beating_play(opponent):
    match opponent:
        case "rock":
            return "paper"
        case "paper":
            return "scissors"
        case "scissors":
            return "rock"


def find_losing_play(opponent):
    match opponent:
        case "rock":
            return "scissors"
        case "paper":
            return "rock"
        case "scissors":
            return "paper"


# Play round of RPS
def play_round_rps(player1, player2):
    if player1 == player2:
        return "draw"
    elif find_beating_play(player1) == player2:
        return "win"
    else:
        return "loss"


# Calculate score
def calc_score(result, choice):
    score = 0

    match result:
        case "win":
            score = score + 6
        case "draw":
            score = score + 3

    match choice:
        case "rock":
            score = score + 1
        case "paper":
            score = score + 2
        case "scissors":
            score = score + 3

    return score


# Change input letter to RPS
def parse_input(letter):
    match letter:
        case "A":
            return "rock"
        case "B":
            return "paper"
        case "C":
            return "scissors"
        case "X":
            return "rock"
        case "Y":
            return "paper"
        case "Z":
            return "scissors"


def parse_input_2(letter):
    match letter:
        case "X":
            return "lose"
        case "Y":
            return "draw"
        case "Z":
            return "win"


# Print results depending on the question (1 or 2)
match question:
    case "1":
        score = 0
        for l in input:
            opponent = parse_input(l[0])
            you = parse_input(l[2])

            result = play_round_rps(opponent, you)

            score = score + calc_score(result, you)

        print(score)

    case "2":
        score = 0
        for l in input:
            opponent = parse_input(l[0])
            desired_outcome = parse_input_2(l[2])

            match desired_outcome:
                case "draw":
                    you = opponent
                case "win":
                    you = find_beating_play(opponent)
                case "lose":
                    you = find_losing_play(opponent)

            result = play_round_rps(opponent, you)
            score = score + calc_score(result, you)

        print(score)
