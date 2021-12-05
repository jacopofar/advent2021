import re


def enumerate_cells(x1, y1, x2, y2):
    x_vals = list(range(min(x1, x2), max(x1, x2) + 1))
    y_vals = list(range(min(y1, y2), max(y1, y2) + 1))

    if len(x_vals) < len(y_vals):
        x_vals = x_vals * len(y_vals)

    if len(x_vals) > len(y_vals):
        y_vals = y_vals * len(x_vals)
    if x1 > x2:
        x_vals = reversed(x_vals)
    if y1 > y2:
        y_vals = reversed(y_vals)
    yield from zip(x_vals, y_vals)


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
