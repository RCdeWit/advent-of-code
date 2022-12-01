with open('input.txt') as f:
    input = f.read()

# Parse input
x = input.split(', ')[0]
y = input.split(', ')[1]

x_min = int(x.split('..')[0][2:])
x_max = int(x.split('..')[1])

y_min = int(y.split('..')[0][2:])
y_max = int(y.split('..')[1])

target = [[x_min, x_max], [y_min, y_max]]

def cycle_step_probe(probe):
    x_new = probe["position"][0] + probe["velocity"][0]
    y_new = probe["position"][1] + probe["velocity"][1]

    probe["position"] = [x_new, y_new]

    vel_y_new = probe["velocity"][1] - 1

    if probe["velocity"][0] > 0:
        vel_x_new = probe["velocity"][0] - 1
    elif probe["velocity"][0] < 0:
        vel_x_new = probe["velocity"][0] + 1
    else:
        vel_x_new = 0

    probe["velocity"] = [vel_x_new, vel_y_new]

    return probe

def check_hit_probe(probe):
    target_x_min = min(probe["target"][0])
    target_x_max = max(probe["target"][0])
    target_y_min = min(probe["target"][1])
    target_y_max = max(probe["target"][1])

    position_x = probe["position"][0]
    position_y = probe["position"][1]

    if target_x_max >= position_x >= target_x_min and target_y_max >= position_y >= target_y_min:
        return "HIT"
    elif position_x > target_x_max or (probe["velocity"][0] == 0 and position_y < target_y_min):
        return "OVERSHOT"
    else:
        return "NOHIT"

def calculate_trajectory(probe, max_cycles):
    high_point = 0
    i = 0
    while i < max_cycles:
        probe = cycle_step_probe(probe)

        result_cycle = check_hit_probe(probe)
        high_point = max(probe["position"][1], high_point)

        if result_cycle == "HIT":
            return {"result": "hit", "position": probe["position"], "cycles": i+1, "high_point": high_point}
        elif result_cycle == "OVERSHOT":
            return {"result": "overshot", "position": probe["position"], "cycles": i+1, "high_point": high_point}

        i += 1

    return  {"result": "max cycles reached", "position": probe["position"], "cycles": i+1, "high_point": high_point}

def find_hitting_trajectory_with_highest_point(max_cycles, max_velocity_x, max_velocity_y):
    highest_trajectory = {"high_point": -1}

    for x in range(min_velocity_x, max_velocity_x):
        for y in range(min_velocity_y, max_velocity_y):
            # Create a probe
            probe = {}
            probe["position"] = [0, 0]
            probe["target"] = target
            probe["velocity"] = [x, y]

            trajectory = calculate_trajectory(probe, max_cycles)

            if trajectory["result"] == "hit":
                if highest_trajectory["high_point"] < trajectory["high_point"]:
                    highest_trajectory = trajectory

    return highest_trajectory

def find_all_hitting_velocities(max_cycles, max_velocity_x, max_velocity_y):
    output = []

    for x in range(min_velocity_x, max_velocity_x):
        for y in range(min_velocity_y, max_velocity_y):
            # Create a probe
            probe = {}
            probe["position"] = [0, 0]
            probe["target"] = target
            probe["velocity"] = [x, y]

            trajectory = calculate_trajectory(probe, max_cycles)

            if trajectory["result"] == "hit":
                output.append(trajectory)

    return output


max_cycles = 1000
min_velocity_x = 0
max_velocity_x = 200
min_velocity_y = -200
max_velocity_y = 200

result = find_all_hitting_velocities(max_cycles, max_velocity_x, max_velocity_y)
print(len(result))
