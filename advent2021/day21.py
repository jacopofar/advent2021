# throwing 3 1-3 dices, how often we get these sums:
DIRAC_DICE_OUTCOMES = {
    3: 1,
    4: 3,
    5: 6,
    6: 7,
    7: 6,
    8: 3,
    9: 1,
}


def deterministic_dice():
    n = 1
    while True:
        yield n
        n += 1
        if n == 101:
            n = 1


def part_one(p1, p2):
    roll_count = 0
    d = deterministic_dice()
    score1, score2 = 0, 0
    while True:
        s1 = next(d) + next(d) + next(d)
        roll_count += 3
        p1 = ((p1 + s1 - 1) % 10) + 1
        score1 += p1
        if score1 >= 1000:
            print(f"p1 wins, after {roll_count} total rolls, p2 is {score2}")
            return roll_count * score2

        s2 = next(d) + next(d) + next(d)
        roll_count += 3
        p2 = ((p2 + s2 - 1) % 10) + 1
        score2 += p2
        if score2 >= 1000:
            # print(f'p2 win, after {roll_count} total rolls, p1 is {score1}')
            return roll_count * score1


def part_two(p1, p2):
    multiverse_count = {(p1, 0, p2, 0): 1}
    winners_count = {
        1: 0,
        2: 0,
    }
    while len(multiverse_count) > 0:
        # print('multiverse-count:', multiverse_count)
        # print('winners:', winners_count)
        new_multiverse_count = dict()
        for (p1, s1, p2, s2), count in multiverse_count.items():
            for add_score, cases in DIRAC_DICE_OUTCOMES.items():
                p1_case = ((p1 + add_score - 1) % 10) + 1
                s1_case = p1_case + s1
                if s1_case >= 21:
                    winners_count[1] += cases * count
                else:
                    state = (p1_case, s1_case, p2, s2)
                    # add to the multiverses the cases multiplied by dice count
                    if state in new_multiverse_count:
                        new_multiverse_count[state] += cases * count
                    else:
                        new_multiverse_count[state] = cases * count
        multiverse_count = new_multiverse_count

        # print(' after p1 multiverse-count:', multiverse_count)
        # print(' after p1 winners:', winners_count)

        multiverse_count = new_multiverse_count
        new_multiverse_count = dict()
        for (p1, s1, p2, s2), count in multiverse_count.items():
            for add_score, cases in DIRAC_DICE_OUTCOMES.items():
                p2_case = ((p2 + add_score - 1) % 10) + 1
                s2_case = s2 + p2_case
                if s2_case >= 21:
                    winners_count[2] += cases * count
                else:
                    state = (p1, s1, p2_case, s2_case)
                    # add to the multiverses the cases multiplied by dice count
                    if state in new_multiverse_count:
                        new_multiverse_count[state] += cases * count
                    else:
                        new_multiverse_count[state] = cases * count
        multiverse_count = new_multiverse_count
        # print(' after p2 multiverse-count:', multiverse_count)
        # print(' after p2 winners:', winners_count)

    return max(winners_count.values())


if __name__ == "__main__":
    with open("input/day21.txt") as fr:
        lines = fr.read().split("\n")
    p1 = int(lines[0].split("position: ")[1])
    p2 = int(lines[1].split("position: ")[1])

    print(part_one(p1, p2))
    print(part_two(p1, p2))
