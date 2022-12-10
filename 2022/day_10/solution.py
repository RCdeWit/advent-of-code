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

    parsed = []
    for l in input:
        command = l.split(" ")[0]
        if command == "addx":
            parsed.append(["wait", None])
            value = int(l.split(" ")[1])
        else:
            value = None

        parsed.append([command, value])

    input = parsed

def process_command(command, X):
    if command[0] in ("noop", "wait"):
        None
    else:
        X = X + command[1]

    return(X)

# Print results depending on the question (1 or 2)
match question:
    case "1":
        X = 1
        result = 0
        for i, line in enumerate(input):
            cycle = i+1

            if cycle in (20, 60, 100, 140, 180, 220):
                result = result + (cycle * X)

            X = process_command(line, X)

        print(result)

    case "2":
        print(2)