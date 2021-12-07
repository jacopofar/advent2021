def part_one(crabs):
    positions = [0] * max(crabs)
    for crab_position in crabs:
        for pos in range(len(positions)):
            positions[pos] += abs(crab_position - pos)
    return min(positions)


def part_two(crabs):
    positions = [0] * max(crabs)
    for crab_position in crabs:
        for pos in range(len(positions)):
            # the sum as requested by the problem is equivalent to the area
            # of a triangle
            side = abs(crab_position - pos)
            positions[pos] += int((side + 1) * side / 2)
    return min(positions)


if __name__ == "__main__":
    with open("input/day07.txt") as fr:
        crabs = [int(v) for v in fr.read().split(",")]
    print(part_one(crabs))
    print(part_two(crabs))
