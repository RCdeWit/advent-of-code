with open("input.txt") as f:
    list_of_fish = list(map(int, f.read().split(",")))

n_days = 256

# Aggregate fish by day rather than simulate them all individually
summed_list_of_fish = [0] * 9
for f, val in enumerate(list_of_fish):
    summed_list_of_fish[val] += 1

# Every day find the number of fish who are fish_reproducing
# Reset those fish to a week
# Add the new fish to the end of the array
# And remove today from the array
for i in range(n_days):
    fish_reproducing = summed_list_of_fish[0]

    summed_list_of_fish[7] += fish_reproducing
    summed_list_of_fish.append(fish_reproducing)
    summed_list_of_fish = summed_list_of_fish[1:]

print(sum(summed_list_of_fish))
