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

    packets = []
    pair = []
    for i, line in enumerate(input):
        i = i + 1
        if i % 3 == 0:
            packets.append(pair)
            pair = []
        else:
            pair.append(eval(line))

    packets.append(pair)

def compare_pairs(pair):
    left = pair[0]
    right = pair[1]

    # One side ran out of items
    if type(left) == list:
        if len(left) == 0:
            return(True)
        else:
            l = left.pop(0)
    else:
        l = left

    if type(right) == list:
        if len(right) == 0:
            return False
        else:
            r = right.pop(0)
    else:
        r = right

    # Compare ints
    if type(l) == int and type(r) == int:
        if l < r:
            return True
        elif l > r:
            return False
        else:
            return compare_pairs([left, right])

    # Compare list to int
    elif type(l) == int and type(r) == list:
        return compare_pairs([[l], r])
    elif type(l) == list and type(r) == int:
        return compare_pairs([l, [r]])

    # Compare lists
    elif type(l) == list and type(r) == list:
        # One side ran out of items
        if len(l) == 0:
            return True
        elif len(r) == 0:
            return False
        # Items are the same, continue to next
        elif l[0] == r[0]:
            l.pop(0)
            r.pop(0)
            return compare_pairs([l, r])
        # Items are not the same
        else:
            return compare_pairs([l[0], r[0]])

    # This shouldn't happen
    else:
        print("ERROR: this shouldn't happen")
        print(pair, type(l), type(r))

# Print results depending on the question (1 or 2)
match question:
    case "1":
        result = 0
        for i, pair in enumerate(packets):
            if compare_pairs(pair):
                result = result + i + 1

        print(result)
    case "2":
        print(2)