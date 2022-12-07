import argparse
import sys

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

def parse_input_to_file_system(input):   
    filesystem = {}
    dirstack = []
    current = filesystem

    for current_line in input:
        if current_line[0] == "$":
            if current_line.startswith("$ cd .."):
                dirstack.pop()

                current = filesystem
                for entry in dirstack:
                    current = filesystem[entry]

            elif current_line.startswith("$ cd"):
                destination = current_line[5:]
                if destination == "/":
                    dirstack = []
                    current = filesystem
                else:
                    dirstack.append(destination)
                    current = current[destination]

        elif current_line.startswith('dir '):
            dir_name = current_line.split(' ')[1]
            current[dir_name] = {}
        else:
            file_name = current_line.split(' ')[1]
            file_size = current_line.split(' ')[0]

            current[file_name] = file_size

    return filesystem

def find_totals(input):
    total = 0

    for key, value in input.items():
        # File
        if type(value) == str:
            total = total + int(value)
        # Directory
        else:
            total = total + find_totals(value)

            if total <= 100000:
                result.append(total)

    return(total)

result = []

# Print results depending on the question (1 or 2)
match question:
    case "1":
        file_system = parse_input_to_file_system(input)
        print(find_totals(file_system))
        print(sum(result))
    case "2":
        None
