with open("input.txt") as f:
    input = f.read().splitlines()

heights = []

for line in input:
    x = []
    for digit in line:
        x.append(int(digit))

    heights.append(x)


# X and Y are swapped in two dimensional array
# Use dedicated function to avoid confusion
def get_value_coordinate(map, coordinate):
    x = coordinate[0]
    y = coordinate[1]

    if x < 0 or y < 0:
        # We hit a wall
        return 100
    else:
        return map[y][x]


def get_adjacent_value(map, coordinate, direction):
    x = coordinate[0]
    y = coordinate[1]

    adjacent_value = 100

    try:
        if direction == "north":
            adjacent_value = get_value_coordinate(map, [x, y - 1])
        elif direction == "south":
            adjacent_value = get_value_coordinate(map, [x, y + 1])
        elif direction == "east":
            adjacent_value = get_value_coordinate(map, [x + 1, y])
        elif direction == "west":
            adjacent_value = get_value_coordinate(map, [x - 1, y])
    except:
        # We hit a wall
        return 100

    return adjacent_value


def get_is_lowpoint(map, coordinate):
    x = coordinate[0]
    y = coordinate[1]
    directions = ["north", "south", "east", "west"]
    value_coordinate = get_value_coordinate(map, [x, y])
    is_lowpoint = True

    for dir in directions:
        adjacent_value = get_adjacent_value(map, coordinate, dir)

        # If we can find an adjacent point with a lower or equal value, this is not a low point
        if adjacent_value <= value_coordinate:
            is_lowpoint = False
            break

    return is_lowpoint


def get_larger_neighbours(map, coordinate):
    x = coordinate[0]
    y = coordinate[1]
    directions = ["north", "south", "east", "west"]
    value_coordinate = get_value_coordinate(map, [x, y])

    larger_neighbours = []

    for dir in directions:
        adjacent_value = get_adjacent_value(map, coordinate, dir)

        if adjacent_value >= value_coordinate and adjacent_value not in (9, 100):
            if dir == "north":
                larger_neighbours.append([x, y - 1])
            elif dir == "south":
                larger_neighbours.append([x, y + 1])
            elif dir == "east":
                larger_neighbours.append([x + 1, y])
            elif dir == "west":
                larger_neighbours.append([x - 1, y])

    return larger_neighbours


def get_basin_size(map, low_point):
    basin_size = 1
    to_visit = get_larger_neighbours(map, low_point)
    have_visited = []

    while len(to_visit) > 0:
        coordinate = to_visit[0]

        if coordinate not in have_visited:
            to_visit.extend(get_larger_neighbours(map, coordinate))
            have_visited.append(coordinate)

        to_visit.pop(0)

    basin_size += len(have_visited)

    return basin_size


low_points = []
for y, col in enumerate(heights):
    for x, val in enumerate(col):
        coordinate = [x, y]
        value = get_value_coordinate(heights, coordinate)
        if get_is_lowpoint(heights, coordinate):
            low_points.append(coordinate)

basin_sizes = []
for lp in low_points:
    basin_sizes.append(get_basin_size(heights, lp))

basin_sizes.sort(reverse=True)
print(basin_sizes)
