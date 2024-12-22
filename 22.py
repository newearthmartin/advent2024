from collections import defaultdict


with open('input/22.txt') as f:
    lines = [int(line.strip()) for line in f.readlines()]


def next_number(n):
    n2 = n * 64
    n = (n ^ n2) % 16777216
    n2 = n // 32
    n = (n ^ n2) % 16777216
    n2 = n * 2048
    return (n ^ n2) % 16777216


def advance(n, times):
    rv = [n % 10]
    for _ in range(times):
        n = next_number(n)
        rv.append(n % 10)
    return n, rv


rv1 = 0
seqs = []
diffs = []
for line in lines:
    n, seq = advance(line, 2000)
    rv1 += n
    seqs.append(seq)
    diffs.append([(seq[i] - seq[i-1]) if i > 0 else None for i in range(len(seq))])
print(rv1)

quat_lines = defaultdict(set)
quat_profit = defaultdict(int)

for line, (seq, diff) in enumerate(zip(seqs, diffs)):
    for i in range(1, len(diff) - 3):
        quat = (diff[i], diff[i + 1], diff[i + 2], diff[i + 3])
        if line not in quat_lines[quat]:
            quat_lines[quat].add(line)
            quat_profit[quat] += seq[i + 3]

print(sorted(quat_profit.values(), reverse=True)[0])