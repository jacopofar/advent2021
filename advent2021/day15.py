from queue import PriorityQueue


def part_one(cells):
    """Find shortest path cost using Dijkstra"""
    max_x = max(x for x, _ in cells)
    max_y = max(y for _, y in cells)
    total_risk = dict()
    to_explore = PriorityQueue()
    to_explore.put((0, (0, 0)))
    while not to_explore.empty():
        cost, (x, y) = to_explore.get()
        # an element may be put multiple times in the queue
        # duplicates are sub-optimal, ignore them
        if (x, y) in total_risk:
            continue
        total_risk[(x, y)] = cost
        for (nx, ny) in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
            # for each neighbor not already explored
            if (nx, ny) in cells and (nx, ny) not in total_risk:
                to_explore.put((cost + cells[(nx, ny)], (nx, ny)))
    return total_risk[(max_x, max_y)]


def expand_cells(original_cells):
    max_x = max(x for x, _ in original_cells)
    max_y = max(y for _, y in original_cells)
    result = dict()
    for tx in range(5):
        for ty in range(5):
            for (x, y), v in original_cells.items():
                new_value = (((v + tx + ty) - 1) % 9) + 1
                result[
                    (x + (max_x + 1) * tx), (y + (max_y + 1) * ty)
                ] = new_value
    return result


def part_two(original_cells):
    new_cells = expand_cells(original_cells)
    # for row in range(50):
    #     print("".join([str(new_cells[(row, col)]) for col in range(50)]))

    return part_one(new_cells)


if __name__ == "__main__":
    with open("input/day15.txt") as fr:
        cells = dict()
        for rowi, line in enumerate(fr):
            for coli, v in enumerate(line.strip()):
                cells[(rowi, coli)] = int(v)

    print(part_one(cells))
    print(part_two(cells))
