with open("input.txt") as f:
    list_of_crabs = list(map(int, f.read().split(",")))


def get_summed_distances_from_line(list, line):
    total_distance = 0

    for val in list:
        if val > line:
            total_distance += val - line
        elif val < line:
            total_distance += line - val

    return total_distance


best_solution = max(list_of_crabs) * max(list_of_crabs)
best_line = -1

for i in range(max(list_of_crabs)):
    sum_for_solution = get_summed_distances_from_line(list_of_crabs, i)

    if sum_for_solution < best_solution:
        best_solution = sum_for_solution
        best_line = i

print(best_line, best_solution)
