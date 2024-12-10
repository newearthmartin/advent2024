from collections import defaultdict
from functools import reduce

with open('10.txt') as f:
    lines = (line.strip() for line in f.readlines())
    lines = [list(map(int, line)) for line in lines if line]

heads = []
connections = defaultdict(list)


def test_connection(i1, j1, i2, j2):
    if 0 <= i2 < len(lines) and 0 <= j2 < len(lines[0]) and lines[i2][j2] == lines[i1][j1] + 1:
        connections[(i1, j1)].append((i2, j2))


for i, row in enumerate(lines):
    for j, val in enumerate(row):
        if val == 0:
            heads.append((i, j))
        test_connection(i, j, i - 1, j)
        test_connection(i, j, i + 1, j)
        test_connection(i, j, i, j - 1)
        test_connection(i, j, i, j + 1)


def count_heads1(i, j):
    if lines[i][j] == 9: return {(i, j)}
    reachable = (count_heads1(i2, j2) for i2, j2 in connections[(i, j)])
    return reduce(lambda x, y: x | y, reachable, set())


def count_heads2(i, j):
    if lines[i][j] == 9: return 1
    trails = (count_heads2(i2, j2) for i2, j2 in connections[(i, j)])
    return reduce(lambda x, y: x + y, trails, 0)


rv1 = 0
rv2 = 0
for i, j in heads:
    rv1 += len(count_heads1(i, j))
    rv2 += count_heads2(i, j)
print(rv1)
print(rv2)