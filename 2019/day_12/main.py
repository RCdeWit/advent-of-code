import argparse
import logging
import sys
import time
import re

from math import gcd
from functools import reduce

def parse_input(puzzle_input: list) -> list:
    pattern = re.compile(r'x=(-?\d+), y=(-?\d+), z=(-?\d+)')
    for line in puzzle_input:
        match = pattern.search(line)
        x, y, z = map(int, match.groups())
        yield x, y, z

def calculate_gravity(moon_1: tuple, moon_2: tuple) -> tuple:
    m1x, m1y, m1z = moon_1
    m2x, m2y, m2z = moon_2

    def compare_values(a, b) -> int:
        if a == b:
            return 0
        elif a < b:
            return 1
        elif a > b:
            return -1
        else:
            raise ValueError("Something has gone very wrong.")

    gx = compare_values(m1x, m2x)
    gy = compare_values(m1y, m2y)
    gz = compare_values(m1z, m2z)

    return (gx, gy, gz)

def calculate_all_gravities(moons: list) -> list:
    for moon, _ in moons:
        gravity = [0, 0, 0]
        for other, _ in moons:
            if moon == other:
                pass
            else:
                gx, gy, gz = calculate_gravity(moon, other)
                gravity[0] += gx
                gravity[1] += gy
                gravity[2] += gz

        yield gravity

def time_step(moons: list) -> list:
    gravities = list(calculate_all_gravities(moons))
    for i, moon in enumerate(moons):
        x, y, z = moon[0]
        vx, vy, vz = moon[1]
        vx += gravities[i][0]
        vy += gravities[i][1]
        vz += gravities[i][2]

        yield [(x + vx, y + vy, z + vz), (vx, vy, vz)]

def calculate_energy(moon: list) -> int:
    position, velocity = moon
    potential_energy = abs(position[0]) + abs(position[1]) + abs(position[2])
    kinetic_energy = abs(velocity[0]) + abs(velocity[1]) + abs(velocity[2])

    return potential_energy * kinetic_energy


def find_cycle_length(moons, dim_index):
    initial_state = [(moon[0][dim_index], moon[1][dim_index]) for moon in moons]
    steps = 0
    while True:
        moons = list(time_step(moons))
        steps += 1
        current_state = [(moon[0][dim_index], moon[1][dim_index]) for moon in moons]
        if current_state == initial_state:
            return steps

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def lcm_multiple(numbers):
    return reduce(lcm, numbers)


def solve_1(puzzle_input: list) -> str:
    moons = list(tuple(parse_input(puzzle_input)))
    moons = [[loc, (0, 0, 0)] for loc in moons]
    
    for _ in range(1000):
        moons = list(time_step(moons))
        # logging.debug(f"After {step} steps: ")
        # logging.debug(moons)

    energy = list(map(calculate_energy, moons))
    return sum(energy)


def solve_2(puzzle_input: list) -> str:
    moons = list(tuple(parse_input(puzzle_input)))
    moons = [[loc, (0, 0, 0)] for loc in moons]

    # Find cycle lengths for x, y, and z dimensions
    cycle_x = find_cycle_length(moons, 0)
    cycle_y = find_cycle_length(moons, 1)
    cycle_z = find_cycle_length(moons, 2)

    # Compute the overall cycle length
    total_cycle = lcm_multiple([cycle_x, cycle_y, cycle_z])
    return total_cycle



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
        puzzle_input = list(f.read().splitlines())

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
    start = time.time()

    if question == "1":
        solution = solve_1(puzzle_input)
        logging.info(f"Found solution: {solution} (in {time.time()-start} seconds)")
    elif question == "2":
        solution = solve_2(puzzle_input)
        logging.info(f"Found solution: {solution} (in {time.time()-start} seconds)")
    else:
        logging.error("Select either question 1 or 2")
