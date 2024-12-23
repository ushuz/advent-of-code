from collections import defaultdict

s = open("input.txt").read()

# s = """
# r, wr, b, g, bwu, rb, gb, br

# brwrr
# bggr
# gbbr
# rrbgbr
# ubwu
# bwurrg
# brgr
# bbrgwb
# """

p, d = s.strip().split("\n\n")
patterns = p.split(", ")
patterns_by_length = dict()
for pattern in patterns:
    patterns_by_length.setdefault(len(pattern), [])
    patterns_by_length[len(pattern)].append(pattern)
designs = d.splitlines()

known = defaultdict(int)

counts = []

for design in designs:
    def count(s: str):
        if not s:
            return 1
        rs = 0
        for pattern in patterns:
            if not s.startswith(pattern): continue
            ns = s[len(pattern):]
            if ns not in known:
                known[ns] += count(ns)
            rs += known[ns]
        known[s] = rs
        return rs
    counts.append(count(design))

# part 1
print(len([c for c in counts if c]))
# part 2
print(sum(counts))

# great optimization using @functools.cache:
# https://www.reddit.com/r/adventofcode/comments/1hhlb8g/comment/m2sos6b/

import functools

@functools.cache
def count(design):
    if len(design) == 0:
        return 1
    return sum(count(design.removeprefix(p)) for p in patterns if design.startswith(p))

counts = list(map(count, designs))
print(len([c for c in counts if c]))
print(sum(counts))
