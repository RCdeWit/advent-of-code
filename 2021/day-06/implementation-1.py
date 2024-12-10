with open("input.txt") as f:
    list_of_fish = list(map(int, f.read().split(",")))

# Remove trailing newline
# list_of_fish = list_of_fish[:-1]

n_days = 80
for i in range(n_days):
    temp_list_of_fish = []
    for f, val in enumerate(list_of_fish):
        if val > 0:
            temp_list_of_fish.append(val - 1)
        else:
            temp_list_of_fish.append(6)
            temp_list_of_fish.append(8)

    list_of_fish = temp_list_of_fish
    # print(f"Day {i}, {len(list_of_fish)} fish: {list_of_fish}")

print(len(list_of_fish))
