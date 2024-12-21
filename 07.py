from functools import reduce

with open('input/07.txt') as f:
    lines = [line.strip() for line in f.readlines() if line]

lines = [line.split(': ') for line in lines]
lines = [(int(val), list(map(int, nums.split(' ')))) for val, nums in lines]


def test_vals(val, nums, i, result, concat):
    if i == len(nums): return result == val
    if result > val: return False
    if i == 0:
        possible = [nums[0]]
    elif not concat:
        possible = [result * nums[i], result + nums[i]]
    else:
        possible = [result * nums[i], int(str(result) + str(nums[i])), result + nums[i]]
    return any(test_vals(val, nums, i + 1, p, concat) for p in possible)


results = (val for val, nums in lines if test_vals(val, nums, 0, 0, False))
print(reduce(lambda x, y: x + y, results))

results = (val for val, nums in lines if test_vals(val, nums, 0, 0, True))
print(reduce(lambda x, y: x + y, results))

