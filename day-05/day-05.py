s = open("input.txt").read()
s1, s2 = s.split("\n\n")

# part 1

import collections
rules = collections.defaultdict(list)

for ln in s1.splitlines():
    k, v = [int(x) for x in ln.strip().split("|")]
    rules[k].append(v)

r1 = 0

incorrect_updates = []

def is_correct(update):
    for idx, x in enumerate(update[:-1]):
        rule = rules[x]
        left = update[:idx]
        if set(left) & set(rule):
            return False
        right = update[idx+1:]
        if not (set(right) & set(rule)):
            return False
    return True

for ln in s2.splitlines():
    update = [int(x) for x in ln.split(",")]
    if not is_correct(update):
        incorrect_updates.append(update)
        continue
    mid = update[len(update)//2]
    r1 += mid

print(f"{r1=}")

# part 2

r2 = 0

def reorder(update):
    final = [-1] * len(update)
    for x in update:
        rule = rules[x]
        after = set(update) & set(rule)
        final[-len(after)-1] = x
    return final

for update in incorrect_updates:
    reordered = reorder(update)
    mid = reordered[len(reordered)//2]
    r2 += mid

print(f"{r2=}")
