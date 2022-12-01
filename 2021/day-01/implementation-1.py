with open('input.txt') as f:
    depth_readings = list(map(int, f.read().splitlines()))

count_increased = 0

for i, dr in enumerate(depth_readings):

    delta = depth_readings[i] - depth_readings[i-1]
    is_deeper = delta > 0

    print(f"Measure: {i}, Measurement: {dr}, Delta: {delta}, Increased: {is_deeper}")

    if is_deeper:
        count_increased += 1

print(count_increased)
