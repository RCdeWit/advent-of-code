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

    # First search North and South
    for x, x_height in enumerate(tree_map[tree_y]):
        if x_height >= tree_height:
            if x == tree_x:
                # At this point we've searched everything to the West
                # If it's visible from that direction, this tree is eliminated
                if visible_w:
                    return True
                else:
                    # Continue searching East
                    None
            elif x < tree_x:
                visible_w = False
            elif x > tree_x:
                visible_e = False
            else:
                print("ERROR: this should never happen")
                exit()

    if visible_e:
        return True

    # Then from West to East
    for y, row in enumerate(tree_map):
        y_height = row[tree_x]

        if y_height >= tree_height:
            if y == tree_y:
                # At this point we've searched everything to the North
                # If it's visible from that direction, this tree is eliminated
                if visible_n:
                    return True
                else:
                    # Continue searching South
                    None
            elif y < tree_y:
                visible_n = False
            elif y > tree_y:
                visible_s = False
            else:
                print("ERROR: this should never happen")
                exit()

    if visible_s:
        return True
    else:
        return False

def determine_scenic_score_tree(tree_map, tree_x=0, tree_y=0):
    tree_height = tree_map[tree_y][tree_x]

    visible_n = 0
    visible_s = 0
    visible_w = 0
    visible_e = 0

    # First search North and South
    for x, x_height in enumerate(tree_map[tree_y]):
        if x == tree_x:
            None
        elif x < tree_x:
            if x_height >= tree_height:
                visible_w = 0
            visible_w = visible_w + 1
        elif x > tree_x:
            visible_e = visible_e + 1
            if x_height >= tree_height:
                break
        else:
            print("ERROR: this should never happen")
            exit()

    # Then from West to East
    for y, row in enumerate(tree_map):
        y_height = row[tree_x]

        if y == tree_y:
            None
        elif y < tree_y:
            if y_height >= tree_height:
                visible_n = 0
            visible_n = visible_n + 1
        elif y > tree_y:
            visible_s = visible_s + 1
            if y_height >= tree_height:
                break
        else:
            print("ERROR: this should never happen")
            exit()

    return(visible_n * visible_e * visible_s * visible_w)

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
        score_list = []

        for y, row in enumerate(tree_map):
            for x, height in enumerate(row):
                scenic_score = determine_scenic_score_tree(tree_map, tree_x=x, tree_y=y)
                score_list.append(scenic_score)

        print(max(score_list))