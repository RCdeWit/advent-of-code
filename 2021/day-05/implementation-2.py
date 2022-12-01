import numpy

# First process input data
with open('input.txt') as f:
    input = f.read().splitlines()

list_of_lines = []

# Parse input: first split into two coordinates, then split into X and Y
for i, line in enumerate(input):
    pos1 = input[i].split(' -> ')[0]
    pos2 = input[i].split(' -> ')[1]

    x1 = int(pos1.split(',')[0])
    y1 = int(pos1.split(',')[1])
    x2 = int(pos2.split(',')[0])
    y2 = int(pos2.split(',')[1])

    list_of_lines.append([[x1, y1], [x2, y2]])

def determine_grid_size(list_of_lines):
    max_x = 0
    max_y = 0

    for line in list_of_lines:
        for p, pos in enumerate(line):
            if line[p][0] > max_x:
                max_x = line[p][0]
            if line[p][1] > max_y:
                max_y = line[p][1]

    return [max_x, max_y]

def draw_line_in_matrix(matrix, line):
    output = matrix

    x1 = line[0][0]
    y1 = line[0][1]
    x2 = line[1][0]
    y2 = line[1][1]

    delta_x = x2 - x1
    delta_y = y2 - y1

    # Horizontal line
    if delta_x == 0:
        length = delta_y
        # Inverted line
        inverted = length < 0
        if inverted:
            length *= -1

        for i in range(length + 1):
            if inverted:
                output[x1][y1 - i] += 1
            else:
                output[x1][y1 + i] += 1

    # Vertical line
    elif delta_y == 0:
        length = delta_x
        # Inverted line
        inverted = length < 0
        if inverted:
            length *= -1

        for i in range(length + 1):
            if inverted:
                output[x1 - i][y1] += 1
            else:
                output[x1 + i][y1] += 1

    # Diagnoal line at 45 degrees
    # This means that the absolute deltas should be equal: one step up/down is one step left/right
    elif abs(delta_x) == abs(delta_y):
        length = abs(delta_x)
        direction = ""
        if delta_y > 0:
            direction += "south"
        else:
            direction += "north"
        if delta_x > 0:
            direction += "-east"
        else:
            direction += "-west"

        for i in range(length + 1):
            if direction == "south-east":
                output[x1 + i][y1 + i] += 1
            elif direction == "south-west":
                output[x1 - i][y1 + i] += 1
            elif direction == "north-east":
                output[x1 + i][y1 - i] += 1
            elif direction == "north-west":
                output[x1 - i][y1 - i] += 1

    return(output)

def count_overlaps_in_matrix(matrix):
    overlaps = 0
    for x, row in enumerate(matrix):
        for y, col in enumerate(matrix[x]):
            if matrix[x][y] >= 2:
                overlaps += 1

    return(overlaps)

# Create empty matrix and start drawing lines
matrix = numpy.zeros((determine_grid_size(list_of_lines)[0]+1, determine_grid_size(list_of_lines)[1]+1))

for line in list_of_lines:
    matrix = draw_line_in_matrix(matrix, line)

print(matrix)
print(count_overlaps_in_matrix(matrix))
