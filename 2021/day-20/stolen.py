from collections import defaultdict
import sys

with open("input.txt", 'r') as file:
    data = [x for x in file.read().splitlines() if x]
    op = '.'
    grid = defaultdict(lambda : op, {(x,y) : data[1:][y][x] for x in range(len(data[1:][0])) for y in range(len(data[1:]))})
    binary = {'.' : lambda : '0', '#' : lambda : '1'}
    new = lambda x,y : data[0][int(''.join([binary[grid[(x + a, y + b)]]() for b in [-1, 0, 1] for a in [-1, 0, 1]]), 2)]
    for i in range(1, 51):
        new_grid = defaultdict(lambda : op)
        minx, maxx = min(z[0] for z in grid.keys()) - 1, max(z[0] for z in grid.keys()) + 2
        miny, maxy = min(z[1] for z in grid.keys()) - 1, max(z[1] for z in grid.keys()) + 2
        for x in range(minx, maxx):
            for y in range(miny, maxy):
                new_grid[(x,y)] = new(x,y)
        grid = new_grid
        op = data[0][int(binary[grid[sys.maxsize, sys.maxsize]]() * 9, 2)]
        grid.pop((sys.maxsize, sys.maxsize))
        if i in [2, 50]:
            print(sum(1 for x in new_grid.values() if x == '#'))
