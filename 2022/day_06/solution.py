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

def find_marker_position(datastream, marker_length):
    buffer = []

    for i, c in enumerate(datastream):
        buffer.append(c)

        if len(buffer) == marker_length:
            # Set retains unique values in list
            # If its length < 4, there's a duplicate in the buffer
            # Otherwise we have found the start of the packet
            if len(set(buffer)) == marker_length:
                return(i+1)

            buffer.pop(0)

# Print results depending on the question (1 or 2)
match question:
    case "1":
        result = find_marker_position(input, marker_length=4)
        print(result)
    case "2":
        result = find_marker_position(input, marker_length=14)
        print(result)