import argparse
import re

# Parse CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True)
parser.add_argument("-q", "--question", required=True)
args = parser.parse_args()

input_file = args.input
question = args.question

# Read input
with open(input_file) as f:
    input = list(f.read())

# Print results depending on the question (1 or 2)
match question:
    case "1":
        print(1)
    case "2":
        result = find_marker_position(input, marker_length=14)
        print(2)