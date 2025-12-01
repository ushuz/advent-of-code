s = open("input.txt").read().strip()

# s = """
# RRRRIICCFF
# RRRRIICCCF
# VVRRRCCFFF
# VVRCCCJFFF
# VVVVCJJCFE
# VVIVCCJJEE
# VVIIICJJEE
# MIIIIIJJEE
# MIIISIJEEE
# MMMISSJEEE""".strip()

# s = """
# EEEEE
# EXXXX
# EEEEE
# EXXXX
# EEEEE""".strip()

# s = """
# AAAAAA
# AAABBA
# AAABBA
# ABBAAA
# ABBAAA
# AAAAAA""".strip()

grid = s.splitlines()
max_y = len(grid)
max_x = len(grid[0])
directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

regions = []

visited = set()

def find_region(plant: str, region: set, y: int, x: int):
    if (y, x) in visited: return False
    if grid[y][x] != plant: return False
    visited.add((y, x))
    region.add((y, x))
    for dy, dx in directions:
        ny, nx = y + dy, x + dx
        if 0 <= ny < max_x and 0 <= nx < max_y:
            find_region(plant, region, ny, nx)

for y, row in enumerate(grid):
    for x, cell in enumerate(row):
        if (y, x) in visited: continue
        region = set()
        plant = grid[y][x]
        find_region(plant, region, y, x)
        regions.append((plant, region))

import itertools

def calculate_perimeter(region: set):
    adj = 0
    for (y1, x1), (y2, x2) in itertools.combinations(region, 2):
        adj += abs(y1 - y2) + abs(x1 - x2) == 1
    return len(region) * 4 - adj * 2

r1 = 0

for plant, region in regions:
    aera = len(region)
    perimeter = calculate_perimeter(region)
    # print(plant, aera, perimeter)
    r1 += aera * perimeter

print(r1)

import collections

region_edges = collections.defaultdict(set)

def find_edges(region: set):
    key = tuple(sorted(region))
    for y, x in region:
        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            ey, ex = y + dy * .1, x + dx * .1
            if (ny, nx) not in region:
                region_edges[key].add((ey, ex))

for plant, region in regions:
    find_edges(region)

def calculate_sides(edges: set):
    sides = []
    connected = set()
    for ey, ex in sorted(edges):
        side = []
        # horizontal: ey ends with .1 or .9
        if str(ey).endswith(".1") or str(ey).endswith(".9"):
            hov = [(0, 1), (0, -1)]
        # vertical: ex ends with .1 or .9
        if str(ex).endswith(".1") or str(ex).endswith(".9"):
            hov = [(1, 0), (-1, 0)]
        # connect edges horizontally or vertically
        def connect(y, x):
            if (y, x) in connected: return
            connected.add((y, x))
            side.append((y, x))
            for dy, dx in hov:
                ny, nx = y + dy, x + dx
                # print(f"{y=}, {x=} {dy=} {dx=} -> {ny=}, {nx=}: {(ny, nx) in edges}")
                if (ny, nx) in edges:
                    connect(ny, nx)
        connect(ey, ex)
        if side: sides.append(sorted(side))
    return sides

r2 = 0

for region, edges in region_edges.items():
    area = len(region)
    sides = calculate_sides(edges)
    nsides = len(sides)
    r2 += area * nsides

print(r2)
