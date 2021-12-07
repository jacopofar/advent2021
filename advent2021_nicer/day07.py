from collections import Counter


def part_one(crabs):
    """In this optimization we keep a partial sum of the crabs found so far.
    So instead of having a nested for cycle (for positions and crabs) we have
    to iterate only over positions.
    It's faster but the code is a bit longer.
    Notice that we need to do it twice, because the distance is in both
    directions. If it wasn't the case then we wouldn't even need a position
    list, we could keep track of the minimum found so far as we process the
    positions.
    """
    # count crabs for position. Note: we can have many crabs per position
    crabs = Counter(crabs)
    positions = [0] * (max(crabs) + 1)
    # how many crabs we found so far, that is, the slope
    slope = 0
    # the previous value
    previous = 0
    for pos in range(len(positions)):
        # the new position is the previous one + the crabs we found
        # i.e. the amount of crabs so far is the slope
        incr = previous + slope
        positions[pos] += incr
        previous = incr
        # increase the slope with the crabs in this position for the next steps
        # notice that Counter gives 0 if there's nothing
        slope += crabs[pos]

    # now same exact logic but moving from right to left
    slope = 0
    previous = 0
    for pos in reversed(range(len(positions))):
        incr = previous + slope
        positions[pos] += incr
        previous = incr
        slope += crabs[pos]

    return min(positions)


def part_two():
    ...


if __name__ == "__main__":
    with open("input/day07.txt") as fr:
        crabs = [int(v) for v in fr.read().split(",")]
    print(part_one(crabs))
    print(part_two(crabs))
