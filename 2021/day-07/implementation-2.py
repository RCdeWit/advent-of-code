with open("input.txt") as f:
    list_of_crabs = list(map(int, f.read().split(",")))


def get_summed_fuel_from_line(list, line):
    total_fuel = 0

    for val in list:
        distance = abs(line - val)

        # Gaussian summation
        total_fuel += distance * (distance + 1) / 2

    return total_distance


best_solution = max(list_of_crabs) ** 3
best_line = -1

for i in range(max(list_of_crabs)):
    sum_for_solution = get_summed_fuel_from_line(list_of_crabs, i)

    if sum_for_solution < best_solution:
        best_solution = sum_for_solution
        best_line = i

print(best_line, best_solution)
