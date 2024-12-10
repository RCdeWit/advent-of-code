with open("input.txt") as f:
    input = f.read().splitlines()

template = input[0]

rules = []
for line in input[2:]:
    pair = line.split(" -> ")[0]
    insert = line.split(" -> ")[1]

    rules.append([pair, insert])


def process_rules(template, rules):
    output = ""
    for i, letter in enumerate(template[:-1]):
        next_letter = template[i + 1]

        output += letter
        for r in rules:
            if r[0] == letter + next_letter:
                output += r[1]

    output += template[-1]
    return output


n_cycles = 10
result = template
for c in range(n_cycles):
    result = process_rules(result, rules)


def count_letter_occurences(string):
    distinct_letters = list(set(string))
    output = dict.fromkeys(distinct_letters, 0)

    for l in string:
        output[l] += 1

    return output


print(count_letter_occurences(result))
