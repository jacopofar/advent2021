import re


def do_they_intersect(cuboid1, cuboid2):
    ax1, ax2, ay1, ay2, az1, az2 = cuboid1
    bx1, bx2, by1, by2, bz1, bz2 = cuboid2
    return (
        (ax1 < bx2)
        and (bx1 < ax2)
        and (ay1 < by2)
        and (by1 < ay2)
        and (az1 < bz2)
        and (bz1 < az2)
    )


def enumerate_uniform_regions(cuboids):
    """Enumerate cuboids completely on or off.

    It splits the whole space according to the bounds of each cuboid.
    """
    xs = set()
    ys = set()
    zs = set()

    for (x1, x2, y1, y2, z1, z2) in cuboids:
        xs.add(x1)
        xs.add(x2)
        ys.add(y1)
        ys.add(y2)
        zs.add(z1)
        zs.add(z2)
    bounds_x = sorted(xs)
    bounds_y = sorted(ys)
    bounds_z = sorted(zs)

    for x1, x2 in zip(bounds_x, bounds_x[1:]):
        for y1, y2 in zip(bounds_y, bounds_y[1:]):
            for z1, z2 in zip(bounds_z, bounds_z[1:]):
                yield (x1, x2, y1, y2, z1, z2)


def is_completely_inside(container, candidate_contained):
    ax1, ax2, ay1, ay2, az1, az2 = container
    bx1, bx2, by1, by2, bz1, bz2 = candidate_contained
    # a comparison here is not necessary (we know bx1 <= bx)
    # but it's nice to see and imagine them in order
    # makes the formula easier to read
    return (
        (ax1 <= bx1 <= bx2 <= ax2)
        and (ay1 <= by1 <= by2 <= ay2)
        and (az1 <= bz1 <= bz2 <= az2)
    )


def add_cube_or_hole(initial_cuboids, cuboid_to_add, is_hole):
    cuboids = []
    for c in initial_cuboids:
        # are we adding something pointless? return
        if is_completely_inside(c, cuboid_to_add) and not is_hole:
            # print('This cuboid is already there! doing nothing')
            return initial_cuboids
        if is_completely_inside(cuboid_to_add, c):
            # either is gone because inside the hole,
            # or is unused because this new cuboid will cover it
            # print('pruning eclipsed cuboid', c)
            continue
        cuboids.append(c)
    result = []
    to_repartition = []
    for old_c in cuboids:
        # not affected, keep as is
        if not do_they_intersect(old_c, cuboid_to_add):
            result.append(old_c)
        else:
            to_repartition.append(old_c)
    to_repartition.append(cuboid_to_add)
    for candidate in enumerate_uniform_regions(to_repartition):
        # is this lost because we are cutting it? skip
        if is_hole and do_they_intersect(candidate, cuboid_to_add):
            # print('removing the hole:', candidate, 'intersecting', cuboid_to_add)
            continue
        # we are not cutting it, check that is to keep
        for cuboid in to_repartition:
            if do_they_intersect(cuboid, candidate):
                result.append(candidate)
                break

    return result


def part_two(commands):
    cuboids = []
    for command, cuboid in commands:
        # this is because the end coordinate is inclusive
        # and is much easier to handle coordinates that are not
        x1, x2, y1, y2, z1, z2 = cuboid
        cuboid = (x1, x2 + 1, y1, y2 + 1, z1, z2 + 1)

        # print('Before running ', command, cuboid, 'there are', len(cuboids))
        # print(cuboids)
        cuboids = add_cube_or_hole(cuboids, cuboid, command == "off")
        # print(cuboids)

    total = 0
    for (x1, x2, y1, y2, z1, z2) in cuboids:
        total += (x2 - x1) * (y2 - y1) * (z2 - z1)
    return total


def enumerate_coords_in_region(cuboid_tuple):
    x1, x2, y1, y2, z1, z2 = cuboid_tuple
    x = x1
    while x <= x2:
        y = y1
        while y <= y2:
            z = z1
            while z <= z2:
                yield x, y, z
                z += 1
            y += 1
        x += 1


def intersect_cuboids(cuboid1, cuboid2):
    ax1, ax2, ay1, ay2, az1, az2 = cuboid1
    bx1, bx2, by1, by2, bz1, bz2 = cuboid2
    return (
        max(ax1, bx1),
        min(ax2, bx2),
        max(ay1, by1),
        min(ay2, by2),
        max(az1, bz1),
        min(az2, bz2),
    )


def calculate_end_state_in_region(commands, region):
    cells_on = set()
    for c, target in commands:
        affected = intersect_cuboids(region, target)
        for x, y, z in enumerate_coords_in_region(affected):
            if c == "on":
                cells_on.add((x, y, z))
            elif c == "off":
                try:
                    cells_on.remove((x, y, z))
                except KeyError:
                    pass
            else:
                raise ValueError(f"Unknown command {c}")
    return cells_on


def part_one(commands):
    return len(
        calculate_end_state_in_region(commands, (-50, 50, -50, 50, -50, 50))
    )


if __name__ == "__main__":
    commands = []
    sep = re.compile("[^-\d]+")
    with open("input/day22.txt") as fr:
        for line in fr:
            # off x=9..11,y=9..11,z=9..11
            command, _, coords = line.strip().partition(" ")
            commands.append(
                (command, tuple(int(v) for v in sep.split(coords) if v != ""))
            )

    print(part_one(commands))
    print(part_two(commands))
