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

    # Capture numbers as four groups
    regex = "^(\d+)-(\d+),(\d+)-(\d+)$"

    input_parsed = []

    # Extract number groups from each line, add to list
    for l in input:
        parsed = re.search(regex, l).groups()

        elf_1 = [int(parsed[0]), int(parsed[1])]
        elf_2 = [int(parsed[2]), int(parsed[3])]

        input_parsed.append([elf_1, elf_2])

    input = input_parsed

# See if one section fully contains the other section
def section_fully_contains_other_section(section_1, section_2):
    start_1 = section_1[0]
    end_1 = section_1[1]
    start_2 = section_2[0]
    end_2 = section_2[1]

    if start_1 <= start_2 and end_1 >= end_2:
        return True
    elif start_2 <= start_1 and end_2 >= end_1:
        return True
    else:
        return False

# See if two sections overlap
def section_partially_contains_other_section(section_1, section_2):
    start_1 = section_1[0]
    end_1 = section_1[1]
    start_2 = section_2[0]
    end_2 = section_2[1]

    if start_2 > end_1:
        return False
    elif start_1 > end_2:
        return False
    else:
        return True


# Print results depending on the question (1 or 2)
match question:
    case "1":
        count = 0

        for pair in input:
            count = count + section_fully_contains_other_section(pair[0], pair[1])

        print(count)

    case "2":
        count = 0

        for pair in input:
            count = count + section_partially_contains_other_section(pair[0], pair[1])

        print(count)