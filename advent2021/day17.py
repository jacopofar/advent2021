from functools import lru_cache
import re


def positions(speed_x, speed_y):
    """Generate positions from 0,0 and given speeds"""
    x, y = 0, 0
    while True:
        yield x, y
        x += speed_x
        y += speed_y
        # meh, no sign() yet
        if speed_x != 0:
            speed_x -= 1 if speed_x > 0 else -1
        speed_y -= 1


@lru_cache
def trajectories_and_max_heights(x1, x2, y1, y2):
    # rough guess of max speed that makes sense
    max_speed = max(x1, x2, -y1)
    max_y_reached = 0
    valid_speeds = 0
    # negative x is never a solution, y can be
    for sx in range(max_speed + 1):
        for sy in range(2 * (max_speed + 1)):
            sy -= max_speed + 1
            max_y_in_this = 0
            for x, y in positions(sx, sy):
                max_y_in_this = max(y, max_y_in_this)
                if x1 <= x <= x2 and y1 <= y <= y2:
                    # hit
                    max_y_reached = max(max_y_reached, max_y_in_this)
                    valid_speeds += 1
                    break
                if y < y1 or x > x2:
                    # missed
                    break
    return max_y_reached, valid_speeds


def part_one(x1, x2, y1, y2):
    return trajectories_and_max_heights(x1, x2, y1, y2)[0]


def part_two(x1, x2, y1, y2):
    return trajectories_and_max_heights(x1, x2, y1, y2)[1]


if __name__ == "__main__":
    sep = re.compile("[^-\d]+")
    with open("input/day17.real.txt") as fr:
        x1, x2, y1, y2 = (int(v) for v in sep.split(fr.read()) if v != "")

    print(part_one(x1, x2, y1, y2))
    print(part_two(x1, x2, y1, y2))
