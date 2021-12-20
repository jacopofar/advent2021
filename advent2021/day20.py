OFFSETS = {
    (-1, -1): 256,
    (0, -1): 128,
    (1, -1): 64,
    (-1, 0): 32,
    (0, 0): 16,
    (1, 0): 8,
    (-1, 1): 4,
    (0, 1): 2,
    (1, 1): 1,
}

DUMB_PADDING_RANGE = 200


def edges(coords):
    min_x = min(x for x, _ in coords) - 1
    max_x = max(x for x, _ in coords) + 1
    min_y = min(y for _, y in coords) - 1
    max_y = max(y for _, y in coords) + 1
    return (min_x, max_x, min_y, max_y)


def enumerate_points(coords):
    """Generate all coordinates pairs plus a margin of 1.

    The coordinate pairs are generated in order of x, then y.
    """
    min_x, max_x, min_y, max_y = edges(coords)
    y = min_y
    while y <= max_y:
        x = min_x
        while x <= max_x:
            yield x, y
            x += 1
        y += 1


def enhance(algo, coords, background_on: bool):
    # find the limits (can be negative) plus some margin
    # for each element in these limits find the pixels turned on
    # and generate the new set
    image = set()
    min_x, max_x, min_y, max_y = edges(coords)
    for x, y in enumerate_points(coords):
        value = 0
        for (ox, oy), val in OFFSETS.items():
            if (x + ox, y + oy) in coords:
                value += val
            elif background_on:
                if (x + ox) in (min_x, max_x) or (y + oy) in (min_y, max_y):
                    value += val
        # print(x, y, 'is',(x,y) in coords,'has value', value)
        if algo[value] == "#":
            image.add((x, y))
    if background_on:
        return image, False
    else:
        return image, algo[0] == "#"


def dumb_padding(coords):
    min_x, max_x, min_y, max_y = edges(coords)
    return coords.union(
        set(
            [
                (min_x - DUMB_PADDING_RANGE, min_y - DUMB_PADDING_RANGE),
                (max_x + DUMB_PADDING_RANGE, max_y + DUMB_PADDING_RANGE),
            ]
        )
    )


def dumb_trunc(coords):
    min_x, max_x, min_y, max_y = edges(coords)
    return set(
        (x, y)
        for x, y in coords
        if (min_x + DUMB_PADDING_RANGE) < x < (max_x - DUMB_PADDING_RANGE)
        and (min_y + DUMB_PADDING_RANGE) < y < (max_y - DUMB_PADDING_RANGE)
    )


def part_one(algo, coords):
    background_on = False
    coords = dumb_padding(coords)
    visualize(coords, background_on)
    coords, background_on = enhance(algo, coords, background_on)
    print("enhanced:", len(coords))
    visualize(coords, background_on)
    coords, background_on = enhance(algo, coords, background_on)
    print("enhanced:", len(coords))
    visualize(coords, background_on)
    coords = dumb_trunc(coords)
    return len(coords)

def part_two(algo, coords):
    coords = dumb_padding(coords)
    for i in range(50):
        coords, _ = enhance(algo, coords, False)
        print(len(coords))
    coords = dumb_trunc(coords)

    return len(coords)

def visualize(coords, background_on):
    min_x, max_x, min_y, max_y = edges(coords)
    print()
    old_y = None
    row = ""
    for x, y in enumerate_points(coords):
        if old_y != y:
            if old_y is not None:
                print(row)
                row = ""
            old_y = y
        if (x, y) in coords:
            row += "#"
        elif x in (min_x, max_x) or y in (min_y, max_y):
            row += "[#]" if background_on else "[.]"
        else:
            row += "."
    print(row)
    print()


if __name__ == "__main__":
    with open("input/day20.real.txt") as fr:
        lines = fr.read().split("\n")
    algo = lines[0]
    assert len(algo) == 512
    turned_on = set()
    for ri, row in enumerate(lines[2:]):
        for ci, c in enumerate(row):
            if c == "#":
                turned_on.add((ci, ri))

    print(part_one(algo, turned_on))
    print(part_two(algo, turned_on))
