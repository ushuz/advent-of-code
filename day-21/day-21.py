from collections import defaultdict
from functools import reduce
import functools
from heapq import heappop, heappush
from itertools import pairwise

s = open("input.txt").read()

# s = """
# 029A
# 980A
# 179A
# 456A
# 379A
# """

codes = s.strip().splitlines()

class hashabledict(dict):
    def __hash__(self):
        return hash(tuple(self.items()))

numpad = ["789", "456", "123", "#0A"]
numpad = hashabledict({y+x*1j: c for y, r in enumerate(numpad) for x, c in enumerate(r) if c != "#"})
numpad_start = 3+2j

dirpad = ["#^A", "<v>"]
dirpad = hashabledict({y+x*1j: c for y, r in enumerate(dirpad) for x, c in enumerate(r) if c != "#"})
dirpad.__hash__ = lambda self: hash(tuple(sorted(self.items())))
dirpad_start = 2j

direction_sc = { "<": -1j, ">": 1j, "^": -1, "v": 1 }
direction_cs = { -1j: "<", 1j: ">", -1: "^", 1: "v" }

def type(pad: dict, activate: complex, seq: str):
    solves = defaultdict(set)
    start = activate
    for idx, ch in enumerate(seq):
        new_start, paths = dijkstra(pad, start, end=ch)
        for path in paths:
            solve = []
            for a, b in pairwise(path):
                if a == b: continue
                solve.append(direction_cs[b-a])
            solve.append("A")
            solves[(idx, pad[start], ch)].add("".join(solve))
        start = new_start
    return solves

@functools.cache
def dijkstra(pad: dict, start: complex, end: str):
    endpos = None
    bestpaths = []
    dist = { start: 1e9 }
    todo = [(t:=0, start, [start])]

    while todo:
        _, pos, path = heappop(todo)

        if pos in dist and len(path) > dist[pos]: continue
        else: dist[pos] = len(path)

        if pad[pos] == end:
            endpos = pos
            bestpaths.append(path + [pos])

        for dir in direction_sc.values():
            new = pos + dir
            if new in pad:
                item = (t:=t+1, new, path + [new])
                # print(end, item)
                heappush(todo, item)

    return endpos, bestpaths

def combine(a, b):
    ret = []
    for va in a:
        for vb in b:
            ret.append(va + vb)
    return ret

r1 = 0

for code in codes:
    robot0 = type(numpad, numpad_start, seq=code)
    robot0r = reduce(combine, robot0.values())

    n = 2
    reduced_prev = robot0r
    for _ in range(n):
        reduced = []
        for seq in reduced_prev:
            robot = type(dirpad, dirpad_start, seq=seq)
            reduced += reduce(combine, robot.values())
        reduced_prev = reduced

    shortest = min(map(len, reduced))
    numeric = int(code[:-1])
    print(f"{shortest} * {numeric}")
    r1 += shortest * numeric

print(r1)

# note: part 1 solution would be impossible for part 2, have to pivot to the "desired" solution
# https://www.reddit.com/r/adventofcode/comments/1hj2odw/comment/m33uf55/

from collections import Counter

numpad = ["789", "456", "123", "#0A"]
numpad = {c: (y, x) for y, r in enumerate(numpad) for x, c in enumerate(r)}

dirpad = ["#^A", "<v>"]
dirpad = {c: (y, x) for y, r in enumerate(dirpad) for x, c in enumerate(r)}

def paths(pad: dict, seq: str, incr: int = 1):
    py, px = pad["A"]
    by, bx = pad["#"]
    counter = Counter()
    for ch in seq:
        ny, nx = pad[ch]
        # if the most direct path goes through the gap, flip, i.e.:
        # - next position is in the same row as the gap and previous position is in the same column as the gap, or
        # - next position is in the same column as the gap and previous position is in the same row as the gap
        flip = ny == by and px == bx or nx == bx and py == by
        # increment by the number of possible paths reaching the current sequence
        counter[(ny-py, nx-px, flip)] += incr
        py, px = ny, nx
    return counter

def solve(n):
    ret = 0
    for code in codes:
        counter = paths(numpad, code)
        for _ in range(n):
            next_counter = Counter()
            for dy, dx, flip in counter:
                # construct directional sequence based on delta y and delta x
                seq = ("<" * -dx + "v" * dy + "^" * -dy + ">" * dx)
                # if "flip" is true, reverse the sequence to avoid the gap
                seq = seq[:: -1 if flip else 1]
                # append the "A" to the end of the sequence
                seq += "A"
                # find the paths for the constructed directional sequence
                # increment by the number of possible paths reaching the current sequence in order to accumulate counts from previous iterations
                next_counter += paths(pad=dirpad, seq=seq, incr=counter[(dy, dx, flip)])
            # pass the counter to next iteration
            counter = next_counter
        shortest = counter.total()
        numeric = int(code[:-1])
        print(f"{shortest} * {numeric}")
        ret += shortest * numeric
    return ret

# total number of directional keypads used, both by robot and human
print(solve(2 + 1))     # part 1
print(solve(25 + 1))    # part 2
