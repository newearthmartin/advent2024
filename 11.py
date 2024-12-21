from functools import cache

with open('input/11.txt') as f:
    stones = [int(n) for n in f.read().strip().split(' ')]


@cache
def how_many(stone, blinks):
    if blinks == 0: return 1
    elif stone == 0: return how_many(1, blinks - 1)
    else:
        digits = str(stone)
        n_digits = len(digits)
        if len(digits) % 2 == 0:
            stone1 = int(digits[:n_digits // 2])
            stone2 = int(digits[n_digits // 2:])
            return how_many(stone1, blinks - 1) + how_many(stone2, blinks - 1)
        else:
            return how_many(stone * 2024, blinks - 1)


print(sum(how_many(stone, 25) for stone in stones))
print(sum(how_many(stone, 75) for stone in stones))