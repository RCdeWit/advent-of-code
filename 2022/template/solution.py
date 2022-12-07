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

def parse_input(input):

    file_structure = {}

    total_lines = len(input)
    current_line = 0

    current_directory = ""
    buffer_list = {}

    while current_line <= total_lines:
        # If command
        if input[current_line][0] == "$":
            # Write output from previous command to file_structure
            # Clear file structure
            # Execute command

            if input[current_line][0:4] == "$ cd":
                current_directory = input[current_line][5:]
                print(current_directory)
        
        else:
            if input[current_line][0:3] == "dir":
                # Add dir to buffer list
                new_level = {}
                buffer_list.append(input[current_line])
            else:
                buffer_list.append(input[current_line])

        
        current_line = current_line + 1

    return structure

        


# Print results depending on the question (1 or 2)
match question:
    case "1":
        print(1)
    case "2":
        print(2)