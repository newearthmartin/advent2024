with open('input/06.txt') as f:
    lines = [line.strip() for line in f.readlines()]

obstacles = set()
for i, line in enumerate(lines):
    for j, c in enumerate(line):
        if c == '#': obstacles.add((i, j))
        if c == '^': guard_pos = (i, j)


NEXT_DIR = {
    (-1, 0): (0, 1),
    (0, 1): (1, 0),
    (1, 0): (0, -1),
    (0, -1): (-1, 0)
}


def get_visited():
    i, j = guard_pos
    visited = set()
    visited2 = set()
    direction = (-1, 0)
    is_loop = False

    while 0 <= i < len(lines) and 0 <= j < len(lines[0]):
        if (visited2_key := (i, j, direction)) in visited2:
            is_loop = True
            break
        visited.add((i, j))
        visited2.add(visited2_key)

        nexti, nextj = i + direction[0], j + direction[1]
        if (nexti, nextj) in obstacles:
            direction = NEXT_DIR[direction]
        else:
            i, j = nexti, nextj
    return visited, is_loop


visited, loop = get_visited()
assert loop is False
print(len(visited))


new_obstacles = set()
visited.remove(guard_pos)
for i, j in visited:
    assert (i, j) not in obstacles
    obstacles.add((i, j))
    if get_visited()[1]:
        new_obstacles.add((i, j))
    obstacles.remove((i, j))
print(len(new_obstacles))
