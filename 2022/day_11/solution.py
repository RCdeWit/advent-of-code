import argparse
from pathlib import Path
import math


# Parse CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True)
parser.add_argument("-q", "--question", required=True)
args = parser.parse_args()

input_file = args.input
question = args.question

# Read input
with open(input_file) as f:
    input = list(f.read().splitlines())

monkeys = {}
monkey = 0
for line in input:
    if line == "":
        monkey = monkey + 1
    
    elif line.startswith("  "):
        line = line[2:]
        key = line.split(":")[0]
        value = line.split(":")[1][1:]

        if key == "Starting items":
            value = [int(x) for x in value.strip(" ").split(",")]
        elif key == "Test":
            value = int(value.split(" ")[-1])
        elif key == "Operation":
            value = [value.split(" ")[-2], value.split(" ")[-1]]
        else:
            key = key.strip(" ")
            value = int(value.split(" ")[-1])

        monkeys[monkey][key] = value
        monkeys[monkey]['Activities'] = 0

    elif line.startswith(""):
        monkeys[monkey] = {}

def inspect_item(item, operation):
    int_1 = item
    if operation[1] == "old":
        int_2 = item
    else:
        int_2 = int(operation[1])

    if operation[0] == "+":
        result = int_1 + int_2
    elif operation[0] == "-":
        result = int_1 - int_2
    elif operation[0] == "*":
        result = int_1 * int_2
    else:
        print("This shouldn't happen")
        exit

    return result

def process_turn(monkeys, current_monkey, lower_stress, supermod):

    operation = monkeys[current_monkey]['Operation']
    if_true = monkeys[current_monkey]['If true']
    if_false = monkeys[current_monkey]['If false']

    for value in monkeys[current_monkey]['Starting items']:
        new_value = inspect_item(value, operation)
        monkeys[current_monkey]['Activities'] += 1
        new_value = worry_level(new_value, lower_stress, supermod)

        if new_value % monkeys[current_monkey]['Test'] == 0:
            monkeys[if_true]['Starting items'].append(new_value)
        else:
            monkeys[if_false]['Starting items'].append(new_value)

    monkeys[current_monkey]['Starting items'] = []

    return(monkeys)

def process_round(monkeys, lower_stress, supermod):
    for monkey in monkeys:
        monkeys = process_turn(monkeys, monkey, lower_stress, supermod)

    return monkeys

def worry_level(level, lower_stress, supermod):
    if lower_stress:
        return math.floor(level / 3)
    elif not lower_stress:
        return (level % supermod)


# Print results depending on the question (1 or 2)
match question:
    case "1":
        for r in range(20):
            monkeys = process_round(monkeys, lower_stress=True, supermod=1)

        result = []
        for monkey in monkeys:
            result.append(monkeys[monkey]['Activities'])

        result = sorted(result)

        print(result[-1] * result[-2])
    case "2":
        supermod = 1
        for m in monkeys:
            supermod = supermod * monkeys[m]['Test']

        for r in range(10000):
            monkeys = process_round(monkeys, lower_stress=False, supermod=supermod)

        result = []
        for monkey in monkeys:
            result.append(monkeys[monkey]['Activities'])

        result = sorted(result)
        print(result[-1] * result[-2])