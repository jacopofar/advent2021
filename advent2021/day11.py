SIZE = 10


def all_coords():
    for x in range(SIZE):
        for y in range(SIZE):
            yield x, y


def neighbors(x, y):
    """Generator of valid neighbors, including diagonals."""
    for ox in [-1, 0, 1]:
        for oy in [-1, 0, 1]:
            if ox == 0 and oy == 0:
                continue
            if x + ox >= SIZE or x + ox < 0:
                continue
            if y + oy >= SIZE or y + oy < 0:
                continue
            yield x + ox, y + oy


def next_step(grid: list[list[int]]) -> tuple[list[list[int]], int]:
    new_grid = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
    # step 1: increase of 1 energy levels
    for x, y in all_coords():
        new_grid[x][y] = grid[x][y] + 1
    # step 2: calculate the flashes, an octopus flashes at most once
    flashed = set()
    while True:
        new_flashes = set()
        for x, y in all_coords():
            if new_grid[x][y] > 9:
                if (x, y) not in flashed:
                    new_flashes.add((x, y))
                    for (nx, ny) in neighbors(x, y):
                        new_grid[nx][ny] += 1
        if len(new_flashes) == 0:
            break
        flashed |= new_flashes
    # step 3: reset to 0 flashed octopuses
    for x, y in flashed:
        new_grid[x][y] = 0

    return new_grid, len(flashed)


def part_one(grid):
    total_flashes = 0
    for s in range(1, 101):
        grid, flash_count = next_step(grid)
        for row in grid:
            print("".join(str(n) for n in row))
        total_flashes += flash_count
        print(f"Step: {s} flashes: {flash_count}, total: {total_flashes}")
    return total_flashes


def part_two(grid):
    s = 1
    while True:
        grid, flash_count = next_step(grid)
        print(f"Step: {s} flashes: {flash_count}")
        if flash_count == SIZE ** 2:
            # we could just return here, but I keep it close to the video
            break
        s += 1
    return s


if __name__ == "__main__":
    with open("input/day11.txt") as fr:
        grid = []
        for line in fr:
            grid.append([int(v) for v in line.strip()])

    print(part_one(grid))
    print(part_two(grid))
