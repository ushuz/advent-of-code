s = open("input.txt").read()

from collections import defaultdict

# s = """
# ###############
# #.......#....E#
# #.#.###.#.###.#
# #.....#.#...#.#
# #.###.#####.#.#
# #.#.#.......#.#
# #.#.#####.###.#
# #...........#.#
# ###.#.#####.#.#
# #...#.....#.#.#
# #.#.#.###.#.#.#
# #.....#...#.#.#
# #.###.#.#.#.#.#
# #S..#.....#...#
# ###############"""

# s = """#################
# #...#...#...#..E#
# #.#.#.#.#.#.#.#.#
# #.#.#.#...#...#.#
# #.#.#.#.###.#.#.#
# #...#.#.#.....#.#
# #.#.#.#.#.#####.#
# #.#...#.#.#.....#
# #.#.#####.#.###.#
# #.#.#.......#...#
# #.#.###.#####.###
# #.#.#...#.....#.#
# #.#.#.#####.###.#
# #.#.#.........#.#
# #.#.#.#########.#
# #S#.............#
# #################"""

maze = s.strip().splitlines()
maxdepth = s.count(".") + 5

waypoints = set()

for y, row in enumerate(maze):
    for x, ch in enumerate(row):
        if ch == "S": start = (y, x)
        if ch == "E": end = (y, x)
        if ch in ".SE": waypoints.add((y, x))

best = 1e9
bestpath = []

distances = defaultdict(lambda: defaultdict(lambda: 1e9))

# (distance, y, x, dy, dx): start facing east
q = [(0, *start, 0, 1, [start])]

def update_distance(distance, y, x, dy, dx, path):
    # if distance >= distances[(y, x)][(dy, dx)]: return    # part 2: optimization disabled to find all best paths
    # distances[(y, x)][(dy, dx)] = distance                # part 2: optimization disabled to find all best paths
    q.append((distance, y, x, dy, dx, path))

while q:
    q.sort(key=lambda e: e[0])
    distance, y, x, dy, dx, path = q.pop(0)

    # input("next? "); print(f"{distance=}, {y=}, {x=}, {dy=}, {dx=}, {distances[(y, x)][(dy, dx)]=} {q=}")

    # if current distance is greater than the known distance, skip
    if distances[(y, x)][(dy, dx)] < distance: continue

    # otherwise, update the known distance
    distances[(y, x)][(dy, dx)] = distance

    if (y, x) == end and distance <= best:
        bestpath += path
        best = distance

    # forward
    ny, nx = y + dy, x + dx
    if (ny, nx) in waypoints:
        update_distance(distance + 1, ny, nx, dy, dx, path+[(ny, nx)])

    # right, rotate clockwise
    rdy, rdx = dx, -dy
    ry, rx = y + rdy, x + rdx
    if (ry, rx) in waypoints:
        update_distance(distance + 1001, ry, rx, rdy, rdx, path+[(ry, rx)])

    # left, rotate counter clockwise
    ldy, ldx = -dx, dy
    ly, lx = y + ldy, x + ldx
    if (ly, lx) in waypoints:
        update_distance(distance + 1001, ly, lx, ldy, ldx, path+[(ly, lx)])

print(best)
print(len(set(bestpath)))
