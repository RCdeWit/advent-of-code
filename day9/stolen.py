import numpy

lines = [line.strip() for line in open('input.txt')]
rows = len(lines)
cols = len(lines[0])


def orthogonal(x, y): return [xy for xy in [
    (x-1, y), (x+1, y), (x, y-1), (x, y+1)] if 0 <= xy[1] < rows and 0 <= xy[0] < cols]


def yield_low_point():
    for row in range(rows):
        for col in range(cols):
            adjacent = [lines[r][c] for c, r in orthogonal(col, row)]
            if min(adjacent) > lines[row][col]:
                yield col, row

                print(col, row)


def find_basin(x, y, basin=None):
    if basin is None:
        basin = set()
    if lines[y][x] != '9' and (x, y) not in basin:
        basin.add((x, y))
        for xy in orthogonal(x, y):
            find_basin(xy[0], xy[1], basin)
    return len(basin)


print('Part 1:', sum(int(lines[y][x])+1 for x, y in yield_low_point()))
#
# print('Part 2:', numpy.prod(sorted(find_basin(x, y)
#                                 for x, y in yield_low_point())[-3:]))
