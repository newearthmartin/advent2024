with open('input/05.txt') as f:
    lines = [line.strip() for line in f.readlines()]

rules = set()
manuals = []

for line in lines:
    if '|' in line: rules.add(tuple(int(n) for n in line.split('|')))
    if ',' in line: manuals.append([int(n) for n in line.split(',')])


def is_correct(manual):
    for i, v1 in enumerate(manual):
        for v2 in manual[i+1:]:
            if (v2, v1) in rules:
                return False
    return True


def middle_val(manual):
    return manual[len(manual) // 2]


def reorder(manual):
    manual2 = []
    for v1 in manual:
        found = False
        for i, v2 in enumerate(manual2):
            if (v1, v2) in rules:
                manual2.insert(i, v1)
                found = True
                break
        if not found:
            manual2.append(v1)
    return manual2


rv1 = 0
rv2 = 0
for m in manuals:
    if is_correct(m):
        rv1 += middle_val(m)
    else:
        rv2 += middle_val(reorder(m))

print(rv1)
print(rv2)
