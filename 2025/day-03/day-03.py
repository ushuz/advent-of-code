s = open("input.txt").read()

# s = """
# 987654321111111
# 811111111111119
# 234234234234278
# 818181911112111
# """

def find_max_joltage(bank):
    max_ = 0
    for idx, i in enumerate(bank[:-1]):
        for j in bank[idx+1:]:
            joltage = int(f"{i}{j}")
            if joltage > max_:
                max_ = joltage
    return max_

def part1():
    sum = 0
    for bank in s.strip().splitlines():
        sum += find_max_joltage(bank)
    return sum

import functools

@functools.cache
def find_max_joltage_k(bank, k):
    n = len(bank)

    if k == 0: return 0
    if n == k: return int("".join(bank))

    # a: take this joltage, plus max k-1 from the rest
    # for the 12th digit, multiply by 10 ^ (12 - 1)
    a = int(bank[0]) * 10 ** (k - 1) + find_max_joltage_k(bank[1:], k - 1)

    # b: skip this joltage, take max k from the rest
    b = find_max_joltage_k(bank[1:], k)

    # find max of the two
    return max(a, b)

def part2():
    sum = 0
    for bank in s.strip().splitlines():
        sum += find_max_joltage_k(bank, 12)
    return sum

print(part1())
print(part2())
