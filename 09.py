from functools import reduce

with open('input/09.txt') as f:
    data = f.read().strip()
data = [int(c) for c in data]


def build_files():
    files = []
    is_file = True
    filenum = 0
    for n in data:
        if n > 0:
            files.append((n, filenum if is_file else None))
        if is_file: filenum += 1
        is_file = not is_file
    return files


def to_disk1(files):
    sizes = (size for size, _ in files)
    total_space = reduce(lambda x, y: x + y, sizes)
    disk = [None] * total_space
    pointer = 0
    for size, num in files:
        for _ in range(size):
            disk[pointer] = num
            pointer += 1
    return disk


def move1(files):
    disk = to_disk1(files)
    l = 0
    r = len(disk) - 1
    while l < r:
        if disk[l] is not None:
            l += 1
            continue
        if disk[r] is None:
            r -= 1
            continue
        disk[l], disk[r] = disk[r], disk[l]
    return disk


def move2(files):
    pointer = 0
    fs = []
    ss = []
    for size, num in files:
        if num is not None:
            fs.append([pointer, size, num])
        else:
            ss.append([pointer, size])
        pointer += size

    for i, (pointer1, size1, num) in reversed(list(enumerate(fs))):
        for j, (pointer2, size2) in enumerate(ss):
            if pointer2 >= pointer1:
                continue
            if size2 >= size1:
                fs[i][0] = pointer2
                ss[j][0] += size1
                ss[j][1] -= size1
                assert ss[j][1] >= 0
                if ss[j][1] == 0: del ss[j]
                break
    fs = sorted(fs)
    disk = [None] * (fs[-1][0] + fs[-1][1])
    for pointer, size, num in fs:
        for i in range(size):
            disk[pointer + i] = num
    return disk


def checksum(disk):
    rv = 0
    for i, n in enumerate(disk):
        if n is None: continue
        rv += i * n
    return rv


files1 = build_files()
disk1 = move1(files1)
print(checksum(disk1))

disk2 = move2(files1)
print(checksum(disk2))