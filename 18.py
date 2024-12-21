from collections import defaultdict

CUTOFF1 = 1024
LENX, LENY = 71, 71

with open('input/18.txt') as f:
    lines = (line.strip() for line in f.readlines())
    lines = (line.split(',') for line in lines)
    lines = [tuple(map(int, line)) for line in lines]


def part1(cutoff):
    lines1 = set(lines[:cutoff])
    start = (0, 0)
    end = (LENX - 1, LENY - 1)
    edges = defaultdict(list)
    for x in range(LENX):
        for y in range(LENY):
            def add_edge(x1, y1):
                if 0 <= x1 < LENX and 0 <= y1 < LENY and (x, y) not in lines1 and (x1, y1) not in lines1:
                    edges[(x, y)].append(((x, y), (x1, y1)))
            add_edge(x + 1, y)
            add_edge(x - 1, y)
            add_edge(x, y + 1)
            add_edge(x, y - 1)

    min_dist = {start: 0}
    head = edges[start]
    while end not in min_dist:
        if not head:
            return None
        min_d = None
        for s, e in head:
            if min_d is None or min_dist[s] < min_d:
                min_d = min_dist[s]
                min_e = e
        min_dist[min_e] = min_d + 1
        head = [e for e in head if e[1] not in min_dist]
        head += (e for e in edges[min_e] if e[1] not in min_dist)
    return min_dist[end]


def part2():
    for i in range(CUTOFF1, len(lines)):
        res = part1(i)
        print(i)
        if not res:
            print()
            x, y = lines[i - 1]
            return f'{x},{y}'


print(part1(CUTOFF1))
print()
print(part2())





