import argparse
from copy import deepcopy

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

    parsed = []
    for line in input:
        path = []
        for coordinate in line.split(" -> "):
            path.append(list(map(int, coordinate.split(","))))
        parsed.append(path)

    input = parsed

def create_map(input):
    min_x = float('inf')
    max_x = 0
    max_y = 0

    # Find dimensions
    for line in input:
        for coordinate in line:
            if coordinate[0] > max_x:
                max_x = coordinate[0]
            if coordinate[0] < min_x:
                min_x = coordinate[0]
            if coordinate[1] > max_y:
                max_y = coordinate[1]

    # Create empty map
    map = []
    for y in range(max_y+1):
        line = []
        for x in range(max_x+1):
            line.append(".")
        map.append(line)

    for line in input:
        for i, coordinate in enumerate(line[:-1]):
            # Horizontal line
            if coordinate[1] == line[i+1][1]:
                y = coordinate[1]
                x_min = min(coordinate[0], line[i+1][0])
                x_max = max(coordinate[0], line[i+1][0])
                for x in range(x_min, x_max+1):
                    map[y][x] = "#"
            # Vertical line
            if coordinate[0] == line[i+1][0]:
                x = coordinate[0]
                y_min = min(coordinate[1], line[i+1][1])
                y_max = max(coordinate[1], line[i+1][1])
                for y in range(y_min, y_max+1):
                    map[y][x] = "#"

    return map

def drop_sand(map, current_position):
    x = current_position[0]
    y = current_position[1]

    void = False

    if y + 1 != len(map):
        # Drop straight down
        if map[y+1][x] == ".":
            return drop_sand(map, [x, y+1])
        elif map[y+1][x-1] == ".":
            if x > 0:
                return drop_sand(map, [x-1, y+1])
        elif map[y+1][x+1] == ".":
            if x < len(map[y]):
                return drop_sand(map, [x+1, y+1])
        map[y][x] = "o"
    
    else:
        void = True

    return(map, void)

def draw_map(map):
    for i, y in enumerate(map):
        line = ""
        for x, character in enumerate(y):
            if x > 490:
                line = line + character
        
        print(i, line)

# Print results depending on the question (1 or 2)
match question:
    case "1":
        map = create_map(input)

        done = False
        i = -1
        while not done:
            result = drop_sand(map, [500, 0])
            i = i+1
            map = result[0]
            done = result[1]

            print(i, done)
        print(i)
    case "2":
        print(2)