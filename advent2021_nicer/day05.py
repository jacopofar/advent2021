import re

# how many cells to consider in an interation
# essentially, save time or use more memory
TILE_SIZE = 500_000


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


def count_crosses(segments, ignore_diagonal, min_x, max_x, min_y, max_y):
    crosses = dict()
    for x1, y1, x2, y2 in segments:
        if x1 != x2 and y1 != y2 and ignore_diagonal:
            continue
        # # immediately skip segments completely outside this tile
        if min(x1, x2) > max_x:
             continue
        if max(x1, x2) < min_x:
             continue
        if min(y1, y2) > max_y:
             continue
        if max(y1, y2) < min_y:
             continue
        for x, y in enumerate_cells(x1, y1, x2, y2):
            if min_x <= x < max_x and min_y <= y < max_y:
                crosses[(x, y)] = crosses.get((x, y), 0) + 1
    return sum(1 for v in crosses.values() if v > 1)


def total_space(segments):
    return (
        max(max(v[0], v[1]) for v in segments),
        max(max(v[2], v[3]) for v in segments),
    )


def part_one(segments):
    total = 0
    max_x, max_y = total_space(segments)
    for x in range(0, max_x + 1, TILE_SIZE):
        for y in range(0, max_y + 1, TILE_SIZE):
            print(x, y, total)
            total += count_crosses(segments, True, x, x + TILE_SIZE, y, y + TILE_SIZE)
    return total


def part_two(segments):
    total = 0
    max_x, max_y = total_space(segments)
    for x in range(0, max_x + 1, TILE_SIZE):
        for y in range(0, max_y + 1, TILE_SIZE):
            # print(x, y, total)
            total += count_crosses(segments, False, x, x + TILE_SIZE, y, y + TILE_SIZE)
    return total


if __name__ == "__main__":
    r = re.compile(r"[^\d]+")
    segments = []
    with open("input/day05.txt") as fr:
        for line in fr:
            if line.strip() == "":
                continue
            segment = re.split(r, line)[:4]
            segments.append(tuple(int(c) for c in segment))
    sol1 = part_one(segments)
    print(sol1)
    sol2 = part_two(segments)
    print(sol2)
