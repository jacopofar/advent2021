from collections import Counter


def reaction_step(polymer: dict, reactions: dict):
    """Given a count of couples and the reactions, calculate next step.

    If in the input polymer we have:
        AB -> 23 times
        B0 -> 1 times
    and in reactions we have:
        AB -> R
    we will produce:
        AR -> 23
        RB -> 23
        B0 -> 1
    """
    new_polymer = dict()
    for couple, count in polymer.items():
        # terminator couple, represents the last letter and is "fake"
        # it's simply preserved
        if couple[1] == "0":
            new_polymer[couple] = 1
            continue
        insertion = reactions[couple]

        new_polymer[couple[0] + insertion] = (
            new_polymer.get(couple[0] + insertion, 0) + count
        )
        new_polymer[insertion + couple[1]] = (
            new_polymer.get(insertion + couple[1], 0) + count
        )

    return new_polymer


def count_letters(polymer: dict) -> dict:
    counts = dict()
    for couple, count in polymer.items():
        counts[couple[0]] = counts.get(couple[0], 0) + count
    return counts


def react_and_count(polymer: dict, reactions: dict, steps: int):
    for _ in range(steps):
        polymer = reaction_step(polymer, reactions)
    freqs = list(count_letters(polymer).values())
    return max(freqs) - min(freqs)


def part_one(polymer, reactions):
    return react_and_count(polymer, reactions, 10)


def part_two(polymer, reactions):
    return react_and_count(polymer, reactions, 40)


if __name__ == "__main__":
    with open("input/day14.txt") as fr:
        polymer = dict()
        reactions = dict()
        for line in fr:
            if "->" in line:
                couple, _, insertion = line.strip().partition(" -> ")
                reactions[couple] = insertion
            elif len(line) > 1:
                polymer_str = line.strip() + "0"
                for a, b in zip(polymer_str, polymer_str[1:]):
                    polymer[a + b] = polymer.get(a + b, 0) + 1
    print(part_one(polymer, reactions))
    print(part_two(polymer, reactions))
