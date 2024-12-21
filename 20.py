with open('input/20.txt') as f:
    lines = [line.strip() for line in f.readlines()]
rows = len(lines)

for i, line in enumerate(lines):
    for j, c in enumerate(line):
        if c == 'S': si, sj = i, j
        if c == 'E': ei, ej = i, j

print('creating path')
visited = set()
path = []
i, j = si, sj
while (i, j) != (ei, ej):
    visited.add((i, j))
    path.append((i, j))

    def try_next(i2, j2):
        global i, j
        p2 = i2, j2
        if p2 not in visited and lines[i2][j2] != '#':
            i, j = p2
            return True
        return False
    try_next(i + 1, j) or try_next(i - 1, j) or try_next(i, j + 1) or try_next(i, j - 1)
path.append((ei, ej))
positions = {p: n for n, p in enumerate(path)}


def get_cheats(max_cheat):
    print(f'getting cheats - max cheat {max_cheat}')
    cheats = 0
    for i, p1 in enumerate(path):
        for j in range(i + max_cheat, len(path)):
            p2 = path[j]
            distance = abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])
            saved = j - i - distance
            if distance <= max_cheat and saved >= 100:
                cheats += 1
    return cheats


print(get_cheats(2))
print(get_cheats(20))
