from collections import Counter


def reaction_step(polymer, reactions):
    insertions = [reactions[a + b] for a, b in zip(polymer, polymer[1:])]
    result = ""
    for o, i in zip(polymer, insertions):
        result += o + i
    return result + polymer[-1]


def part_one(polymer, reactions):
    for idx in range(1, 40):
        polymer = reaction_step(polymer, reactions)
        print(idx)
        # print(idx, polymer)
    freq_ranking = Counter(polymer).most_common(None)
    # print(freq_ranking)
    return freq_ranking[0][1] - freq_ranking[-1][1]


def part_two():
    ...


if __name__ == "__main__":
    with open("input/day14.txt") as fr:
        polymer = None
        reactions = dict()
        for line in fr:
            if "->" in line:
                couple, _, insertion = line.strip().partition(" -> ")
                reactions[couple] = insertion
            elif len(line) > 1:
                polymer = line.strip()
    print(part_one(polymer, reactions))
    print(part_two())
