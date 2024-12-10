import argparse
import logging
import sys


def pad_map(input: list):
    padding_line = "".join(["." for n in range(len(input[0]))]) + ".."
    padded_map = [padding_line]

    for line in input:
        line = "." + line + "."
        padded_map.append(line)

    padded_map.append(padding_line)

    # logging.debug(padded_map)

    return padded_map


def digit_with_adjacent_symbol(input_map: list, coordinate: list):
    ignored_chars = "0123456789."
    y, x = coordinate
    if input_map[y][x] not in "0123456789":
        return False
    elif input_map[y - 1][x - 1] not in ignored_chars:
        return True
    elif input_map[y - 1][x] not in ignored_chars:
        return True
    elif input_map[y - 1][x + 1] not in ignored_chars:
        return True
    elif input_map[y][x - 1] not in ignored_chars:
        return True
    elif input_map[y][x + 1] not in ignored_chars:
        return True
    elif input_map[y + 1][x - 1] not in ignored_chars:
        return True
    elif input_map[y + 1][x] not in ignored_chars:
        return True
    elif input_map[y + 1][x + 1] not in ignored_chars:
        return True
    else:
        return False


def mapped_engine_adjacencies(input_map: list):
    padded_map = pad_map(input_map)
    mapped_engine_adjacencies = []
    for x in range(1, len(padded_map[0]) - 1):
        row = []
        for y in range(1, len(padded_map) - 1):
            row.append(digit_with_adjacent_symbol(padded_map, [x, y]))
        mapped_engine_adjacencies.append(row)

    return mapped_engine_adjacencies


def solve_1(input: list):
    adjacencies = mapped_engine_adjacencies(input)

    result = []
    for y, line in enumerate(input):
        part = ""
        has_adjaceny = False
        for x, char in enumerate(line):
            if char.isdigit():
                part += char
                has_adjaceny = max(adjacencies[y][x], has_adjaceny)
            else:
                if has_adjaceny:
                    result.append(int(part))
                part = ""
                has_adjaceny = False

        if has_adjaceny:
            result.append(int(part))

    return sum(result)


def find_gears(input_map: list):
    for y, line in enumerate(input_map):
        for x, char in enumerate(line):
            if char == "*":
                yield (x, y)


def find_adjacent_parts_for_gear_old(input_map: list, coordinate: tuple):
    padded_map = pad_map(input_map)
    gear_x = coordinate[0] + 1
    gear_y = coordinate[1] + 1

    # logging.debug(["Gear",gear_x, gear_y])

    for y in range(gear_y - 1, gear_y + 2):
        x_offset = 0
        for x in range(gear_x - 1, gear_x + 2):
            if x_offset > 0:
                x_offset -= 1
                continue
            elif padded_map[y][x].isdigit():
                machine_part = padded_map[y][x]
                x_offset = 1
                left_end = right_end = False
                while x - x_offset > 0 and x + x_offset < len(padded_map[0]) - 1:
                    if padded_map[y][x - x_offset].isdigit() and not left_end:
                        machine_part = padded_map[y][x - x_offset] + machine_part
                    else:
                        left_end = True
                    if padded_map[y][x + x_offset].isdigit() and not right_end:
                        machine_part = machine_part + padded_map[y][x + x_offset]
                    else:
                        right_end = True
                    x_offset += 1
                yield machine_part


def find_adjacent_parts_for_gear(input_map: list, coordinate: tuple):
    padded_map = pad_map(input_map)
    gear_x = coordinate[0] + 1
    gear_y = coordinate[1] + 1

    rows = []
    rows.append(padded_map[gear_y - 1][gear_x - 3 : gear_x + 4])
    rows.append(padded_map[gear_y][gear_x - 3 : gear_x + 4])
    rows.append(padded_map[gear_y + 1][gear_x - 3 : gear_x + 4])

    parsed = []

    for row in rows:
        parsed_row = ""
        for i, char in enumerate(row):
            if i == 0:
                if row[1].isnumeric() and row[2].isnumeric():
                    parsed_row = parsed_row + char
                else:
                    parsed_row = parsed_row + "."
            elif i == 1:
                if row[2].isnumeric():
                    parsed_row = parsed_row + char
                else:
                    parsed_row = parsed_row + "."
            elif i in [2, 3, 4]:
                parsed_row = parsed_row + char
            elif i == 5:
                if row[4].isnumeric():
                    parsed_row = parsed_row + char
                else:
                    parsed_row = parsed_row + "."
            elif i == 6:
                if row[4].isnumeric() and row[5].isnumeric():
                    parsed_row = parsed_row + char
                else:
                    parsed_row = parsed_row + "."

        parsed.append(parsed_row)

    for line in parsed:
        part = ""
        for char in line:
            if char.isdigit():
                part += char
            elif len(part) > 0:
                yield int(part)
                part = ""

        if len(part) > 0:
            yield int(part)


def solve_2(input: list):
    gears = list(find_gears(input))

    result = 0
    for gear in gears:
        parts = list(find_adjacent_parts_for_gear(input, gear))
        logging.debug(f"Gear on line {gear[1]+1} at pos {gear[0]+1} has {parts}")
        if len(parts) == 2:
            result += parts[0] * parts[1]

    return result


if __name__ == "__main__":
    # Parse CLI arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--question", required=True)
    parser.add_argument("-i", "--input", required=False, default="input.txt")
    args = parser.parse_args()

    input_file = args.input
    question = args.question

    # Read input
    with open(input_file) as f:
        input = list(f.read().splitlines())

    # Set up logging
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    root.addHandler(handler)

    logging.info(f"Question {question} with input {input_file}")

    if question == "1":
        solution = solve_1(input)
        logging.info(f"Found solution: {solution}")
    elif question == "2":
        solution = solve_2(input)
        logging.info(f"Found solution: {solution}")
    else:
        logging.error("Select either question 1 or 2")
