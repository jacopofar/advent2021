import re


def part_one(problem_input):
    ret = 0

    for patterns, values in problem_input:
        for value in values:
            if len(value) in (2, 4, 3, 7):
                ret += 1
    return ret


def calculate_mapping(patterns):
    counts = {s: sum(1 for p in patterns if s in p) for s in "abcdefg"}
    segments_in_four = [p for p in patterns if len(p) == 4][0]
    mapping = {}

    for letter, count in counts.items():
        if count == 4:
            mapping[letter] = "e"
        if count == 6:
            mapping[letter] = "b"
        if count == 7:
            if letter in segments_in_four:
                mapping[letter] = "d"
            else:
                mapping[letter] = "g"
        if count == 8:
            if letter in segments_in_four:
                mapping[letter] = "c"
            else:
                mapping[letter] = "a"
        if count == 9:
            mapping[letter] = "f"
    return mapping


DECODINGS = dict(
    cf=1,
    acdeg=2,
    acdfg=3,
    bcdf=4,
    abdfg=5,
    abdefg=6,
    acf=7,
    abcdefg=8,
    abcdfg=9,
    abcefg=0,
)


def decode_value(mapping, value) -> str:
    mapped = sorted([mapping[v] for v in value])
    return str(DECODINGS["".join(mapped)])


def part_two(problem_input):
    total = 0
    for patterns, values in problem_input:
        mapping = calculate_mapping(patterns)
        digits = "".join([decode_value(mapping, v) for v in values])
        total += int(digits)
    return total


if __name__ == "__main__":
    sep = re.compile("[^a-g]+")
    with open("input/day08.txt") as fr:
        problem_input = []
        for line in fr:
            parts = sep.split(line)
            pattern = parts[:10]
            value = parts[10:14]
            problem_input.append((pattern, value))
    print(part_one(problem_input))
    print(part_two(problem_input))
