import argparse
import re

# Parse CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True)
parser.add_argument("-q", "--question", required=True)
args = parser.parse_args()

input_file = args.input
question = args.question

def get_radius(location_1, location_2):
    return abs(location_1[0] - location_2[0]) + abs(location_1[1] - location_2[1])

# Read input
with open(input_file) as f:
    input = list(f.read().splitlines())

    regex = "^.+x=(-?\d+). y=(-?\d+).+x=(-?\d+), y=(-?\d+)$"

    sensors = {}
    beacons = {}

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

        radius = get_radius([sensor_x, sensor_y], [beacon_x, beacon_y])

        if sensor_x + (radius) > max_x:
            max_x = sensor_x + (radius)
        if beacon_x > max_x:
            max_x = beacon_x
        if sensor_y + (radius) > max_y:
            max_y = sensor_y + (radius)
        if beacon_y > max_y:
            max_y = beacon_y 

        if sensor_x - (radius) < min_x:
            min_x = sensor_x - (radius)
        if beacon_x < min_x:
            min_x = beacon_x
        if sensor_y - (radius) < min_y:
            min_y = sensor_y - (radius)
        if beacon_y < min_y:
            min_y = beacon_y

    for line in input:
        coordinates = re.search(regex, line).groups()

        sensor_x = int(coordinates[0])
        sensor_y = int(coordinates[1])
        beacon_x = int(coordinates[2])
        beacon_y = int(coordinates[3])

        sensors[sensor_x, sensor_y] = get_radius([sensor_x, sensor_y], [beacon_x, beacon_y])
        beacons[beacon_x, beacon_y] = 1

def is_in_radius(point, sensor, radius):
    point_x = point[0]
    point_y = point[1]
    sensor_x = sensor[0]
    sensor_y = sensor[1]

    delta_x = abs(sensor_x - point_x)
    delta_y = abs(sensor_y - point_y)

    return delta_x + delta_y <= radius


# Print results depending on the question (1 or 2)
match question:
    case "1":
        y = 2000000
        covered = 0
        for x in range(min_x, max_x):
            print(x, "/", max_x)
            for s in sensors:
                in_radius = is_in_radius([x, y], s, sensors[s])

                if in_radius:
                    covered = covered + 1
                    break

        beacons_on_line = 0
        for b in beacons:
            if b[1] == y:
                beacons_on_line = beacons_on_line + 1

        print(covered, beacons_on_line)
        print(covered - beacons_on_line)

    case "2":
        print(2)