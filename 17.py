import re

with open('17.txt') as f:
    lines = [line.strip() for line in f.readlines()]

reg_a, reg_b, reg_c = None, None, None
for line in lines:
    if m := re.match(r'^Register (.): ', line):
        s1, s2 = m.span()
        val = int(line[s1 + s2:])
        if m[1] == 'A': reg_a = val
        if m[1] == 'B': reg_b = val
        if m[1] == 'C': reg_c = val
    elif m := re.match(r'^Program: (.*)$', line):
        program = [int(n) for n in m[1].split(',')]


def execute(a, b, c):
    output = []
    i = 0
    while i < len(program):
        opcode = program[i]
        operand = program[i + 1]
        operand_combo = operand if operand <= 3 else \
            a if operand == 4 else \
            b if operand == 5 else \
            c if operand == 6 else None
        next_i = i + 2

        if opcode == 0:
            a = a // (2 ** operand_combo)
        elif opcode == 1:
            b = b ^ operand
        elif opcode == 2:
            b = operand_combo % 8
        elif opcode == 3:
            if a != 0:
                next_i = operand
        elif opcode == 4:
            b = b ^ c
        elif opcode == 5:
            res = operand_combo % 8
            output.append(res)
        elif opcode == 6:
            b = a // (2 ** operand_combo)
        elif opcode == 7:
            c = a // (2 ** operand_combo)
        i = next_i
    return output


def part1():
    out = execute(reg_a, reg_b, reg_c)
    return ','.join(map(str, out))


def part2():
    matches = [0]
    for d in range(len(program) - 1, -1, -1):
        desired = program[d]
        print(f'digit {d} looking for {desired} in {matches}')
        new_matches = []
        for match in matches:
            for i in range(8):
                a = match * 8 + i
                output = execute(a, 0, 0)
                if output[0] == desired:
                    new_matches.append(a)
        matches = new_matches
    print()
    return min(matches)


print(part1())
print()
print(part2())
