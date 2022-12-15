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

    regex = "^.+x=(-?\d+). y=(-?\d+).+x=(-?\d+), y=(-?\d+)$"

    pairs = {}

    min_x = float('inf')
    max_x = -float('inf')
    min_y = float('inf')
    max_y = -float('inf')

    for line in input:
        coordinates = re.search(regex, line).groups()

        sensor_x = int(coordinates[0])
        sensor_y = int(coordinates[1])
        beacon_x = int(coordinates[2])
        beacon_y = int(coordinates[3])

        if sensor_x > max_x:
            max_x = sensor_x
        if beacon_x > max_x:
            max_x = beacon_x
        if sensor_y > max_y:
            max_y = sensor_y
        if beacon_y > max_y:
            max_y = beacon_y

        if sensor_x < min_x:
            min_x = sensor_x
        if beacon_x < min_x:
            min_x = beacon_x
        if sensor_y < min_y:
            min_y = sensor_y
        if beacon_y < min_y:
            min_y = beacon_y

    for line in input:
        coordinates = re.search(regex, line).groups()

        sensor_x = int(coordinates[0])
        sensor_y = int(coordinates[1])
        beacon_x = int(coordinates[2])
        beacon_y = int(coordinates[3])

        pairs[sensor_x-min_x, sensor_y-min_y] = [beacon_x-min_x, beacon_y-min_y]

    max_x = max_x - min_x
    max_y = max_y - min_y
    min_x = 0
    min_y = 0

    input = pairs

def create_map(input, min_x, max_x, min_y, max_y):
    map = [ [ "." for x in range( max_x + 1 ) ] for y in range( max_y + 1 ) ]

    for i, key in enumerate(list(input.keys())):
        sensor_x = key[0]
        sensor_y = key[1]
        beacon_x = input[key][0]
        beacon_y = input[key][1]

        map[sensor_y][sensor_x] = "S"
        map[beacon_y][beacon_x] = "B"

        delta_x = abs(sensor_x - beacon_x)
        delta_y = abs(sensor_y - beacon_y)

        delta_total = delta_x + delta_y
        for dx in range(-delta_total, delta_total + 1):
            for dy in range(-delta_total, delta_total + 1):

                if abs(dx) + abs(dy) <= delta_total:
                    # Out of bounds check
                    if sensor_y+dy >= 0 and sensor_y+dy < len(map) and sensor_x+dx >= 0 and sensor_x+dx < len(map[0]):

                        # Draw range
                        if map[sensor_y+dy][sensor_x+dx] == ".":
                            map[sensor_y+dy][sensor_x+dx] = "#"

    return map
        
def draw_map(map):
    for y, row in enumerate(map):
        line = ""
        count = 0
        for character in row:
            line = line + str(character)
            if character == "#":
                count = count + 1
        print(str(y).zfill(2), line, "- Count:", count)

def count_characters(array, line, character="#"):
    result = 0
    for c in array[line]:
        if c == character:
            result = result + 1

    return result


# Print results depending on the question (1 or 2)
match question:
    case "1":
        map = create_map(input, min_x, max_x, min_y, max_y)
        draw_map(map)

        print(count_characters(map, 10, "#"))

    case "2":
        print(2)