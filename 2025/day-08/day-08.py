s = open("input.txt").read()
p = 1000

# s = """
# 162,817,812
# 57,618,57
# 906,360,560
# 592,479,940
# 352,342,300
# 466,668,158
# 542,29,236
# 431,825,988
# 739,650,466
# 52,470,668
# 216,146,977
# 819,987,18
# 117,168,530
# 805,96,715
# 346,949,466
# 970,615,88
# 941,993,340
# 862,61,35
# 984,92,344
# 425,690,689
# """
# p = 10

def distance(box1, box2):
    # euclidean distance squared
    return sum((abs(a - b) ** 2) for a, b in zip(box1, box2))

def part1():
    boxes = [tuple(map(int, line.split(","))) for line in s.strip().split("\n")]
    n = len(boxes)

    # calculate all pairwise distances
    closest = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = distance(boxes[i], boxes[j])
            closest.append((dist, (i, j)))
    closest.sort()

    # track connected circuits
    circuits: list[set[int]] = []

    # connect 'p' closest pairs
    for dist, (i, j) in closest[:p]:
        union = set([i, j])
        tbd = []
        # merge with any existing circuits that intersect
        for idx, circuit in enumerate(circuits):
            # no intersection, skip
            if not circuit.intersection(union):
                continue
            # merge circuits
            union = union.union(circuit)
            # record index to be deleted
            tbd.append(idx)
        # delete connecting circuits, in reverse order to avoid messing up indices
        for idx in reversed(tbd):
            circuits.pop(idx)
        # append the merged circuit
        circuits.append(union)

    # multiply the sizes of the three largest circuits
    circuits.sort(key=len, reverse=True)
    product = 1
    for circuit in circuits[:3]:
        product *= len(circuit)

    return product

def part2():
    boxes = [tuple(map(int, line.split(","))) for line in s.strip().split("\n")]
    n = len(boxes)

    # calculate all pairwise distances
    closest = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = distance(boxes[i], boxes[j])
            closest.append((dist, (i, j)))
    closest.sort()

    # track connected circuits
    circuits: list[set[int]] = []

    # connect closest pairs until stop
    cursor = 0
    result = 0
    while not result:
        dist, (i, j) = closest[cursor]
        union = set([i, j])
        tbd = []
        # merge with any existing circuits that intersect
        for idx, circuit in enumerate(circuits):
            # no intersection, skip
            if not circuit.intersection(union):
                continue
            # merge circuits
            union = union.union(circuit)
            # record index to be deleted
            tbd.append(idx)
        # delete connecting circuits, in reverse order to avoid messing up indices
        for idx in reversed(tbd):
            circuits.pop(idx)
        # append the merged circuit
        circuits.append(union)
        # move to next closest pair
        cursor += 1

        # once we have one big circuit that includes all boxes
        # i.e. len(union) == n, stop and return the product of their X coordinates
        if len(union) >= n:
            result = boxes[i][0] * boxes[j][0]
            break

    return result

print(part1())
print(part2())
