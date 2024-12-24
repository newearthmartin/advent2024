import re
from collections import defaultdict
from doctest import UnexpectedException

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


def set_wire(wire_gates, wire_vals, wire, val):
    wire_vals[wire] = val
    for w1, op, w2, w3 in wire_gates[wire]:
        if w1 in wire_vals and w2 in wire_vals and w3 not in wire_vals:
            v1 = wire_vals[w1]
            v2 = wire_vals[w2]
            if op == 'AND': result = v1 and v2
            elif op == 'OR': result = v1 or v2
            elif op == 'XOR': result = v1 ^ v2
            else: raise UnexpectedException(f'Unexpected op {op}')
            set_wire(wire_gates, wire_vals, w3, result)


def z_val(wire_vals):
    z_wires = sorted((wire, 1 if val else 0) for wire, val in wire_vals.items() if wire.startswith('z'))
    z_digits = (v for _, v in z_wires)
    return sum((2 ** i) if d else 0 for i, d in enumerate(z_digits))


def run():
    wire_vals = {}
    wire_gates = get_wire_gates()
    for w, v in wires.items():
        set_wire(wire_gates, wire_vals, w, v)
    return z_val(wire_vals)


print(run())
