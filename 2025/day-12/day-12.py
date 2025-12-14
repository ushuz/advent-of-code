from struct import pack


s = """
0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
"""

s = open("input.txt").read()

sep = 95

# rotate a shape 90 degrees clockwise
def rotate(shape: list[list[int]]) -> list[list[int]]:
    return [list(reversed(col)) for col in zip(*shape)]

# display a shape in # and .
def display(shape: list[list[int]]):
    for row in shape:
        print("".join("#" if c == 1 else "." for c in row))
    print()

shapes_ = s.strip()[:sep].strip().split("\n\n")
shapes = []  # original shapes, each in four rotations
for shape in shapes_:
    # extract the original shape
    _, oshape = shape.split(":\n")
    oshape = [[int(c) for c in l] for l in oshape.strip().replace("#", "1").replace(".", "0").splitlines()]
    oshape90 = rotate(oshape)
    oshape180 = rotate(oshape90)
    oshape270 = rotate(oshape180)
    # flip the shape horizontally and rotate
    fshape = [list(reversed(row)) for row in oshape]
    fshape90 = rotate(fshape)
    fshape180 = rotate(fshape90)
    fshape270 = rotate(fshape180)
    # collect all variants
    oshapes = [oshape, oshape90, oshape180, oshape270, fshape, fshape90, fshape180, fshape270]
    shapes.append(oshapes)

def part1():
    packable = 0

    # parse regions
    regions_ = s.strip()[sep:].strip().splitlines()
    for region in regions_:
        size, counts = region.split(": ")
        w, h = map(int, size.split("x"))
        counts = tuple(map(int, counts.split()))

        # calculate minimum area needed
        min_area = 0
        for c, shape in zip(counts, shapes_):
            shape_area = shape.count("#")
            min_area += c * shape_area

        # sanity check, if region area < min area needed, skip
        if w * h < min_area:
            continue

        # already the answer?
        packable += 1

    return packable

print(part1())
