def calculate_rate(method, input):
    output = [0] * len(input[0])

    for row, val in enumerate(input):
        for col, bit in enumerate(val):
            if bit == "1":
                output[col] += 1
            else:
                output[col] -= 1

    if method == "epsilon":
        for col, val in enumerate(output):
            output[col] = val * -1

    for col, val in enumerate(output):
        if val < 0:
            output[col] = 0
        if val > 0:
            output[col] = 1

    # Convert to string again
    output_string = ""
    for col in output:
        output_string += str(col)

    return output_string


with open("input.txt") as f:
    diagnostics = list(f.read().splitlines())

# Convert binary to decimal
epsilon = int(calculate_rate("epsilon", diagnostics), 2)
gamma = int(calculate_rate("gamma", diagnostics), 2)

print(epsilon, gamma, epsilon * gamma)
