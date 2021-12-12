with open('input.txt') as f:
    input = f.read().splitlines()

arches = []

for line in input:
    pos1 = line.split('-')[0]
    pos2 = line.split('-')[1]

    arches.append([pos1, pos2])

graph = {}

for arch in arches:
    start = arch[0]
    end = arch[1]

    if start in graph:
        graph[start].append(end)
    else:
        graph[start] = [end]

    if end in graph:
        graph[end].append(start)
    else:
        graph[end] = [start]


revisit_small_available = True

# Horrendous approach, but we
def double_small_cave_exists(path):
    count = 0
    for node in set(path):
        if path.count(node) > 1 and node.islower():
            return True

# Adapted from https://www.python.org/doc/essays/graphs/
# With sincere gratitude
def find_all_paths(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if not start in graph:
            return []
        paths = []
        for node in graph[start]:
            if node not in path or node.isupper() or (not double_small_cave_exists(path) and node != "start"):
                newpaths = find_all_paths(graph, node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)

        return paths

print(len(find_all_paths(graph, "start", "end")))
