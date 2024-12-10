import argparse

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


# Sum lines of calories by elf
def sum_elves(input):
    sum = 0
    elves = []

    for l in input:
        if l == "":
            elves.append(sum)
            sum = 0
        else:
            sum = sum + int(l)

    elves.append(sum)
    return elves


# Find highest calory elf
def find_highest_calory_elf(elves):
    index_max_calories = calories_by_elf.index(max(calories_by_elf))
    max_calories = max(calories_by_elf)

    return (index_max_calories, max_calories)


# Print results depending on the question (1 or 2)
match question:
    case "1":
        # Sum calories by elf, then find the highest sum and return it
        calories_by_elf = sum_elves(input)
        answer = find_highest_calory_elf(calories_by_elf)
        print(answer[0], answer[1])

    case "2":
        # Go through the sums by elves 3 times, add the highest value to the
        # answer, and remove that value from the list

        answer = 0
        calories_by_elf = sum_elves(input)

        for i in range(0, 3):
            elf = find_highest_calory_elf(calories_by_elf)
            answer = answer + elf[1]
            calories_by_elf.pop(elf[0])

        print(answer)
