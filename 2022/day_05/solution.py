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
    input = list(f.read().splitlines())

    # Split the raw input into two sections
    input_crates = []
    input_directions = []

    target = input_crates

    for l in input:
        # If we have reached a blank line, skip to parsing next section
        if l == "":
            target = input_directions
            continue

        target.append(l)

    # Parse crates into lists
    for i, line in enumerate(reversed(input_crates)):
        
        # Get number of columns
        if i == 0:
            n_columns = int(max(line))

            # Create stack of crates 
            crates = []
            for i in range(n_columns):
                crates.append([])

        # Go through the lines one by one
        # Add every crate to its respective column
        else:
            line_position = 1
            stack = 0
            while line_position <= len(line):
                character = line[line_position]

                if  ord(character) in range(65, 91):
                    crates[stack].append(character)

                stack = stack + 1
                line_position = line_position + 4

    # Parse directions

    directions = []
    for l in input_directions:
        regex = "^move (\d+) from (\d+) to (\d+)$"

        direction = re.search(regex, l).groups()
        direction = list(int(item) for item in direction)

        # Make stacks 0 indexed
        direction[1] = direction[1] - 1
        direction[2] = direction[2] - 1

        directions.append(direction)

    input_crates = crates
    input_directions = directions

def move_crates(stacks, directions):
    n_moves = directions[0]
    origin = directions[1]
    destination = directions[2]

    for i in range(n_moves):
        target = stacks[origin].pop()
        stacks[destination].append(target)

    return stacks

def move_crates_maintain_order(stacks, directions):
    n_moves = directions[0]
    origin = directions[1]
    destination = directions[2]

    target = stacks[origin][-n_moves:]

    stacks[origin] = stacks[origin][:-n_moves]
    stacks[destination].extend(target)

    return stacks
        
# Print results depending on the question (1 or 2)
match question:
    case "1":
        stacks = input_crates
        for d in input_directions:
            stacks = move_crates(stacks, d)
            
        result = ""

        for s in stacks:
            result = result + s.pop()

        print(result)

    case "2":
        stacks = input_crates
        for d in input_directions:
            stacks = move_crates_maintain_order(stacks, d)
            
        result = ""

        for s in stacks:
            result = result + s.pop()

        print(result)