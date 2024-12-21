with open('input/15.txt') as f:
    lines = [line.strip() for line in f.readlines()]
    divider = lines.index('')
    instructions = ''.join(lines[divider+1:])
    lines = [list(line) for line in lines[:divider]]

rows = len(lines)
cols = len(lines[0])


def get_robot_pos():
    for i, line in enumerate(lines):
        try:
            rj = line.index('@')
            return i, rj
        except ValueError:
            pass


def draw():
    for i, line in enumerate(lines):
        print(''.join(line))
    print('-' * cols)
    print('-' * cols)


def get_boxes1(i, j, di, dj):
    boxes = set()
    while True:
        i += di
        j += dj
        if lines[i][j] == '#': return None
        if lines[i][j] == '.': return boxes
        if lines[i][j] == 'O':
            boxes.add((i, j))
        if lines[i][j] == '[':
            boxes.add((i, j))
            boxes.add((i, j + 1))
        if lines[i][j] == ']':
            boxes.add((i, j))
            boxes.add((i, j - 1))


def get_boxes2(i, j, di, dj):
    if di == 0: return get_boxes1(i, j, di, dj)
    boxes = set()

    def add_start(pi, pj, start_list):
        start_list.append((pi, pj))
        if lines[pi][pj] == '[': start_list.append((pi, pj + 1))
        if lines[pi][pj] == ']': start_list.append((pi, pj - 1))

    start = []
    add_start(i + di, j + dj, start)

    while start:
        new_start = []
        for pi, pj in start:
            if lines[pi][pj] == '#': return None
            elif lines[pi][pj] == '.': continue
            elif lines[pi][pj] in ['[', ']']:
                boxes.add((pi, pj))
                add_start(pi + di, pj + dj, new_start)
            else:
                raise Exception('Unexpected ' + lines[pi][pj])
        start = new_start
    return boxes


def move_boxes(boxes, di, dj):
    shapes = {}
    for i, j in boxes:
        shapes[(i, j)] = lines[i][j]
        lines[i][j] = '.'
    for i, j in boxes:
        lines[i + di][j + dj] = shapes[(i, j)]


def move_robot(get_boxes_fn):
    ri, rj = get_robot_pos()
    for instruction in instructions:
        if instruction == '<': di, dj = 0, -1
        if instruction == '>': di, dj = 0, 1
        if instruction == 'v': di, dj = 1, 0
        if instruction == '^': di, dj = -1, 0

        pi, pj = ri + di, rj + dj
        if lines[pi][pj] == '#': continue
        if lines[pi][pj] == '.':
            lines[ri][rj] = '.'
            ri, rj = pi, pj
            lines[ri][rj] = '@'
            continue
        boxes = get_boxes_fn(ri, rj, di, dj)
        if boxes is None: continue
        move_boxes(boxes, di, dj)
        lines[ri][rj] = '.'
        ri, rj = pi, pj
        lines[ri][rj] = '@'
    return sum(100 * i + j for i, line in enumerate(lines) for j, c in enumerate(line) if c in ['O', '['])


print(move_robot(get_boxes1))
for i, line in enumerate(lines):
    new_line = []
    for c in line:
        if c == '#': new_line += ['#', '#']
        if c == 'O': new_line += ['[', ']']
        if c == '@': new_line += ['@', '.']
        if c == '.': new_line += ['.', '.']
    lines[i] = new_line
print(move_robot(get_boxes2))
