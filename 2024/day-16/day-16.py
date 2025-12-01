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

# good inspo found on reddit:
# https://www.reddit.com/r/adventofcode/comments/1hfboft/comment/m2bcfmq/
# https://topaz.github.io/paste/#XQAAAQACAwAAAAAAAAAzHIoib6pXbueH4X9F244lVRDcOZab5q1+VXY/ex42qR7D+RJIsq5/YCi6YHJak4tBC2I+oV44GGsk3yILWGnOyXBRhMTGj1iPohCpnraI7cOVIQMgn6rgSzIs8ivVrbZy5UZbCRK5ynh8s/ewf4aWP/ziHGlRvx+evmR5c+dJCcg4aXptpJ4wX011RpSp9CrrqxfG6AHLLvuWe3uAsiz3BMUMAxoduis7+KevEU1N9ZpXOg+AllGx9HrV+/PBI/U7z4HjfpO5j1HdlhNfEp3Qlhydf4IQ/6nQvX39jWc8fG7LXD/YiMj89zdaG/93MmfrJX7dGkxO5W/kKqZqO/tNiX4gHNh8VgWnSZKMZFStlzAbhBBjgAAhbcxSnU9IFqa2T3RwFdPZVnL0q/xI7M4vq/vbdJo4mVGhuuAZwcCRCk7mwXcJxfVxZDgokb7Njdezsi/RwHybpdPs9vYGGixqU7aEfM+AJGtAU9ALoQN+8xKCaeOkuee7lSEd2Qx6qmuA9mcR7JX34lwmrJd0f8PrWWIjtAYYZP787Tg8B22iFBM02EmP5mt5A+hB7aSrldDMh2mb91VXFf/ztA22
#
# this solution applies the following which make the code more clean and efficient
# - compiles the maze into one-dimension
# - uses complex numbers to represent the direction
# - uses heapq to manage the queue in Dijkstra

from collections import defaultdict
from heapq import heappop, heappush

grid = {i+j*1j: c for i,r in enumerate(open('input.txt'))
                  for j,c in enumerate(r) if c != '#'}

start, = (p for p in grid if grid[p] in 'S')

seen = []
best = 1e9
dist = defaultdict(lambda: 1e9)
todo = [(0, t:=0, start, 1j, [start])]

while todo:
    score, _, pos, dir, path = heappop(todo)

    if score > dist[pos, dir]: continue
    else: dist[pos, dir] = score

    if grid[pos] == 'E' and score <= best:
        seen += path
        best = score

    for rot, pts in (1, 1), (1j, 1001), (-1j, 1001):
        new = pos + dir*rot
        if new in grid:
            heappush(todo, (score + pts, t := t+1,
                new, dir*rot, path + [new]))

print(best, len(set(seen)))
