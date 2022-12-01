with open('input.txt') as f:
    input = f.read().splitlines()

values = []

for i, line in enumerate(input):
    signal = input[i].split(' | ')[0].split(' ')
    output = input[i].split(' | ')[1].split(' ')

    values.append([signal, output])

count_numbers = [0] * 10

for i, output in enumerate(values):
    for j, number in enumerate(output[1]):
        if len(number) == 0:
            None
        elif len(number) == 1:
            None
        elif len(number) == 2:
            count_numbers[2] += 1
        elif len(number) == 3:
            count_numbers[7] += 1
        elif len(number) == 4:
            count_numbers[4] += 1
        elif len(number) == 5:
            None
        elif len(number) == 6:
            None
        elif len(number) == 7:
            count_numbers[8] += 1


        # print(number)

print(sum(count_numbers))
