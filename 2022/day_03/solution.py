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

# Take a rugsack, parse values, and split into compartments
def split_into_compartments(rugsack):
    rugsack_parsed = []

    for i in rugsack:
        rugsack_parsed.append(parse_letter_to_value(i))

    full = len(rugsack)
    half = int(full / 2)

    compartment_1 = rugsack_parsed[0:half]
    compartment_2 = rugsack_parsed[half:full]

    return([compartment_1, compartment_2])

def find_intersection_compartments(rugsack):
    compartment_1 = rugsack[0]
    compartment_2 = rugsack[1]

    intersection = set(compartment_1).intersection(compartment_2)
    return intersection


# Print results depending on the question (1 or 2)
match question:
    case "1":
        rugsack = split_into_compartments(input[0])

        result = 0

        for rs in input:
            rugsack = split_into_compartments(rs)
            intersection = find_intersection_compartments(rugsack)

            result = result + max(intersection)
        
        print(result)



    case "2":
        print(0)