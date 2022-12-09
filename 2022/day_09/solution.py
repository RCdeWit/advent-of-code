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

    parsed = []

    for l in input:
        direction = l.split(" ")[0]
        distance = l.split(" ")[1]

        parsed.append([direction, distance])

    input = parsed


def create_empty_map(width, height):
    map = [[0 for x in range(width)] for y in range(height)] 
    return map

# Take one step at a time, return new map
def move_rope_along_map(map, direction, head=[0, 0], tail=[0,0]):
    head_x = head[1]
    head_y = head[0]
    tail_x = tail[1]
    tail_y = tail[0]

    match direction:
        case "R":
            head_x = head_x + 1
        case "L":
            head_x = head_x - 1
        case "U":
            head_y = head_y + 1
        case "D":
            head_y = head_y - 1

    delta_x = abs(head_x - tail_x)
    delta_y = abs(head_y - tail_y)

    if delta_x > 1 or delta_y > 1:
        match direction:
            case "R":
                tail_x = head_x - 1
                tail_y = head_y
            case "L":
                tail_x = head_x + 1
                tail_y = head_y
            case "U":
                tail_y = head_y - 1
                tail_x = head_x
            case "D":
                tail_y = head_y + 1
                tail_x = head_x

    # map[head_y][head_x] = 1
    map[tail_y][tail_x] = 1

    return(map, [head_y, head_x], [tail_y, tail_x])

# Do it for a sequence of steps
# Trace where the tail has been
def trace_path_rope_along_map(map, input, head, tail):
    for line in input:
            direction = line[0]
            distance = int(line[1])

            for i in range(0, distance):
                result = move_rope_along_map(
                            map=map
                            , direction=direction
                            , head=head
                            , tail=tail
                            )

                map = result[0]
                head = result[1]
                tail = result[2]

    return(map)

def sum_map(map):
    result = 0
    for y in map:
        for x in y:
            result = result + x

    return(result)

# Print results depending on the question (1 or 2)
match question:
    case "1":

        # Not the prettiest, but create a big enough map and start in the middle
        dimensions = 500
        map = create_empty_map(dimensions*2, dimensions*2)
        map[dimensions][dimensions] = 1
        head = [dimensions, dimensions]
        tail = [dimensions, dimensions]

        map = trace_path_rope_along_map(map, input, head, tail)

        # for line in reversed(map):
        #     print(line)

        print(sum_map(map))

    case "2":
        print(2)