s = open("input.txt").read().strip()

# s = """
# 89010123
# 78121874
# 87430965
# 96549874
# 45678903
# 32019012
# 01329801
# 10456732
# """.strip()

import collections

grid = s.splitlines()

max_y = len(grid)
max_x = len(grid[0])

directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

trailheads = []

for y, row in enumerate(grid):
    for x, v in enumerate(row):
        if v == "0": trailheads.append((y, x))

scores = collections.defaultdict(set)
ratings = collections.defaultdict(int)

for trailhead in trailheads:
    def search(y, x):
        v = int(grid[y][x])
        if v == 9:
            scores[trailhead].add((y, x, v))
            ratings[trailhead] += 1
            return
        for dy, dx in directions:
            if 0 <= y + dy < max_y and 0 <= x + dx < max_x:
                if int(grid[y + dy][x + dx]) - v == 1:
                    search(y + dy, x + dx)
    search(*trailhead)

r1 = 0

for trailhead, positions in scores.items():
    r1 += len(positions)

print(r1)

r2 = 0

for trailhead, rating in ratings.items():
    r2 += rating

print(r2)
