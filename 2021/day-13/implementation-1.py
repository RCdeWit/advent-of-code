import numpy

with open("input.txt") as f:
    input = f.read().splitlines()

dots = []
folds = []

max_x = 0
max_y = 0

for line in input:
    if line[0:4] == "fold":
        axis = line[11:].split("=")[0]
        value = int(line[11:].split("=")[1])
        folds.append([axis, value])
    elif line == "":
        None
    else:
        x = int(line.split(",")[0])
        y = int(line.split(",")[1])

        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y

        dots.append([x, y])

paper = numpy.zeros([max_y + 1, max_x + 1])
for dot in dots:
    paper[dot[1]][dot[0]] += 1


def fold_grid(grid, axis, value):
    output = []
    distance_from_fold = 0

    # Horizontal fold along y
    if axis == "y":
        for i, row in enumerate(grid):
            if i < value:
                output.append(row)
            elif i == value:
                None
            else:
                distance_from_fold += 1
                for j, val in enumerate(row):
                    output[value - distance_from_fold][j] += val

    # Vertical fold along x
    elif axis == "x":
        for i, row in enumerate(grid):
            output_row = []
            distance_from_fold = 0  # Reset for every new row
            for j, val in enumerate(row):
                if j < value:
                    output_row.append(val)
                elif j == value:
                    None
                else:
                    distance_from_fold += 1
                    output_row[value - distance_from_fold] += val

            output.append(output_row)

    return output


def count_dots(grid):
    count = 0
    for x in grid:
        for y in x:
            if y >= 1:
                count += 1
    return count


# print(f"Original width: {len(paper)}, Original length: {len(paper[0])}")
for fold in folds:
    paper = fold_grid(paper, fold[0], fold[1])
    # print(f"Fold: {fold}, New width: {len(paper)}, New length: {len(paper[0])}")


# Solution 1:
# print(count_dots(paper))


def print_paper(grid):
    for x in grid:
        row = ""
        for y in x:
            if y > 0:
                row += "#"
            else:
                row += " "

        print(row)


# Solution 2:
print_paper(paper)
