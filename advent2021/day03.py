def count_zeros_ones(numbers: list[str]) -> tuple[list[int], list[int]]:
    """Count how often a 0 or 1 digit appears in each position.

    The numbers are strings of 0s and 1s, all with the same length.
    """
    ones = None
    for line in numbers:
        if ones is None:
            ones = [0] * (len(line))
        for idx, digit in enumerate(line):
            if digit == "1":
                ones[idx] += 1
    return [len(numbers) - v for v in ones], ones


def part_one(lines):
    """Return the most common values in each position, multiplied as decimals."""
    zeros, ones = count_zeros_ones(lines)
    gamma, epsilon = "", ""
    for z, o in zip(zeros, ones):
        if o > z:
            gamma += "1"
            epsilon += "0"
        else:
            gamma += "0"
            epsilon += "1"
    gamma = int(gamma, 2)
    epsilon = int(epsilon, 2)
    return gamma * epsilon


def part_two(lines):
    """Filter by most and leats common prefix iteratively, multiply the results."""

    r1 = find_rating(lines, "high")
    r2 = find_rating(lines, "low")
    return r1 * r2


def find_rating(lines, criteria):
    prefix = ""
    while len(lines) > 1:
        zeros, ones = count_zeros_ones(lines)
        idx = len(prefix)
        if criteria == "high":
            if zeros[idx] > ones[idx]:
                prefix += "0"
            else:
                prefix += "1"
        elif criteria == "low":
            if zeros[idx] <= ones[idx]:
                prefix += "0"
            else:
                prefix += "1"
        else:
            raise ValueError(f"Unknown criteria {criteria}")
        lines = [l for l in lines if l.startswith(prefix)]

    return int(lines[0], 2)


if __name__ == "__main__":
    with open("input/day03.txt") as fr:
        lines = fr.read().split("\n")
    print(part_one(lines))
    print(part_two(lines))
