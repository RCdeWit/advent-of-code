from queue import PriorityQueue

with open("input.txt") as f:
    input = f.read().splitlines()

map = []
for line in input:
    x = []
    for digit in line:
        x.append(int(digit))
    map.append(x)


def dijkstra(map):
    width = len(map[0])
    length = len(map)

    costs = []
    for y in range(len(map)):
        row = []
        for x in range(len(map[0])):
            row.append(float("inf"))
        costs.append(row)

    # Use a dictionary to avoid double entries
    to_visit = {(0, 0): True}

    while len(to_visit) > 0:
        position = list(to_visit.keys())[0]
        x = position[0]
        y = position[1]

        neighbours = {}

        if x > 0:
            neighbours["left"] = [costs[y][x - 1], -1, 0]
        if x < width - 1:
            neighbours["right"] = [costs[y][x + 1], 1, 0]
        if y > 0:
            neighbours["up"] = [costs[y - 1][x], 0, -1]
        if y < length - 1:
            neighbours["down"] = [costs[y + 1][x], 0, 1]

        old_value = costs[y][x]
        new_value = neighbours[min(neighbours, key=neighbours.get)][0] + map[y][x]

        if x == 0 and y == 0:
            new_value = 0
            costs[y][x] = new_value
        else:
            costs[y][x] = min(old_value, new_value)

        for n in neighbours:
            x_offset = neighbours[n][1]
            y_offset = neighbours[n][2]

            neighbours_old_value = costs[y + y_offset][x + x_offset]
            neighbours_new_value = map[y + y_offset][x + x_offset] + new_value

            if neighbours_new_value < neighbours_old_value:
                to_visit[(x + x_offset, y + y_offset)] = True

        # Remove current coordinate from list
        del to_visit[position]

    return costs


print(dijkstra(map)[-1][-1])
