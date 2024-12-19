with open('19.txt') as f:
    towels = f.readline().strip().split(', ')
    f.readline()
    designs = [line.strip() for line in f.readlines()]


def is_possible1(design):
    return is_possible1_dfs(design, 0)


def is_possible1_dfs(design, i):
    if i == len(design): return True
    for towel in towels:
        if is_substr(design, towel, i):
            if is_possible1_dfs(design, i + len(towel)): return True
    return False


def is_substr(string, substring, i):
    if i + len(substring) > len(string): return False
    return all(string[i + j] == c for j, c in enumerate(substring))


def is_possible2(design):
    positions = [[] for _ in range(len(design))]
    for i in range(len(design)):
        for towel in towels:
            if is_substr(design, towel, i):
                positions[i].append(len(towel))
    cache = {}
    return is_possible2_dp(design, 0, positions, cache)


def is_possible2_dp(design, i, positions, cache):
    if i == len(design): return 1
    if i in cache: return cache[i]
    rv = 0
    for length in positions[i]:
        rv += is_possible2_dp(design, i + length, positions, cache)
    cache[i] = rv
    return rv


print(sum(1 for design in designs if is_possible1(design)))
print(sum(is_possible2(design) for design in designs))