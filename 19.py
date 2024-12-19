with open('19.txt') as f:
    towels = f.readline().strip().split(', ')
    f.readline()
    designs = [line.strip() for line in f.readlines()]


def is_possible(design, i):
    if i == len(design): return True
    for towel in towels:
        if is_substr(design, towel, i):
            if is_possible(design, i + len(towel)): return True
    return False


def is_substr(string, substring, i):
    if i + len(substring) > len(string): return False
    return all(string[i + j] == c for j, c in enumerate(substring))


print(sum(1 for design in designs if is_possible(design, 0)))
