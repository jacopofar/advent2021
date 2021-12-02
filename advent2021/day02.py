"""
We get a list of commands in the form "direction value", e.g. "forward 3".
The directions are up, down and forward.

In part one up and down change the depth, forward the horizontal axis,
we have to return the produt of the two final values.

In part two an extra variable called aim is introduced with these rules:

    down X increases your aim by X units.
    up X decreases your aim by X units.
    forward X does two things:
        It increases your horizontal position by X units.
        It increases your depth by your aim multiplied by X.
and the solution is again the product of the two axis
"""
def part_one(fr):
    depth, hor = 0, 0
    for line in fr:
        [direction, units] = line.split()
        units = int(units)
        match (direction, units):
            case ("up", v):
                depth -= v
            case ("forward", v):
                hor += v
            case ("down", v):
                depth += v
    return depth * hor

def part_two(fr):
    depth, hor, aim = 0, 0, 0
    for line in fr:
        [direction, units] = line.split()
        units = int(units)
        match (direction, units):
            case ("up", v):
                aim -= v
            case ("forward", v):
                hor += v
                depth += aim * v
            case ("down", v):
                aim += v
    return depth * hor

if __name__ == "__main__":
    with open("input/day02.txt") as fr:
        print(part_one(fr))
        fr.seek(0)
        print(part_two(fr))
