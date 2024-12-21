from collections import Counter
from functools import reduce

with open('input/01.txt') as f:
    lines = f.readlines()

lines = (line.strip().split('   ') for line in lines)
lines = ((int(n) for n in line) for line in lines)

lines1, lines2 = zip(*lines)
lines1 = sorted(lines1)
lines2 = sorted(lines2)

distance = 0
for l1, l2 in zip(lines1, lines2):
    distance += abs(l1 - l2)
print(distance)

count = Counter(lines2)
vals = (l1 * count[l1] for l1 in lines1)
similarity = reduce(lambda x, y: x + y, vals)
print(similarity)