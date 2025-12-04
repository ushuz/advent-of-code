s = open("input.txt").read()

# s = """
# ..@@.@@@@.
# @@@.@.@.@@
# @@@@@.@.@@
# @.@@@@..@.
# @@.@@@@.@@
# .@@@@@@@.@
# .@.@.@.@@@
# @.@@@.@@@@
# .@@@@@@@@.
# @.@.@@@.@.
# """

grid = [list(line) for line in s.strip().split("\n")]
rows = len(grid)
cols = len(grid[0])

# in bounds check
def in_bounds(r, c):
    return 0 <= r < rows and 0 <= c < cols

directions = [
    (-1, 0), (1, 0), (0, -1), (0, 1),   # up, down, left, right
    (-1, -1), (-1, 1), (1, -1), (1, 1), # diagonals
]

def find_adjacent_cells(y, x):
    adjacent = set()
    for dy, dx in directions:
        ny, nx = y + dy, x + dx
        if in_bounds(ny, nx) and grid[ny][nx] == "@":
            adjacent.add((ny, nx))
    return adjacent

def part1():
    accessible = 0
    for y in range(rows):
        for x in range(cols):
            if grid[y][x] != "@": continue
            adjacent = find_adjacent_cells(y, x)
            accessible += len(adjacent) < 4
    return accessible

def part2():
    checked = set()
    removed = set()

    def dfs(y, x):
        if (y, x) in checked: return
        adjacent = find_adjacent_cells(y, x)
        if len(adjacent) < 4:
            grid[y][x] = "."
            checked.add((y, x))
            removed.add((y, x))
            for ny, nx in adjacent:
                dfs(ny, nx)

    for y in range(rows):
        for x in range(cols):
            if grid[y][x] != "@":
                checked.add((y, x))
                continue
            dfs(y, x)

    return len(removed)

print(part1())
print(part2())
