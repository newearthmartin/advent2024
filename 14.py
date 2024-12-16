from collections import defaultdict
import time

with open('14.txt') as f:
    lines = (line.strip() for line in f.readlines())
    lines = (line.replace('p=', '')
                 .replace('v=', '')
                 .replace(' ', ',').split(',')
            for line in lines if line)
    robots = [[int(n) for n in line] for line in lines]

lenx = 101
leny = 103


def robot_loop():
    for robot in robots:
        px, py, vx, vy = robot
        robot[0] = (px + vx) % lenx
        robot[1] = (py + vy) % leny


def part1():
    for _ in range(100):
        robot_loop()
    q1 = sum(1 for px, py, _, _ in robots if px < lenx // 2 and py < leny // 2)
    q2 = sum(1 for px, py, _, _ in robots if px > lenx // 2 and py < leny // 2)
    q3 = sum(1 for px, py, _, _ in robots if px < lenx // 2 and py > leny // 2)
    q4 = sum(1 for px, py, _, _ in robots if px > lenx // 2 and py > leny // 2)
    print(q1 * q2 * q3 * q4)


def draw():
    lines = [[' '] * lenx for _ in range(leny)]
    for px, py, _, _ in robots:
        lines[py][px] = '*'
    for line in lines:
        print(''.join(line))
    print('-----------------------------------------------------------------------------------------------------')
    print('-----------------------------------------------------------------------------------------------------')
    print('-----------------------------------------------------------------------------------------------------')


def part2():
    for i in range(7000):
        cols = defaultdict(set)
        robot_loop()
        max_col = 0
        for px, py, _, _ in robots:
            cols[px].add(py)
            max_col = max(max_col, len(cols[px]))
        if max_col > 30:
            print(i + 1)
            draw()
            time.sleep(0.25)


# part1()
part2()
