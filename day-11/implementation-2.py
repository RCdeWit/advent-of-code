with open('input.txt') as f:
    input = f.read().splitlines()

octopuses = []

for line in input:
    x = []
    for digit in line:
        x.append(int(digit))

    octopuses.append(x)

def get_value_coordinate(map, coordinate):
    x = coordinate[0]
    y = coordinate[1]

    if x < 0 or y < 0:
        return None
    elif x > len(map[0]) - 1 or y > len(map) - 1:
        return None
    else:
        return map[y][x]

def set_value_coordinate(map, coordinate, mutation):
    x = coordinate[0]
    y = coordinate[1]

    if x < 0 or y < 0:
        return map
    elif x > len(map[0]) - 1 or y > len(map) - 1:
        return map
    elif map[y][x] == -1:
        return map
    else:
        map[y][x] += mutation

    return map

total_flashes = 0
def flash_octopus(map):
    output = map
    count_flashes = 0

    for y, row in enumerate(output):
        for x, val in enumerate(row):
            if val >= 10:

                # Change adjacent values
                # Bit lazy but easier than the double loop
                output = set_value_coordinate(output, [x-1, y-1], 1)
                output = set_value_coordinate(output, [x, y-1], 1)
                output = set_value_coordinate(output, [x+1, y-1], 1)

                output = set_value_coordinate(output, [x-1, y], 1)
                output = set_value_coordinate(output, [x+1, y], 1)

                output = set_value_coordinate(output, [x-1, y+1], 1)
                output = set_value_coordinate(output, [x, y+1], 1)
                output = set_value_coordinate(output, [x+1, y+1], 1)

                output[y][x] = -1
                count_flashes += 1

    return([output, count_flashes])

def check_all_flashed(map):
    for y, row in enumerate(map):
        for x, val in enumerate(row):
                if val >= 10:
                    return False

    return True

def check_all_flashed_now(map):
    for y, row in enumerate(map):
        for x, val in enumerate(row):
                if val != -1:
                    return False

    return True

def set_flashed_to_0(map):
    for y, row in enumerate(map):
        for x, val in enumerate(row):
            if val == -1:
                map[y][x] = 0

    return map



n_cycles = 1000
total_flashes = 0
for i in range(n_cycles):
    for y, row in enumerate(octopuses):
        for x, val in enumerate(row):
            set_value_coordinate(octopuses, [x, y], 1)

    while not check_all_flashed(octopuses):
        flash = flash_octopus(octopuses)
        octopuses = flash[0]
        total_flashes += flash[1]
        if check_all_flashed_now(octopuses):
            print(i+1)
            exit()

    octopuses = set_flashed_to_0(octopuses)

# print(total_flashes
