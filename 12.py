from collections import defaultdict
from itertools import groupby

with open('12.txt') as f:
    lines = (line.strip() for line in f.readlines())
    lines = [line for line in lines if line]


def get_regions():
    regions = {}
    region_num = 0
    regions_by_pos = [None] * len(lines)

    def try_same_region(i, j, i0, j0):
        if not(0 <= i0 <= len(lines) and 0 <= j0 <= len(lines[0])): return False
        if lines[i][j] != lines[i0][j0]: return False
        region = regions_by_pos[i][j]
        region0 = regions_by_pos[i0][j0]
        if region is None:
            regions_by_pos[i][j] = region0
            regions[region0].append((i, j))
        elif region != region0:
            min_reg = min(region, region0)
            max_reg = max(region, region0)
            for i2, j2 in regions[max_reg]:
                regions[min_reg].append((i2, j2))
                regions_by_pos[i2][j2] = min_reg
            del regions[max_reg]
        return True

    for i, line in enumerate(lines):
        regions_by_pos[i] = [None] * len(line)
        for j, v in enumerate(line):
            found1 = try_same_region(i, j, i - 1, j)
            found2 = try_same_region(i, j, i, j - 1)
            if not found1 and not found2:
                region_num += 1
                regions_by_pos[i][j] = region_num
                regions[region_num] = [(i, j)]
    return regions


def get_sides(regions):
    sides = defaultdict(set)
    for region, cells in regions.items():
        def try_side(i, j, i2, j2):
            if (i2, j2) not in cells:
                sides[region].add(((i, j), (i2 - i, j2 - j)))
        for i, j in cells:
            try_side(i, j, i + 1, j)
            try_side(i, j, i - 1, j)
            try_side(i, j, i, j + 1)
            try_side(i, j, i, j - 1)
    return sides


regions = get_regions()
region_sides = get_sides(regions)
rv1 = sum((len(cells) * len(region_sides[region]) for region, cells in regions.items()))
print(rv1)

rv2 = 0
for region, cells in regions.items():
    key_func = lambda e: e[1]
    area = len(cells)
    directions = groupby(sorted(region_sides[region], key=key_func), key=key_func)
    directions = {d: [pos for pos, d in sides] for d, sides in directions}
    side_count = 0
    for direction, sides in directions.items():
        if direction[1] == 0:
            sides.sort()
        else:
            sides.sort(key=lambda e: (e[1], e[0]))

        for i, side in enumerate(sides):
            si, sj = side
            prev = (si - 1, sj) if direction[0] == 0 else (si, sj - 1)
            if i == 0 or sides[i-1] != prev:
                side_count += 1
    rv2 += area * side_count
print(rv2)
