def part_one(coords, folding_instructions):
    print(folding_instructions[0])
    if folding_instructions[0][0] == "x":
        folded = fold_x(coords, folding_instructions[0][1])
    else:
        folded = fold_y(coords, folding_instructions[0][1])
    return len(folded)


def part_two(coords, folding_instructions):
    for direction, value in folding_instructions:
        if direction == "x":
            coords = fold_x(coords, value)
        else:
            coords = fold_y(coords, value)
    visualize(coords)


def visualize(coords):
    xmax = max(x for x, _ in coords)
    ymax = max(y for _, y in coords)
    for y in range(ymax + 1):
        row = ""
        for x in range(xmax + 1):
            if (x, y) in coords:
                row += "#"
            else:
                row += " "
        print(row)


def fold_y(coords, y_val):
    ret = set()
    for x, y in coords:
        if y < y_val:
            ret.add((x, y))
        else:
            ret.add((x, y_val - (y - y_val)))
    return ret


def fold_x(coords, x_val):
    ret = set()
    for x, y in coords:
        if x < x_val:
            ret.add((x, y))
        else:
            ret.add((x_val - (x - x_val), y))
    return ret


if __name__ == "__main__":
    with open("input/day13.txt") as fr:
        coords = set()
        folding_instructions = []
        for line in fr:
            if "," in line:
                x, _, y = line.strip().partition(",")
                coords.add((int(x), int(y)))
            if "=" in line:
                # e.g.: fold along y=7
                desc, _, position = line.strip().partition("=")
                folding_instructions.append((desc[-1], int(position)))
        print(part_one(coords, folding_instructions))
        part_two(coords, folding_instructions)
