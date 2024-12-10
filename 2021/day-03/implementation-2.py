def get_most_common_value_in_column(input, column):
    output = [0] * len(input[0])

    for row, val in enumerate(input):
        for col, bit in enumerate(val):
            if bit == "1":
                output[col] += 1
            else:
                output[col] -= 1

    if output[column] >= 0:
        return 1
    else:
        return 0


def reduce_list_by_common_columns(input, metric):
    output = input

    for i, val in enumerate(output[0]):
        most_common_value = get_most_common_value_in_column(output, i)
        temp_list = []
        for j, val2 in enumerate(output):

            if int(output[j][i]) == most_common_value and metric == "most":
                temp_list.append(output[j])
            elif int(output[j][i]) != most_common_value and metric == "least":
                temp_list.append(output[j])

        output = temp_list

        if len(output) == 1:
            return (output)[0]


with open("input.txt") as f:
    diagnostics = list(f.read().splitlines())

oxygen = int(reduce_list_by_common_columns(diagnostics, "most"), 2)
scrubber = int(reduce_list_by_common_columns(diagnostics, "least"), 2)

print(oxygen, scrubber, oxygen * scrubber)
