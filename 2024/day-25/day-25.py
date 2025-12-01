s = open("input.txt").read()

locks = set()
keys = set()

npins = 5

for schematic in s.strip().split("\n\n"):
    top, *schematic, bottom = schematic.splitlines()
    heights = [0] * npins
    for ln in schematic:
        for idx, ch in enumerate(ln):
            heights[idx] += ch == "#"
    if top == "#" * npins and bottom == "." * npins:
        keys.add(tuple(heights))
    elif top == "." * npins and bottom == "#" * npins:
        locks.add(tuple(heights))
    else:
        raise NotImplementedError

r1 = 0

for lock in locks:
    for key in keys:
        r1 += all(k + l <= npins for k, l in zip(key, lock))

print(r1)
