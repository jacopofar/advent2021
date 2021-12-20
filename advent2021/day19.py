from functools import lru_cache
from itertools import permutations
import re

SCANNER_RANGE = 1000
SIGNATURE_RANGE = 155
REQUIRED_MATCHES = 12
AXIS_ROTATIONS = [
    p
    for t in [
        (1, 2, 3),
        (1, 2, -3),
        (1, -2, 3),
        (1, -2, -3),
        (-1, 2, 3),
        (-1, 2, -3),
        (-1, -2, 3),
        (-1, -2, -3),
    ]
    for p in permutations(t)
]


def transform_point(original: tuple, axis, trasl):
    """Transform a point coordinates by axis rotation and offset.

    This would be a lot easier with numpy, but I prefer to not have a
    dependency here. Also, instead of using quaternions I keep the elements
    explicit so the code is easier to follow.

    Note: we don't really care about the correctness of this operation.

    Params
    ------

    original: sequence of int
        The 3 values of the original coordinate
    axis: sequence of int
        The three values from (1, -1, 2, -2, 3, -3) representing the axis
        rotation for example -2 in position 0 means that this value will
        become the axis 1 (1-indexed) and be negative
    trasl: sequence of int
        Three values to add to the result on the three axis, after the rotation

    """
    res = [0, 0, 0]
    for i in range(3):
        res[abs(axis[i]) - 1] = original[i]
        if axis[i] < 0:
            res[abs(axis[i]) - 1] *= -1

    for i, v in enumerate(trasl):
        res[i] += v

    return tuple(res)


def enumerate_transforms(start, end):
    """Given two coordinates, find all possible transformations to get them.

    We have a starting and ending point, we need to find an axis rotation and
    offset that, given to transform_point(), will go from one to the other.
    """
    for axis in AXIS_ROTATIONS:
        end_without_offset = transform_point(start, axis, (0, 0, 0))
        offsets = tuple(s - e for e, s in zip(end_without_offset, end))
        # print('start:', start)
        # print('end:', end)
        # print('end_without_offset', end_without_offset)
        # print('axis', axis)
        # print('offsets', offsets)
        # print('result', transform_point(start, axis, offsets))

        assert end == transform_point(start, axis, offsets)
        yield axis, offsets


def is_valid_transform(coords1, coords2, axis, offset):
    total = 0
    for c1 in coords1:
        if transform_point(c1, axis, offset) in coords2:
            total += 1
            if total == REQUIRED_MATCHES:
                return True
    return False


def find_matching_transform(coords1, coords2, refs1):
    refs2 = find_reference_points(coords2)
    for c1, d1 in refs1.items():
        for c2, d2 in refs2.items():
            if d2 != d1:
                continue
            # NOTE we are looking for a transform from c2 to c1
            for axis, offset in enumerate_transforms(c2, c1):
                if is_valid_transform(coords2, coords1, axis, offset):
                    return axis, offset


def combine_coordinates(scanners):
    absolute_positions = scanners[0]
    absolute_references = find_reference_points(scanners[0])
    total_detected = set()
    scanners_offsets = [None] * len(scanners)
    scanners_offsets[0] = (0, 0, 0)
    while True:
        detected_now = set()
        for idx, coords in enumerate(scanners[1:]):
            if (idx + 1) in total_detected:
                continue
            t = find_matching_transform(
                absolute_positions, coords, absolute_references
            )
            if t is not None:
                print("Found transform for scanner", idx + 1, t)
                scanners_offsets[idx + 1] = t[1]
                detected_now.add(idx + 1)
                total_detected.add(idx + 1)
                for coord in coords:
                    transformed = transform_point(coord, t[0], t[1])
                    # print('Point ', coord, 'becomes', transformed)
                    absolute_positions.add(transformed)
                    for refc, refd in find_reference_points(coords).items():
                        absolute_references[
                            transform_point(refc, t[0], t[1])
                        ] = refd
        if len(detected_now) == 0:
            break
    assert len(total_detected) == len(scanners) - 1
    return absolute_positions, scanners_offsets


def part_one(scanners):
    coords = combine_coordinates(scanners)[0]
    return len(coords)


def part_two(scanners):
    coords = combine_coordinates(scanners)[1]
    max_so_far = 0
    for a1, b1, c1 in coords:
        for a2, b2, c2 in coords:
            distance_a = abs(a1 - a2)
            distance_b = abs(b1 - b2)
            distance_c = abs(c1 - c2)
            this_dist = distance_a + distance_b + distance_c
            if this_dist > max_so_far:
                max_so_far = this_dist
    return max_so_far


def find_reference_points(coords, sig_range=SIGNATURE_RANGE):
    # return {c: 1 for c in coords}
    res = dict()
    signature_limit = SCANNER_RANGE - sig_range
    for a, b, c in coords:
        # print('Examining', (a, b, c))
        if (
            abs(a) > signature_limit
            or abs(b) > signature_limit
            or abs(c) > signature_limit
        ):
            # print('Too close to the edge, skipping')
            continue
        for a2, b2, c2 in coords:
            distance_a = abs(a - a2)
            distance_b = abs(b - b2)
            distance_c = abs(c - c2)
            if not (distance_a and distance_b and distance_c):
                # print('Ignoring same point:', (a2, b2, c2))
                continue
            if (
                distance_a < sig_range
                and distance_b < sig_range
                and distance_c < sig_range
            ):
                res[(a, b, c)] = res.get((a, b, c), 0) + (
                    (distance_a + 1) * (distance_b + 1) * (distance_c + 1)
                )
            # else:
            # print('Ignoring point too far from signature:', (a2, b2, c2))

    return res


def show_signature_distance_results(scanners):
    for sr in range(5, 900, 10):
        total = sum(
            len(find_reference_points(coords, sig_range=sr))
            for coords in scanners
        )
        print(f"With sr of {sr} we got {total} reference points")


if __name__ == "__main__":
    sep = re.compile("[^-\d]+")
    with open("input/day19.txt") as fr:
        scanners = []
        coords = set()
        for line in fr:
            if line.strip() == "":
                continue
            if "scanner" in line:
                # add the coords to the list of scanners
                if len(coords) > 0:
                    scanners.append(coords)
                coords = set()
                continue

            a, b, c = (int(v) for v in sep.split(line) if v != "")
            coords.add((a, b, c))
        # last scanner, add it to the list
        scanners.append(coords)

    # how to choose a signature
    # show_signature_distance_results(scanners)

    print(part_one(scanners))
    print(part_two(scanners))
