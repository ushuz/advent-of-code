s = open("input.txt").read()

# s = """
# 7,1
# 11,1
# 11,7
# 9,7
# 9,5
# 2,5
# 2,3
# 7,3
# """

def part1():
    red_tiles = [tuple(map(int, line.split(","))) for line in s.strip().split("\n")]
    n = len(red_tiles)

    max_area = 0
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = red_tiles[i]
            x2, y2 = red_tiles[j]
            area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
            max_area = max(max_area, area)
    return max_area

def part2():
    red_tiles = [tuple(map(int, line.split(","))) for line in s.strip().split("\n")]
    n = len(red_tiles)

    edges = set(red_tiles)

    import collections
    edges_vertical = collections.defaultdict(set)
    edges_horizontal = collections.defaultdict(set)

    # walk every edge
    for i in range(n):
        x1, y1 = red_tiles[i]
        x2, y2 = red_tiles[(i + 1) % n]
        xmin, xmax = min(x1, x2), max(x1, x2)
        ymin, ymax = min(y1, y2), max(y1, y2)
        for x in range(xmin, xmax + 1):
            for y in range(ymin, ymax + 1):
                edges.add((x, y))
                # only one end of the edge should be included to correctly count crossed edges with ray-casting
                # opt to include the min end, exclude the max end
                if x1 == x2 and y < ymax: edges_vertical[y].add(x)
                if y1 == y2 and x < xmax: edges_horizontal[x].add(y)

    def is_inside(x, y):
        # true if the point is on edge
        if (x, y) in edges: return True
        # otherwise, use ray-casting method
        # cast a ray to any direction, straight-right in our case, count how many edges it crosses
        #    odd = inside
        #   even = outside
        edges_crossed = [ex for ex in edges_vertical[y] if ex > x]
        return len(edges_crossed) % 2 == 1

    max_area = 0
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = red_tiles[i]
            x2, y2 = red_tiles[j]

            # check if all four corners are inside, skip if not
            if not all([
                is_inside(x1, y1),
                is_inside(x1, y2),
                is_inside(x2, y1),
                is_inside(x2, y2),
            ]):
                continue

            # FIXME: too slow to check every tile along the bounds
            #
            # # check if all four bounds are inside, skip if not
            # if not all([
            #     all(is_inside(x, y1) for x in range(min(x1, x2), max(x1, x2) + 1)),
            #     all(is_inside(x, y2) for x in range(min(x1, x2), max(x1, x2) + 1)),
            #     all(is_inside(x1, y) for y in range(min(y1, y2), max(y1, y2) + 1)),
            #     all(is_inside(x2, y) for y in range(min(y1, y2), max(y1, y2) + 1)),
            # ]):
            #     continue

            # check if all four bounds are inside, skip if not
            # optimized by:
            #   1. finding intersections between the bounds and the crossing edges
            #      include x-min and y-min, exclude x-max and y-max, to avoid out-of-bounds
            ymin, ymax = min(y1, y2), max(y1, y2)
            xmin, xmax = min(x1, x2), max(x1, x2)
            x1ys = sorted([y for y in edges_horizontal[x1] if ymin <= y < ymax])
            x2ys = sorted([y for y in edges_horizontal[x2] if ymin <= y < ymax])
            y1xs = sorted([x for x in edges_vertical[y1] if xmin <= x < xmax])
            y2xs = sorted([x for x in edges_vertical[y2] if xmin <= x < xmax])
            #   2. check if the segments between intersections are inside
            #      we only need to check one tile per segment, e.g. the tile immediately off by one beyond the intersection
            if not all([
                all([is_inside(x1, y+1) for y in x1ys]) if x1ys else True,
                all([is_inside(x2, y+1) for y in x2ys]) if x2ys else True,
                all([is_inside(x+1, y1) for x in y1xs]) if y1xs else True,
                all([is_inside(x+1, y2) for x in y2xs]) if y2xs else True,
            ]):
                continue

            area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
            max_area = max(max_area, area)

            # # log every time we find a new largest rectangle
            # if area == max_area:
            #     print(i, j, (x1, y1), (x2, y2), area)

    return max_area

print(part1())
print(part2())
