import re

def sign(v):
    if v == 0:
        return 0
    if v < 0:
        return -1
    return 1

def enumerate_cells(x1, y1, x2, y2):
    # get how much x and y grow as we move across the segment
    ox = sign(x2 - x1)
    oy = sign(y2 - y1)
    x, y = x1, y1
    while (x, y) != (x2, y2):
        yield x, y
        x += ox
        y += oy
    yield x, y


def count_crosses(segments, ignore_diagonal):
    crosses = dict()
    for x1, y1, x2, y2 in segments:
        if x1 != x2 and y1 != y2 and ignore_diagonal:
            continue
        for x, y in enumerate_cells(x1, y1, x2, y2):
            crosses[(x, y)] = crosses.get((x, y), 0) + 1
    return sum(1 for v in crosses.values() if v > 1)


def part_one(segments):
    return count_crosses(segments, True)


def part_two(segments):
    return count_crosses(segments, False)


if __name__ == "__main__":
    r = re.compile(r"[^\d]+")
    segments = []
    with open("input/day05.txt") as fr:
        for line in fr:
            if line.strip() == "":
                continue
            segment = re.split(r, line)[:4]
            segments.append(tuple(int(c) for c in segment))
    print(part_one(segments))
    print(part_two(segments))
