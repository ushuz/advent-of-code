s = open("input.txt").read()

# s = """
# ###############
# #...#...#.....#
# #.#.#.#.#.###.#
# #S#...#.#.#...#
# #######.#.#.###
# #######.#.#...#
# #######.#.###.#
# ###..E#...#...#
# ###.#######.###
# #...###...#...#
# #.#####.#.###.#
# #.#...#.#.#...#
# #.#.#.#.#.#.###
# #...#...#...###
# ###############"""

s = s.strip().splitlines()
max_y = len(s) - 1
max_x = len(s[0]) - 1

from collections import defaultdict
from heapq import heappop, heappush

grid = set()
wall = set()

for y, r in enumerate(s):
    for x, c in enumerate(r):
        if c != "#": grid.add(y+x*1j)
        if c == "S": start = y+x*1j
        if c == "E": end = y+x*1j
        if c == "#":
            # exclude border wall
            if 0 < y < max_y and 0 < x < max_x: wall.add(y+x*1j)

def dijkstra(grid: set, cheat: complex):
    best = 1e9
    dist = defaultdict(lambda: 1e9)
    todo = [(0, t:=0, start, 1j)]

    while todo:
        score, _, pos, dir = heappop(todo)

        if score > dist[pos]: continue
        else: dist[pos] = score

        if pos == end and score <= best:
            best = score

        for rot, pts in (1, 1), (-1, 1), (1j, 1), (-1j, 1):
            new = pos + dir*rot
            if new in grid or new == cheat:
                item = (score + pts, t := t+1, new, dir*rot)
                heappush(todo, item)

    return best

control = len(grid) - 1  # exclude start

saves1 = defaultdict(int)

import tqdm

for w in tqdm.tqdm(wall):
    pico = dijkstra(grid=grid, cheat=w)
    save = control - pico
    if save > 0: saves1[save] += 1
    print(w, pico, save)

print(sum(v for k, v in saves1.items() if k >= 100))

# note: part 2 was too hard for my conventional thinking, there's actually a really simple and efficient solution:
# https://www.reddit.com/r/adventofcode/comments/1hicdtb/comment/m2y56t8/
#
# breakdown:
# - find the distance from start to every point
# - for every pair of points, calculate their distance (Manhattan distance)
# - if the distance is less than 21, calculate the picoseconds saved if going from a directly to b with cheat
#       e.g. a is 5 steps away from start
#            b is 135 steps away from start
#            Manhattan distance between a and b is 18, well under 20 picoseconds cheat limit
#
#            then, the picoseconds saved if cheat through from a to b is: 135 - 5 - 18 = 112

dist = {start: 0}
todo = [start]

for pos in todo:
    for new in pos-1, pos+1, pos-1j, pos+1j:
        if new in grid and new not in dist:
            dist[new] = dist[pos] + 1
            todo.append(new)

saves2 = defaultdict(int)

for a in dist:
    for b in dist:
        # calculate Manhattan distance
        d = abs((a-b).real) + abs((a-b).imag)
        if d < 21:
            save = dist[a] - dist[b] - d
            if save > 0: saves2[save] += 1

print(sum(v for k, v in saves2.items() if k >= 100))
