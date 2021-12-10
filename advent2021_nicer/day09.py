def get_neighbors_values(grid, x, y) -> list[int]:
    """Get the numbers in the cells close to the given one."""
    ret = []
    if x > 0:
        ret.append(grid[x - 1][y])
    if y > 0:
        ret.append(grid[x][y - 1])
    if x < len(grid) - 1:
        ret.append(grid[x + 1][y])
    if y < len(grid[0]) - 1:
        ret.append(grid[x][y + 1])
    return ret


def get_neighbors_coords(grid, x, y) -> list[tuple[int, int]]:
    """Get the coordinates of the neighborign cells."""
    ret = []
    if x > 0:
        ret.append((x - 1, y))
    if y > 0:
        ret.append((x, y - 1))
    if x < len(grid) - 1:
        ret.append((x + 1, y))
    if y < len(grid[0]) - 1:
        ret.append((x, y + 1))
    return ret


def local_minima(grid):
    """Find coordinates and 'risk level' of each minima."""
    total = 0
    minima = []
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            neighbors = get_neighbors_values(grid, x, y)
            current = grid[x][y]
            if current < min(neighbors):
                total += current + 1
                minima.append((x, y))
    return total, minima


def part_one(grid):
    return local_minima(grid)[0]


def part_two(grid):
    basin_sizes = []
    # get local minimas (part one)
    for mx, my in local_minima(grid)[1]:
        # the current basin, initially empty
        basin = set()
        # the edge of cells we'll explore at the next cycle
        edge = set([(mx, my)])
        # keep exploring until there's something new
        while len(edge) > 0:
            # the cells to explore in the next steps
            new_edge = set()
            for (x, y) in edge:
                # get the neighbors of a cell in the set
                # they are candidate future cells to explore
                for nx, ny in get_neighbors_coords(grid, x, y):
                    # if this neighbor was already explored, skip it
                    if (nx, ny) in basin or (nx, ny) in edge:
                        continue
                    # also ignore 9, the border of the cell
                    if grid[nx][ny] == 9:
                        continue
                    # this candidate is valid, add it to the new edge
                    new_edge.add((nx, ny))
            # add the edge just explored to the list of cells in the basin
            basin = basin.union(edge)
            # and prepare dor the next cycle, the new edge becomes the current one
            edge = new_edge
        basin_sizes.append(len(basin))
    # take the 3 largest basins, call them a, b, c
    # note: even better use math.prod
    # here I keep that to do like in the video
    [a, b, c] = sorted(basin_sizes, reverse=True)[:3]
    return a * b * c


if __name__ == "__main__":
    with open("input/day09.txt") as fr:
        grid = []
        for line in fr:
            grid.append([int(v) for v in line.strip()])
    print(part_one(grid))
    print(part_two(grid))
