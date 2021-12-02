def part_one(fr):
    """Count how many lines are greater than the previous one."""
    previous = None
    increases = 0
    for line in fr:
        if line.strip() == "":
            continue
        line_val = int(line)
        if previous is not None and line_val > previous:
            increases += 1
        previous = line_val
    return increases


def part_two(fr):
    """Count how many lines are greater than 4 lines before."""

    a, b, c, d = None, None, None, None
    increases = 0
    for line in fr:
        if line.strip() == "":
            continue
        cur_val = int(line)
        a, b, c, d = b, c, d, cur_val
        if a is None:
            continue
        if d > a:
            increases += 1
    return increases


if __name__ == "__main__":
    with open("input/day01.txt") as fr:
        print(part_one(fr))
        fr.seek(0)
        print(part_two(fr))
