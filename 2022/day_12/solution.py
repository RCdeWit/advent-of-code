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

    # Pad map with borders of height 100
    map = [[100] * (len(input[0]) + 2)]
    for line in input:
        row = [100]
        for char in line:
            row.append(ord(char) - 96)
            if char == "S":
                row[-1] = 0
            elif char == "E":
                row[-1] = 27
        row.append(100)
        map.append(row)
    map.append([100] * (len(input[0]) + 2))


def find_valid_steps(map, location, visited_positions):
    x_loc = location[1]
    y_loc = location[0]

    current_height = map[y_loc][x_loc]

    N = map[y_loc - 1][x_loc]
    S = map[y_loc + 1][x_loc]
    E = map[y_loc][x_loc + 1]
    W = map[y_loc][x_loc - 1]

    result = []

    if N - current_height < 2 and (y_loc - 1, x_loc) not in visited_positions:
        result.append((y_loc - 1, x_loc))
    if S - current_height < 2 and (y_loc + 1, x_loc) not in visited_positions:
        result.append((y_loc + 1, x_loc))
    if E - current_height < 2 and (y_loc, x_loc + 1) not in visited_positions:
        result.append((y_loc, x_loc + 1))
    if W - current_height < 2 and (y_loc, x_loc - 1) not in visited_positions:
        result.append((y_loc, x_loc - 1))

    return result


def find_paths(map, start_location, end_location):
    visited_positions = {start_location: 0}
    queue = [start_location]

    while len(queue) > 0:
        position = queue.pop(0)
        visited_positions

        if position == end_location:
            return visited_positions[position]
        else:
            next_steps = find_valid_steps(map, position, visited_positions.keys())
            queue.extend(next_steps)
            for step in next_steps:
                visited_positions[step] = visited_positions[position] + 1


# Print results depending on the question (1 or 2)
match question:
    case "1":
        # Find starting location on map
        for y, row in enumerate(map):
            map_row = []
            for x, val in enumerate(row):
                map_row.append(-1)
                if val == 0:
                    start_location = (y, x)
                elif val == 27:
                    end_location = (y, x)

        result = find_paths(map, start_location, end_location)

        print(result)

    case "2":
        # Naive approach, but fast enough
        potential_start_locations = []
        for y, row in enumerate(map):
            map_row = []
            for x, val in enumerate(row):
                map_row.append(-1)
                if val in (0, 1):
                    potential_start_locations.append((y, x))
                elif val == 27:
                    end_location = (y, x)

        result = -1
        for start_location in potential_start_locations:
            solution = find_paths(map, start_location, end_location)
            if type(solution) == int:
                if solution < result or result == -1:
                    result = solution

        print(result)
