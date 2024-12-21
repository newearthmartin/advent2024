from collections import defaultdict, deque
from enum import Enum

with open('input/16.txt') as f:
    lines = [line.strip() for line in f.readlines()]


distances = defaultdict(list)


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


DIRS = {
    Direction.UP: (-1, 0),
    Direction.DOWN: (1, 0),
    Direction.LEFT: (0, -1),
    Direction.RIGHT: (0, 1),
}


ei, ej = None, None
si, sj = None, None
for i, line in enumerate(lines):
    for j, c in enumerate(line):
        pos = i, j
        if c == 'E': ei, ej = pos
        if c == 'S': si, sj = pos
        if c == '#': continue

        def add_straight(d):
            di, dj = DIRS[d]
            pos2 = i2, j2 = i + di, j + dj
            if lines[i2][j2] != '#':
                distances[(pos, d)].append(((pos, d), (pos2, d), 1))

        def add_turn(d1, d2):
            di, dj = DIRS[d2]
            if lines[i + di][j + dj] != '#':
                distances[(pos, d1)].append(((pos, d1), (pos, d2), 1000))

        add_straight(Direction.UP)
        add_straight(Direction.RIGHT)
        add_straight(Direction.DOWN)
        add_straight(Direction.LEFT)
        add_turn(Direction.UP, Direction.RIGHT)
        add_turn(Direction.UP, Direction.LEFT)
        add_turn(Direction.RIGHT, Direction.DOWN)
        add_turn(Direction.RIGHT, Direction.UP)
        add_turn(Direction.DOWN, Direction.LEFT)
        add_turn(Direction.DOWN, Direction.RIGHT)
        add_turn(Direction.LEFT, Direction.UP)
        add_turn(Direction.LEFT, Direction.DOWN)

start = ((si, sj), Direction.RIGHT)
target = ((ei, ej), Direction.RIGHT)
min_distance = {start: 0}
prev_nodes = defaultdict(set)
visited = set()
edges = distances[start]
i = 0
while True:
    if i % 1000 == 0: print(i)
    i += 1
    new_edges = []
    min_edge = None
    for e in edges:
        if e in visited: continue
        if min_edge is None or e[2] < min_edge[2]:
            min_edge = e
        new_edges.append(e)
    if min_edge is None:
        break
    n1, n2, d = min_edge
    n2_dist = min_distance[n1] + d
    if n2 not in min_distance or n2_dist <= min_distance[n2]:
        min_distance[n2] = n2_dist
        prev_nodes[n2].add(n1)
    visited.add(min_edge)
    new_edges += (e for e in distances[n2] if e not in visited)
    edges = new_edges
print()
print(min_distance[target])

best_path_nodes = {target}
head = [target]
visited = set()
while head:
    new_head = []
    for h in head:
        visited.add(h)
        best_path_nodes |= {n[0] for n in prev_nodes[h]}
        new_head += (n for n in prev_nodes[h] if n not in visited)
    head = new_head
print(len(best_path_nodes))
