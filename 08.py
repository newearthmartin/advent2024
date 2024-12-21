from collections import defaultdict

with open('input/08.txt') as f:
    lines = [line.strip() for line in f.readlines() if line]

nodes = defaultdict(list)
antinodes1 = set()
antinodes2 = set()

for i, line in enumerate(lines):
    for j, c in enumerate(line):
        if c != '.':
            nodes[c].append((i, j))


def add_antinode1(i, j):
    if 0 <= i < len(lines) and 0 <= j < len(lines[0]):
        antinodes1.add((i, j))


def add_antinode2(i, j, incri, incrj):
    while 0 <= i < len(lines) and 0 <= j < len(lines[0]):
        antinodes2.add((i, j))
        i += incri
        j += incrj


for node, positions in nodes.items():
    for i1, pos1 in enumerate(positions):
        for i2 in range(i1 + 1, len(positions)):
            pos2 = positions[i2]
            diffi = pos2[0] - pos1[0]
            diffj = pos2[1] - pos1[1]
            add_antinode1(pos1[0] - diffi, pos1[1] - diffj)
            add_antinode1(pos2[0] + diffi, pos2[1] + diffj)
            add_antinode2(pos1[0], pos1[1], -diffi, -diffj)
            add_antinode2(pos2[0], pos2[1], diffi, diffj)

print(len(antinodes1))
print(len(antinodes2))
