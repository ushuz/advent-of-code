s = open("input.txt").read().strip()

# s = "125 17"

stones = [int(x) for x in s.split()]

# first version w/ list

def blink(stones, n):
    after = stones
    for _ in range(n):
        before = after
        after = []
        for stone in before:
            # rule 1
            if stone == 0:
                after.append(1)
                continue
            # rule 2
            n_digits = len(str(stone))
            if n_digits % 2 == 0:
                stone = str(stone)
                left, right = int(stone[:n_digits // 2]), int(stone[n_digits // 2:])
                after.append(left)
                after.append(right)
                continue
            # rule 3
            after.append(int(stone) * 2024)
    return after

# print(len(blink(stones, 25)))    # part 1
# print(len(blink(stones, 75)))    # part 2 is too slow and memory consuming

# optimized version w/ collections.Counter

import collections

def blink(stones, n):
    after = collections.Counter(stones)
    for _ in range(n):
        before = after
        after = collections.Counter()
        for stone, count in before.items():
            # rule 1
            if stone == 0:
                after[1] += count
                continue
            # rule 2
            n_digits = len(str(stone))
            if n_digits % 2 == 0:
                stone_str = str(stone)
                left = int(stone_str[:n_digits // 2])
                right = int(stone_str[n_digits // 2:])
                after[left] += count
                after[right] += count
                continue
            # rule 3
            after[stone * 2024] += count
    return after

print(sum(blink(stones, 25).values()))  # part 1
print(sum(blink(stones, 75).values()))  # part 2
