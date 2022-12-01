with open('input.txt') as f:
    input = f.read().splitlines()

algorithm = ""
for char in input[0]:
    if char == ".":
        algorithm += "0"
    elif char == "#":
        algorithm += "1"

image = []
for line in input[2:]:
    y = []
    for x in line:
        if x == ".":
            y.append(0)
        elif x == "#":
            y.append(1)
    image.append(y)

def get_padding_value(algorithm, oddeven):
    if algorithm[0] == "0":
        return 0
    else:
        if oddeven % 2 == 0:
            return algorithm[-1]
        else:
            return algorithm[0]

def pad_image(image, padding, algorithm, oddeven):
    padding = int(padding)
    pad = get_padding_value(algorithm, oddeven)

    width = len(image[0]) + (padding * 2)
    height = len(image[0]) + (padding * 2)

    output = []
    for i in range(padding):
        output.append([pad] * width)

    for y, row in enumerate(image):
        output_row = []
        for i in range(padding):
            output_row.append(pad)
        for x, val in enumerate(row):
            output_row.append(val)
        for i in range(padding):
            output_row.append(pad)
        output.append(output_row)

    for i in range(padding):
        output.append([pad] * width)

    return(output)

def get_value_coordinate_from_algorithm(image, coordinate, algorithm, pad):
    output = ""
    pos_x = coordinate[0]
    pos_y = coordinate[1]

    for offset_y in range(-1, 2):
        for offset_x in range(-1, 2):
            neighbour_x = pos_x + offset_x
            neighbour_y = pos_y + offset_y

            if neighbour_x < 0 or neighbour_y < 0:
                output += str(pad)
            elif neighbour_x >= len(image[0]) or neighbour_y >= len(image):
                output += str(pad)
            else:
                output += str(image[neighbour_y][neighbour_x])


    algorithm_postion = int(output, 2)
    value = algorithm[algorithm_postion]

    return value


def process_image(image, algorithm, oddeven):
    image = pad_image(image, 5, algorithm, oddeven)
    pad = get_padding_value(algorithm, oddeven)

    output = []
    for y, row in enumerate(image):
        output_row = []
        for x, val in enumerate(row):
            output_row.append(get_value_coordinate_from_algorithm(image, [x, y], algorithm, pad))
        output.append(output_row)

    return output

n_cycles = 50
result = image
for cycle in range(n_cycles):
    result = process_image(result, algorithm, cycle % 2)

count_pixels = 0
for y, row in enumerate(result):
    for x, val in enumerate(row):
        if val == "1":
            count_pixels += 1

print(count_pixels)

# print(int("000000000", 2))
# print(int("111111111", 2))
# print(algorithm[511])
