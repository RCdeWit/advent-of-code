from collections import Counter

with open('input.txt') as f:
    input = f.read().splitlines()

rules = []
for line in input[2:]:
    pair = line.split(' -> ')[0]
    insert = line.split(' -> ')[1]

    rules.append([pair, insert])

def template_string_to_dict(string, multiplication=1):
    template = {}
    for c, char in enumerate(string[0:-1]):
        key = char + string[c+1]

        if key not in template:
            template[key] = multiplication
        else:
            template[key] += multiplication

    return template

# Process all rules for one key
def process_rules(key, rules, multiplication=1):
    for r in rules:
        if r[0] == key:
            return template_string_to_dict(key[0] + r[1] + key[1], multiplication)

    return template_string_to_dict(key)

def count_letter_occurences(dict):
    letters = {}

    for key in dict:
        start_letter = key[0]
        if start_letter not in letters:
            letters[start_letter] = dict[key]
        else:
            letters[start_letter] += dict[key]

    # Because we always look at the first letter of each pair,
    # only the very last letter in the input string is excluded.
    # Hacked it back in here.
    letters[input[0][-1]] += 1

    return sorted(letters.items(), key=lambda item: item[1])

def cycle_rules(template, rules):
    output = Counter({})
    for key in template:
        key_result = process_rules(str(key), rules, template[key])
        output += Counter(key_result) # Merge two dictionaries

    return dict(output)


template = template_string_to_dict(input[0])
result = template
n_cycles = 40
for c in range(n_cycles):
    result = cycle_rules(result, rules)

# print(result)
print(count_letter_occurences(result))
