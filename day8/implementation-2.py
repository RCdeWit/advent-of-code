with open('input.txt') as f:
    input = f.read().splitlines()

values = []

for i, line in enumerate(input):
    signal = input[i].split(' | ')[0].split(' ')
    output = input[i].split(' | ')[1].split(' ')

    signal_sorted = []
    for i in signal:
        sort = set(sorted(i))
        signal_sorted.append(sort)

    output_sorted = []
    for i in output:
        sort = set(sorted(i))
        output_sorted.append(sort)

    values.append([signal_sorted, output_sorted])

count_numbers = [0] * 10

# Based on a line of inputs and outputs, deduce the translation of signals to numbers
def find_definitions(input):
    dictionary_numbers = [-1] * 10

    # First pass to find numbers 1478
    for i, val in enumerate(input):
        for j, number in enumerate(val):
            if len(number) == 0:
                None
            elif len(number) == 1:
                None
            elif len(number) == 2:
                dictionary_numbers[1] = number
            elif len(number) == 3:
                dictionary_numbers[7] = number
            elif len(number) == 4:
                dictionary_numbers[4] = number
            elif len(number) == 5:
                None
            elif len(number) == 6:
                None
            elif len(number) == 7:
                dictionary_numbers[8] = number

    # Find 9
    # 4 is a subset of only 9
    for i, val in enumerate(input):
        for j, number in enumerate(val):
            if number not in dictionary_numbers:
                if dictionary_numbers[4].issubset(number):
                    dictionary_numbers[9] = number

    # Find 3
    # 3 is a subset of only 9 and a superset of 1
    for i, val in enumerate(input):
        for j, number in enumerate(val):
            if number not in dictionary_numbers:
                if number.issubset(dictionary_numbers[9]) and dictionary_numbers[1].issubset(number):
                    dictionary_numbers[3] = number

    # Find 6
    # 6 has 6 segments and is not a superset of 1
    for i, val in enumerate(input):
        for j, number in enumerate(val):
            if number not in dictionary_numbers:
                if len(number) == 6 and not dictionary_numbers[1].issubset(number):
                    dictionary_numbers[6] = number

    # Find 0
    # 0 is the only remaining number with 6 segments
    for i, val in enumerate(input):
        for j, number in enumerate(val):
            if number not in dictionary_numbers:
                if len(number) == 6:
                    dictionary_numbers[0] = number

    # Find 5
    # 5 is a subset of 6
    for i, val in enumerate(input):
        for j, number in enumerate(val):
            if number not in dictionary_numbers:
                if number.issubset(dictionary_numbers[6]):
                    dictionary_numbers[5] = number

    # Find 2
    # 2 is the remaining number
    for i, val in enumerate(input):
        for j, number in enumerate(val):
            if number not in dictionary_numbers:
                dictionary_numbers[2] = number

    return(dictionary_numbers)

# Now do the actual decoding per line
results_decoding = []
for i, val in enumerate(values):
    dictionary = find_definitions(val)
    result_line = ""
    for j, number in enumerate(val[1]):
        # decoded = number.index(dictionary)
        # result_line.append(decoded)

        for n, dic in enumerate(dictionary):
            if dic == number:
                result_line += str(n)

    results_decoding.append(int(result_line))

print(sum(results_decoding))
