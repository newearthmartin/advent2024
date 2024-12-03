import re

with open('03.txt') as f:
    data = f.read()

MUL_DO_DONT_REGEX = r"don't\(\)|do\(\)|mul\(\d\d?\d?,\d\d?\d?\)"
rv1 = 0
rv2 = 0
do = True
for match in re.finditer(MUL_DO_DONT_REGEX, data):
    s = match[0]
    if s == 'do()': do = True
    elif s == "don't()": do = False
    else:
        n1, n2 = (int(n) for n in re.findall(r'\d+', s))
        mul = n1 * n2
        rv1 += mul
        if do: rv2 += mul

print(rv1)
print(rv2)
