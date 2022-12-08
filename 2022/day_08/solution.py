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

    tree_map = []

    for line in input:
        tree_line = []
        for digit in line:
            tree_line.append(digit)
        tree_map.append(tree_line)

def determine_visibility_tree(tree_map, tree_x=0, tree_y=0):

    # Edges of map, always visible
    if tree_x == 0 or tree_y == 0 or tree_x == len(tree_map[tree_y] or tree_y == len(tree_map)):
        return True

    tree_height = tree_map[tree_y][tree_x]

    visible_n = True
    visible_s = True
    visible_w = True
    visible_e = True

    for x, x_height in enumerate(tree_map[tree_y]):
        if x_height >= tree_height:
            if x == tree_x:
                None
            elif x < tree_x:
                visible_w = False
            elif x > tree_x:
                visible_e = False
            else:
                print("ERROR: this should never happen")
                exit()

    if visible_w or visible_e:
        return True

    for y, row in enumerate(tree_map):
        y_height = row[tree_x]

        if y_height >= tree_height:
            if y == tree_y:
                None
            elif y < tree_y:
                visible_n = False
            elif y > tree_y:
                visible_s = False
            else:
                print("ERROR: this should never happen")
                exit()

    if visible_n or visible_s:
        return True

    else:
        return False


# Print results depending on the question (1 or 2)
match question:
    case "1":
        count_visible = 0

        for y, row in enumerate(tree_map):
            for x, height in enumerate(row):
                if determine_visibility_tree(tree_map, tree_x=x, tree_y=y):
                    count_visible = count_visible + 1

        print(count_visible)

    case "2":
        print(2)