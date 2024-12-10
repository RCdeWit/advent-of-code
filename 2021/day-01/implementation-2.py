with open("input.txt") as f:
    depth_readings = list(map(int, f.read().splitlines()))


def count_increases_over_previous_list_item(input, verbose=False):
    count_increased = 0

    for i, dr in enumerate(input):

        delta = input[i] - input[i - 1]
        is_deeper = delta > 0

        if verbose:
            print(
                f"Measure: {i}, Measurement: {dr}, Delta: {delta}, Increased: {is_deeper}"
            )

        if is_deeper:
            count_increased += 1

    return count_increased


def aggregate_list_by_sliding_window(input, window_size, drop_last_item=True):
    windowed_readings = [0] * len(input)

    for i, dr in enumerate(depth_readings):
        for n in range(0, window_size):
            try:
                windowed_readings[i - n] += dr
            except:
                if drop_last_item:
                    # Drop last list item because it cannot be fully aggregated
                    windowed_readings.pop()

    return windowed_readings


aggregated_list = aggregate_list_by_sliding_window(depth_readings, 3, False)
count_increased = count_increases_over_previous_list_item(aggregated_list, False)

print(count_increased)
