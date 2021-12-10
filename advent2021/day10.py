PAIRS = {
    '(': ')',
    '[': ']',
    '<': '>',
    '{': '}',
}

SCORES = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

def part_one(lines):
    total = 0
    for line in lines:
        opened = []
        for c in line:
            if c in '([{<':
                opened.append(c)
            else:
                last_opened = opened.pop()
                if PAIRS[last_opened] != c:
                    total += SCORES[c]
                    break
    return total

def part_two():
    ...


if __name__ == "__main__":
    with open("input/day10.txt") as fr:
        lines = fr.read().split('\n')
    print(part_one(lines))
    print(part_two())
