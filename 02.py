with open('02.txt') as f:
    reports = (line.strip().split(' ') for line in f.readlines())
    reports = [[int(n) for n in line] for line in reports]


def is_safe1(levels):
    if len(levels) == 1: return True
    if levels[0] == levels[1]: return False
    asc = levels[0] < levels[1]
    diff1 = 1 if asc else -3
    diff2 = 3 if asc else -1
    for i in range(len(levels) - 1):
        diff = levels[i + 1] - levels[i]
        if diff < diff1 or diff > diff2: return False
    return True


def is_safe2(levels):
    if is_safe1(levels): return True
    for i in range(len(levels)):
        levels2 = levels[:i] + levels[i+1:]
        if is_safe1(levels2): return True
    return False


print(sum(1 for report in reports if is_safe1(report)))
print(sum(1 for report in reports if is_safe2(report)))
