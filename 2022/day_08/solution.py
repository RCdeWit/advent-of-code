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

    tree_map = []

    for line in input:
        tree_line = []
        for digit in line:
            tree_line.append(digit)
        tree_map.append(tree_line)

# Print results depending on the question (1 or 2)
match question:
    case "1":
        print(tree_map)
    case "2":
        print(2)