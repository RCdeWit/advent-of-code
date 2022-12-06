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

def find_start_of_packet(datastream):
    buffer = []

    for i, c in enumerate(datastream):
        buffer.append(c)

        if len(buffer) == 4:
            # Set retains unique values in list
            # If its length < 4, there's a duplicate in the buffer
            # Otherwise we have found the start of the packet
            if len(set(buffer)) == 4:
                return(i+1)

            buffer.pop(0)

# Print results depending on the question (1 or 2)
match question:
    case "1":
        result = find_start_of_packet(input)
        print(result)
    case "2":
        print(2)