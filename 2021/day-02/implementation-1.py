def change_position(starting_position, direction, distance):
    updated_position = starting_position

    if direction == "forward":
        updated_position["x-pos"] += distance
    elif direction == "down":
        updated_position["z-pos"] += distance
    elif direction == "up":
        updated_position["z-pos"] -= distance
    else:
        print(f"Error: direction '{direction}' is undefined.")

    return updated_position


with open("input.txt") as f:
    directions = list(f.read().splitlines())

position = {"x-pos": 0, "y-pos": 0, "z-pos": 0}

for dir in directions:
    command = dir.split(" ")
    position = change_position(position, command[0], int(command[1]))

print(position)
