with open('input/04.txt') as f:
    lines = [line.strip() for line in f.readlines()]


def search1(i, j, di, dj):
    for c in 'XMAS':
        if i < 0 or i >= len(lines): return False
        if j < 0 or j >= len(lines[0]): return False
        if lines[i][j] != c: return False
        i += di
        j += dj
    return True


def search2(i, j):
    if i == 0 or i == len(lines) - 1: return False
    if j == 0 or j == len(lines[0]) - 1: return False
    line1 = {lines[i - 1][j - 1], lines[i + 1][j + 1]}
    line2 = {lines[i - 1][j + 1], lines[i + 1][j - 1]}
    return lines[i][j] == 'A' and line1 == {'M', 'S'} and line2 == {'M', 'S'}


rv1 = 0
rv2 = 0
for i, line in enumerate(lines):
    for j, c in enumerate(line):
        if c == 'X':
            if search1(i, j, 1, 0): rv1 += 1
            if search1(i, j, 1, 1): rv1 += 1
            if search1(i, j, 0, 1): rv1 += 1
            if search1(i, j, -1, 1): rv1 += 1
            if search1(i, j, -1, 0): rv1 += 1
            if search1(i, j, -1, -1): rv1 += 1
            if search1(i, j, 0, -1): rv1 += 1
            if search1(i, j, 1, -1): rv1 += 1
        if c == 'A':
            if search2(i, j): rv2 += 1

print(rv1)
print(rv2)