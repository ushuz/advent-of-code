s = open("input.txt").read()

# s = """
# 3-5
# 10-14
# 16-20
# 12-18

# 1
# 5
# 8
# 11
# 17
# 32
# """

s_ranges, s_ingredients = s.strip().split("\n\n")

ranges = [list(map(int, line.split("-"))) for line in s_ranges.splitlines()]
ingredients = list(map(int, s_ingredients.splitlines()))

def part1():
    fresh = 0
    for ingredient in ingredients:
        fresh += any(a <= ingredient <= b for a, b in ranges)
    return fresh

# brute-force approach doesn't work with extremely large ranges, won't fit in memory
#
# def part2():
#     fresh = set()
#     for a, b in ranges:
#         for f in range(a, b + 1):
#             fresh.add(f)
#     return len(fresh)

def part2():
    merged = []
    for a, b in sorted(ranges):
        # add first range
        if not merged:
            merged.append([a, b])
        # if new 'a' > last 'b', no overlap, append new range
        if a > merged[-1][1]:
            merged.append([a, b])
        # otherwise, there is overlap, extend last range to greater 'b'
        else:
            merged[-1][1] = max(merged[-1][1], b)
    # now every range in 'merged' has no overlap, sum delta of each range
    # +1 to include both ends
    return sum(b - a + 1 for a, b in merged)

print(part1())
print(part2())
