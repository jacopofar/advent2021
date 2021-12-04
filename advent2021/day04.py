BOARD_SIZE = 5


class Board:
    def __init__(self, matrix):
        self.positions = dict()
        for irow, row in enumerate(matrix):
            for icol, val in enumerate(row):
                self.positions[val] = (irow, icol)
        self.marked = set()

    def mark(self, number):
        if number in self.positions:
            self.marked.add(self.positions[number])

    def is_winning(self):
        row_count = [0] * BOARD_SIZE
        column_count = [0] * BOARD_SIZE
        for (r, c) in self.marked:
            row_count[r] += 1
            column_count[c] += 1
        return any(rc == BOARD_SIZE for rc in row_count) or any(
            cc == BOARD_SIZE for cc in column_count
        )

    def get_unmarked(self):
        return [
            n for n, coord in self.positions.items() if coord not in self.marked
        ]

    def __str__(self):
        return f"{self.positions} marked: {self.marked}"


def parse_input(lines):
    drawn_numbers = [int(n) for n in lines[0].split(",")]
    assert (len(lines) - 1) % BOARD_SIZE == 0, "spurious data!"
    boards = []
    for bpos in range(1, len(lines), BOARD_SIZE):
        matrix = [
            [int(v) for v in row.split()]
            for row in lines[bpos : bpos + BOARD_SIZE]
        ]
        boards.append(Board(matrix))
    assert (len(lines) - 1) / 5 == len(boards)

    return drawn_numbers, boards


def part_one(drawn_numbers, boards):
    for dn in drawn_numbers:
        for b in boards:
            b.mark(dn)
        for b in boards:
            if b.is_winning():
                return sum(b.get_unmarked()) * dn


def part_two(drawn_numbers, boards):
    for dn in drawn_numbers:
        for b in boards:
            b.mark(dn)
        survivors = []
        for b in boards:
            if not b.is_winning():
                survivors.append(b)
            else:
                if len(boards) == 1:
                    return sum(b.get_unmarked()) * dn
        boards = survivors


if __name__ == "__main__":
    with open("input/day04.txt") as fr:
        lines = [l for l in fr.read().split("\n") if l.strip() != ""]
    drawn_numbers, boards = parse_input(lines)
    print(part_one(drawn_numbers, boards))
    print(part_two(drawn_numbers, boards))
