import argparse
import logging
import sys

def parse_input(input: list):
    seeds = [int(seed) for seed in input[0].split(":")[1][1:].split(" ")]
    # logging.debug(seeds)

    maps = {}
    map_name = map_ranges = None

    for line in input[2:]:
        if len(line) == 0:
            maps[map_name] = map_ranges
        elif ":" in line:
            map_name = line.split(" ")[0]
            map_ranges = {}
        else:
            dest_min = int(line.split(" ")[0])
            source_min = int(line.split(" ")[1])
            range_length = int(line.split(" ")[2])
            source_max = source_min + range_length - 1
            offset = dest_min - source_min

            map_ranges[tuple([source_min, source_max])] = offset
    maps[map_name] = map_ranges

    return seeds, maps

def parse_seeds_2(input: str):
    seeds = [int(seed) for seed in input.split(":")[1][1:].split(" ")]
    ranges = []
    i = 0
    while i < len(seeds):
        ranges.append(tuple([seeds[i], seeds[i] + seeds[i+1]]))
        i += 2

    return ranges


def map_source_to_dest(origin: int, map_name: str, maps: dict):
    map_current = maps[map_name]
    for key, offset in map_current.items():
        if origin in range(key[0], key[1]+1):
            return origin + offset
    
    return origin

def map_source_to_dest_2(origin: tuple, map_name: str, maps: dict):
    map_current = maps[map_name]
    for key, offset in map_current.items():
        # logging.debug(f"Finding overlap seed range {origin} in {key}")
        if origin[0] >= key[0] and origin[1] <= key[1]:
            # logging.debug(f"COMPLETE: {tuple([origin[0] + offset, origin[1] + offset])}")
            yield tuple([origin[0] + offset, origin[1] + offset])
            origin = (-1, -1)
        elif origin[1] < key[0] or origin[0] > key[1]:
            # logging.debug("NO MATCH")
            continue
        elif origin[0] >= key[0]:
            # logging.debug("TO RIGHT")
            yield tuple([origin[0] + offset, key[1] + offset])
            origin = tuple([key[1] + 1, origin[1]])
            map_source_to_dest_2(origin, map_name, maps)
        elif origin[1] <= key[1]:
            # logging.debug("TO LEFT")
            yield tuple([key[0] + offset, origin[1] + offset])
            origin = tuple([origin[0], key[0]-1])
            map_source_to_dest_2(origin, map_name, maps)

    if origin != (-1, -1):
        yield origin

def seeds_to_locations(seeds: list, maps: dict):
    destinations = []
    for seed in seeds:
        soil = map_source_to_dest(seed, "seed-to-soil", maps)
        fertilizer = map_source_to_dest(soil, "soil-to-fertilizer", maps)
        water = map_source_to_dest(fertilizer, "fertilizer-to-water", maps)
        light = map_source_to_dest(water, "water-to-light", maps)
        temperature = map_source_to_dest(light, "light-to-temperature", maps)
        humidity = map_source_to_dest(temperature, "temperature-to-humidity", maps)
        location = map_source_to_dest(humidity, "humidity-to-location", maps)

        destinations.append(location)
        # logging.debug([seed, soil, fertilizer, water, light, temperature, humidity, location])

    return destinations

def solve_1(input):
    seeds, maps = parse_input(input)
    destinations = seeds_to_locations(seeds, maps)
    return min(destinations)

def solve_2(input):
    seeds, maps = parse_input(input)
    seeds = parse_seeds_2(input[0])

    seed_ranges = seeds
    destinations = []
    for map_name in maps:
        for sr in seed_ranges:
            destination = list(map_source_to_dest_2(sr, map_name, maps))
            destinations += destination
        seed_ranges = destinations
        destinations = []

        # logging.debug(f"{map_name}: {seed_ranges}")

    return sorted([sr[0] for sr in seed_ranges])[0]

if __name__ == '__main__':
     # Parse CLI arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--question", required=True)
    parser.add_argument("-i", "--input", required=False, default='input.txt')
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

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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