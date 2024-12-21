from itertools import product
from functools import cache


with open('input/21.txt') as f:
    lines = [line.strip() for line in f.readlines()]


def get_min_elems(lst):
    min_len = min(len(e) for e in lst)
    return (e for e in lst if len(e) == min_len)


KEYPAD1 = {
    '7': (0, 0),
    '8': (0, 1),
    '9': (0, 2),
    '4': (1, 0),
    '5': (1, 1),
    '6': (1, 2),
    '1': (2, 0),
    '2': (2, 1),
    '3': (2, 2),
    ' ': (3, 0),
    '0': (3, 1),
    'A': (3, 2),
}

KEYPAD2 = {
    ' ': (0, 0),
    '^': (0, 1),
    'A': (0, 2),
    '<': (1, 0),
    'v': (1, 1),
    '>': (1, 2),
}

KEYS1 = sorted([k for k in KEYPAD1.keys() if k != ' '])
KEYS2 = sorted([k for k in KEYPAD2.keys() if k != ' '])


@cache
def get_token(k1, k2): return k1, k2
def as_tokens(line): return tuple(as_tokens_gen(line))


def as_tokens_gen(line):
    prev = 'A'
    for c in line:
        yield get_token(prev, c)
        prev = c


def get_presses_generator(keypad, i1, j1, i2, j2):
    di, dj = i2 - i1, j2 - j1
    ai, aj = abs(di), abs(dj)
    diri = 0 if di == 0 else 1 if di > 0 else -1
    dirj = 0 if dj == 0 else 1 if dj > 0 else -1

    ci = 'v' if di > 0 else '^'
    cj = '>' if dj > 0 else '<'

    if ai == 0 and aj == 0: yield 'A'
    elif ai == 0: yield cj * aj + 'A'
    elif aj == 0: yield ci * ai + 'A'
    else:
        if keypad[' '] != (i1 + diri, j1):
            for p2 in get_presses_generator(keypad, i1 + diri, j1, i2, j2):
                yield ci + p2
        if keypad[' '] != (i1, j1 + dirj):
            for p2 in get_presses_generator(keypad, i1, j1 + dirj, i2, j2):
                yield cj + p2


@cache
def get_presses(key1, key2, is_keypad2):
    keypad = KEYPAD2 if is_keypad2 else KEYPAD1
    i1, j1 = keypad[key1]
    i2, j2 = keypad[key2]
    presses = list(get_presses_generator(keypad, i1, j1, i2, j2))
    min_len = min(len(p) for p in presses)
    presses = [as_tokens(p) for p in presses if len(p) == min_len]
    return presses


def get_sequence_presses(tokens, is_keypad2):
    seqs = [get_presses(k1, k2, is_keypad2) for k1, k2 in tokens]
    return [[e for sublist in combination for e in sublist] for combination in product(*seqs)]


@cache
def min_len_token(token, times):
    if times == 0: return 1
    presses = get_presses(token[0], token[1], True)
    return min(sum(min_len_token(t, times - 1) for t in press) for press in presses)


def process_line(line, depth):
    seqs0 = get_sequence_presses(as_tokens(line), False)
    min_len = min(sum(min_len_token(t, depth) for t in s) for s in seqs0)
    num = int(line.replace('A', ''))
    return num * min_len


print(sum(process_line(line, 2) for line in lines))
print(sum(process_line(line, 25) for line in lines))
