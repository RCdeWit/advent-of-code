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

# Change a letter to a value (a-z: 1-26; A-Z:27-52)
def parse_letter_to_value(letter):
    ascii = ord(letter)

    if 65 <= ascii <= 90:
        # Upper case
        return ascii - 38
    elif 97 <= ascii <= 122:
        # Lower case
        return ascii - 96
    else:
        print(f"Invalid letter: {letter}")

def parse_rugsack(rugsack):
    rugsack_parsed = []

    for i in rugsack:
        rugsack_parsed.append(parse_letter_to_value(i))

    return rugsack_parsed

# Take a rugsack, parse values, and split into compartments
def split_into_compartments(rugsack):
    full = len(rugsack)
    half = int(full / 2)

    compartment_1 = rugsack[0:half]
    compartment_2 = rugsack[half:full]

    return([compartment_1, compartment_2])

def find_intersection_compartments(compartment_1, compartment_2):
    intersection = set(compartment_1).intersection(compartment_2)
    return intersection


# Print results depending on the question (1 or 2)
match question:
    case "1":
        result = 0

        for rs in input:
            rugsack = parse_rugsack(rs)
            rugsack = split_into_compartments(rugsack)
            intersection = find_intersection_compartments(rugsack[0], rugsack[1])

            result = result + max(intersection)
        
        print(result)

    case "2":
        result = 0
        rugsack_list = []

        for ln in input:
            rugsack_list.append(parse_rugsack(ln))

        # Treat lines in blocks of three
        i = 0
        while i < len(rugsack_list):
            # First find intersection between 1 and 2
            intersection = find_intersection_compartments(rugsack_list[i], rugsack_list[i+1])
            # Then intersection with previous result and 3
            intersection = find_intersection_compartments(intersection, rugsack_list[i+2])

            result = result + max(intersection)

            # Jump to next block
            i = i + 3

        print(result)