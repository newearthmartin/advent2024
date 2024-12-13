from itertools import groupby
from sympy import symbols, Eq, solve


with open('13.txt') as f:
    lines = [line.strip() for line in f.readlines()]

lines = (None if not l else l.replace('Button A: ', '')
         .replace('Button B: ', '')
         .replace('Prize: ', '')
         .replace('X', '')
         .replace('Y', '')
         .replace('+', '')
         .replace('=','')
         .replace(',', '')
         for l in lines)
lines = (l.split(' ') if l else None for l in lines)
lines = (tuple(int(n) for n in l) if l else None for l in lines)
machines = [tuple(g) for k, g in groupby(lines, lambda x: x is not None) if k]


def test_machine(ax, ay, bx, by, px, py):
    limit_b = min(px // bx, py // by)
    min_cost = None
    for bi in range(limit_b + 1):
        pxb = bi * bx
        pyb = bi * by
        if pxb > px or pyb > py: break
        diffx = px - pxb
        diffy = py - pyb
        if diffx % ax == 0 and diffy % ay == 0 and (ai := diffx // ax) == diffy // ay:
            cost = bi + ai * 3
            min_cost = min(min_cost, cost) if min_cost else cost
    return min_cost if min_cost is not None else 0


def test_machine2(ax, ay, bx, by, px, py):
    ai, bi = symbols('ai bi', integer=True)
    eq1 = Eq(bx * bi + ax * ai, px)
    eq2 = Eq(by * bi + ay * ai, py)
    sol = solve((eq1, eq2), (bi, ai))
    if not sol: return 0
    return 3 * sol[ai] + sol[bi]


print(sum(test_machine(ax, ay, bx, by, px, py) for (ax, ay), (bx, by), (px, py) in machines))
print(sum(test_machine2(ax, ay, bx, by, px + 10000000000000, py + 10000000000000)
          for (ax, ay), (bx, by), (px, py) in machines))
