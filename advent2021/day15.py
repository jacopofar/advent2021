def part_one(cells):
    max_x = max(x for x, _ in cells)
    max_y = max(y for _, y in cells)
    total_risk = dict()
    edge = {(0, 0): 0}
    while True:
        new_edge = dict()
        # for each cell in edge, get the neighbors
        for (x, y), risk_so_far in edge.items():
            # add edge to the total_risk
            total_risk[(x, y)] = risk_so_far
            for (nx, ny) in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                # for each neighbor not already explored
                if (nx, ny) in cells and (nx, ny) not in total_risk:
                    # calculate the risk of that neighbor, add it to new_edge
                    if (nx, ny) in new_edge:
                        new_edge[(nx, ny)] = min(
                            risk_so_far + cells[(nx, ny)],
                            new_edge[(nx, ny)]
                        )
                    else:
                        new_edge[(nx, ny)] = risk_so_far + cells[(nx, ny)]

        # if new_edge is empty, break the cycle
        if len(new_edge) == 0:
            break
        # set edge = new_edge
        edge = new_edge
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
    for row in range(50):
        print("".join([str(new_cells[(row, col)]) for col in range(50)]))
    return part_one(new_cells)


if __name__ == "__main__":
    with open("input/day15.txt") as fr:
        cells = dict()
        for rowi, line in enumerate(fr):
            for coli, v in enumerate(line.strip()):
                cells[(rowi, coli)] = int(v)
    print(part_one(cells))
    raise NotImplementedError(
        "Currently part 2 works on the sample input but not on my real input. There must be an error but I have no time today to troubleshoot :("
    )
    print(part_two(cells))
