s = open("input.txt").read()

# s = """
# .......S.......
# ...............
# .......^.......
# ...............
# ......^.^......
# ...............
# .....^.^.^.....
# ...............
# ....^.^...^....
# ...............
# ...^.^...^.^...
# ...............
# ..^...^.....^..
# ...............
# .^.^.^.^.^...^.
# ...............
# """

grid = [list(line) for line in s.strip().split("\n")]
h = len(grid)
w = len(grid[0])

def part1():
    # total times of splits
    splits = 0
    # determine 'x' positions of beam positions above
    # starting with 'S' in the first row
    beams = set([grid[0].index('S')])
    # propagate downwards starting from the second row
    for row in grid[1:]:
        # inspect each position in the row
        for x, ch in enumerate(row):
            # skip if there's no beam above
            if x not in beams: continue
            # otherwise, there's a beam coming down
            # for empty spaces, the beam continues down
            if ch == ".": continue
            # for splitters, the beam splits left and right
            if ch == "^":
                beams.add(x - 1)
                beams.add(x + 1)
                # the current beam stops here
                beams.remove(x)
                # incr the counter
                splits += 1
    return splits

def part2():
    start: int = grid[0].index('S')
    # track number of timelines reaching each position
    timelines: list[list[int]] = [[0 for _ in range(w)] for _ in range(h)]
    timelines[0][start] = 1

    for y in range(1, h):
        for x in range(w):
            ts = timelines[y - 1][x]
            if not ts: continue
            ch = grid[y][x]
            # for empty spaces, the beam continues down
            if ch == ".":
                timelines[y][x] += ts
            # for splitters, the beam splits left and right
            if ch == "^":
                timelines[y][x - 1] += ts
                timelines[y][x + 1] += ts

    # sum up all timelines reaching the bottom row
    return sum([t for t in timelines[-1]])

print(part1())
print(part2())
