import re
from collections import defaultdict
from itertools import product

with open('input/24.txt') as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

wires = {}
gates = []

for line in lines:
    if ':' in line:
        wire, val = line.split(': ')
        wires[wire] = True if int(val) else False
    else:
        gate = re.match(r'^(\S\S\S) (XOR|AND|OR) (\S\S\S) -> (\S\S\S)$', line).groups()
        gates.append(list(gate))


def get_wire_gates():
    wire_gates = defaultdict(list)
    for gt in gates:
        w1, _, w2, _ = gt
        wire_gates[w1].append(gt)
        wire_gates[w2].append(gt)
    return wire_gates


def clear_wires():
    for w in wires.keys():
        wires[w] = False


def set_wire(wire_gates, wire_vals, w, v):
    wire_vals[w] = v
    for w1, op, w2, w3 in wire_gates[w]:
        if w1 in wire_vals and w2 in wire_vals and w3 not in wire_vals:
            v1 = wire_vals[w1]
            v2 = wire_vals[w2]
            if op == 'AND':
                result = v1 and v2
            elif op == 'OR':
                result = v1 or v2
            elif op == 'XOR':
                result = v1 ^ v2
            else:
                raise Exception(f'Unexpected op {op}')
            set_wire(wire_gates, wire_vals, w3, result)


def z_val(wire_vals):
    on_wires = (w for w, v in wire_vals.items() if v)
    z_wires = (int(w[1:]) for w in on_wires if w.startswith('z'))
    return sum(2 ** w for w in z_wires)


def run():
    wire_vals = {}
    wire_gates = get_wire_gates()
    for w, v in wires.items():
        set_wire(wire_gates, wire_vals, w, v)
    return z_val(wire_vals)


def swap_out_wires(g1, g2):
    g1[3], g2[3] = g2[3], g1[3]


def get_out_wires(comb):
    rv = set()
    for g1, g2 in comb:
        rv.add(g1[3])
        rv.add(g2[3])
    return sorted(rv)


def original_gate(g):
    return next(g0 for g0 in gates if tuple(g) == tuple(g0))


print(run())
print()


def dotest(test_fn, start=None, end=None):
    rv = []
    for i in range(start or 0, end or 45):
        clear_wires()
        if not test_fn(i):
            rv.append(i)
    return rv


def test1(i):
    wires[f'x{i:02}'] = True
    return run() == 2 ** i


def test2(i):
    wires[f'y{i:02}'] = True
    return run() == 2 ** i


def test3(i):
    wires[f'x{i:02}'] = True
    wires[f'y{i:02}'] = True
    return run() == 2 ** (i + 1)


def test4(i):
    if i == 44: return True
    wires[f'x{i:02}'] = True
    wires[f'y{i:02}'] = True
    wires[f'x{i + 1:02}'] = True
    return run() == 2 ** (i + 2)


def test5(i):
    if i == 44: return True
    wires[f'x{i:02}'] = True
    wires[f'y{i:02}'] = True
    wires[f'y{i + 1:02}'] = True
    return run() == 2 ** (i + 2)


def test6(i):
    if i == 44: return True
    wires[f'x{i:02}'] = True
    wires[f'y{i:02}'] = True
    wires[f'x{i + 1:02}'] = True
    wires[f'y{i + 1:02}'] = True
    return run() == 2 ** (i + 1) + 2 ** (i + 2)


def test_single(i):
    errors = [
        dotest(test1, i, i + 1),
        dotest(test2, i, i + 1),
        dotest(test3, i - 1, i),
        dotest(test4, i - 2, i - 1),
        dotest(test5, i - 2, i - 1),
        dotest(test6, i - 2, i - 1)
    ]
    return not any(e for e in errors)


problem_points = dotest(test1)
print(f'Problems at: {problem_points}')


def get_candidate_swaps(pos):
    print(f'Getting candidate swaps for {pos}')
    candidates = []
    for i, g1 in enumerate(gates):
        for j in range(i + 1, len(gates)):
            g2 = gates[j]
            swap_out_wires(g1, g2)
            correct = test_single(pos)
            swap_out_wires(g1, g2)
            if correct:
                swap = sorted([g1, g2])
                candidates.append(swap)
    return candidates


swap_candidates = [get_candidate_swaps(p) for p in problem_points]

# Already computed, uncomment for quicker code:
#
# swap_candidates = [
#     [
#         [['jsq', 'AND', 'vcj', 'z21'], ['shh', 'OR', 'kcq', 'sjk']],
#         [['jsq', 'AND', 'vcj', 'z21'], ['sjk', 'XOR', 'dpc', 'z22']],
#         [['jsq', 'AND', 'vcj', 'z21'], ['jsq', 'XOR', 'vcj', 'shh']]
#     ], [
#         [['y26', 'AND', 'x26', 'vgs'], ['y26', 'XOR', 'x26', 'dtk']]
#     ], [
#         [['dqr', 'XOR', 'wnt', 'z34'], ['jqp', 'AND', 'vkp', 'fdv']],
#         [['dqr', 'XOR', 'wnt', 'z34'], ['x33', 'AND', 'y33', 'mtw']],
#         [['dqr', 'XOR', 'wnt', 'z34'], ['mtw', 'OR', 'fdv', 'z33']],
#         [['jqp', 'AND', 'vkp', 'fdv'], ['vkp', 'XOR', 'jqp', 'dqr']],
#         [['vkp', 'XOR', 'jqp', 'dqr'], ['x33', 'AND', 'y33', 'mtw']],
#         [['mtw', 'OR', 'fdv', 'z33'], ['vkp', 'XOR', 'jqp', 'dqr']]
#     ], [
#         [['jqk', 'XOR', 'vnc', 'z40'], ['x39', 'AND', 'y39', 'z39']],
#         [['gqn', 'XOR', 'sjq', 'pfw'], ['x39', 'AND', 'y39', 'z39']],
#         [['pfw', 'OR', 'kdd', 'jqk'], ['x39', 'AND', 'y39', 'z39']]
#     ]
# ]
# for point in swap_candidates:
#     for swap in point:
#         swap[0] = original_gate(swap[0])
#         swap[1] = original_gate(swap[1])

print()
print('Testing swap candidates')
for comb in product(*swap_candidates):
    for g1, g2 in comb: swap_out_wires(g1, g2)
    results = [
        dotest(test1),
        dotest(test2),
        dotest(test3),
        dotest(test4),
        dotest(test5),
        dotest(test6)
    ]
    for g1, g2 in comb: swap_out_wires(g1, g2)
    if not any(results):
        solution = comb
        break

swap_wires = get_out_wires(solution)
print(','.join(sorted(swap_wires)))

exit()
