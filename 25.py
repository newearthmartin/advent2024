def parse_lines():
    with open('input/25.txt') as f:
        lines = [l.strip() for l in f.readlines()]

    rv_keys = []
    rv_locks = []
    current = []

    def add_current():
        nonlocal current
        if current:
            (rv_keys if is_key else rv_locks).append(current)
            current = []
    for line in lines:
        if line:
            if len(current) == 0:
                is_key = line[0] == '.'
            current.append(line)
        else:
            add_current()
    add_current()
    return rv_locks, rv_keys


locks, keys = parse_lines()
rows = len(keys[0])
cols = len(keys[0][0])


def parse_lock(l): return [next(i for i in range(rows) if l[i][j] == '.') - 1 for j in range(cols)]
def parse_key(k): return [rows - next(i for i in range(rows) if k[i][j] == '#') - 1 for j in range(cols)]


locks = [parse_lock(l) for l in locks]
keys = [parse_key(k) for k in keys]


def overlaps(lock, key):
    for l, k in zip(lock, key):
        if k + l > rows - 2:
            return True
    return False


print(sum(1 for k in keys for l in locks if not overlaps(l, k)))