from collections import Counter


def part_one(edges):
    solution = [["start"]]
    while True:
        new_list = []
        # calculate all continuations of solution
        # and put them in new_list
        for path in solution:
            last_node = path[-1]
            if last_node == "end":
                new_list.append(path)
                continue
            for candidate_next in edges[last_node]:
                # if start, ignore it
                if candidate_next == "start":
                    continue
                # if lowercase and already there, ignore it
                if candidate_next.islower() and candidate_next in path:
                    continue
                # otherwise, expand and keep it
                new_list.append(path + [candidate_next])
        # if new_list ha same size of solution, stop
        if len(new_list) == len(solution):
            break
        solution = new_list
    return len(solution)


def part_two():
    solution = [["start"]]
    while True:
        new_list = []
        # calculate all continuations of solution
        # and put them in new_list
        for path in solution:
            last_node = path[-1]
            if last_node == "end":
                new_list.append(path)
                continue
            for candidate_next in edges[last_node]:
                # if start, ignore it
                if candidate_next == "start":
                    continue
                # if lowercase and already there, ignore it
                if candidate_next.islower() and candidate_next in path:
                    c = Counter(path)
                    for edge, count in c.items():
                        if edge.islower() and count > 1:
                            break
                    else:
                        new_list.append(path + [candidate_next])
                    continue
                # otherwise, expand and keep it
                new_list.append(path + [candidate_next])
        # if new_list ha same size of solution, stop
        if len(new_list) == len(solution):
            break
        solution = new_list
    return len(solution)


if __name__ == "__main__":
    with open("input/day12.txt") as fr:
        edges = {}
        for line in fr:
            s, _, e = line.strip().partition("-")
            edges[s] = edges.get(s, []) + [e]
            edges[e] = edges.get(e, []) + [s]

    print(part_one(edges))
    print(part_two())
