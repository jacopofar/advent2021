from collections import Counter


def evolve_population(fishes, day_count):
    c = Counter(fishes)
    current_generation = [c[t] for t in range(9)]
    print("Initial population:", current_generation)
    for day in range(1, day_count + 1):
        new_generation = current_generation[1:]
        new_generation.append(current_generation[0])
        new_generation[6] = current_generation[0] + current_generation[7]
        print(
            f"Population at day {day}: {new_generation} (sum: {sum(new_generation)})"
        )
        current_generation = new_generation
    return sum(current_generation)


def part_one(fishes):
    return evolve_population(fishes, 80)


def part_two(segments):
    return evolve_population(fishes, 256)


if __name__ == "__main__":
    with open("input/day06.txt") as fr:
        fishes = [int(v) for v in fr.read().split(",")]
    print(part_one(fishes))
    print(part_two(fishes))
