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

        if adjacent_value <= value_coordinate:
            is_lowpoint = False
            break

    return is_lowpoint


total_risk_level = 0
for y, col in enumerate(heights):
    for x, val in enumerate(col):
        coordinate = [x, y]
        value = get_value_coordinate(heights, coordinate)
        if get_is_lowpoint(heights, coordinate):
            total_risk_level += value + 1

print(f"Total risk level: {total_risk_level}")
