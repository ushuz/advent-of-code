s = open("input.txt").read()

import collections
import itertools

antennas = collections.defaultdict(list)

for y, ln in enumerate(s.strip().splitlines()):
    for x, ch in enumerate(ln):
        if ch == ".": continue
        antennas[ch].append((x, y))

max_y = y
max_x = len(ln) - 1

# part 1

antinodes1 = set()

for freq, coords in antennas.items():
    for (x1, y1), (x2, y2) in itertools.combinations(coords, 2):
        # antinode 1
        a1y, a1x = y1 + (y1 - y2), x1 + (x1 - x2)
        if 0 <= a1y <= max_y and 0 <= a1x <= max_x:
            antinodes1.add((a1x, a1y))
        # antinode 2
        a2y, a2x = y2 + (y2 - y1), x2 + (x2 - x1)
        if 0 <= a2y <= max_y and 0 <= a2x <= max_x:
            antinodes1.add((a2x, a2y))

print(len(antinodes1))

# part 2

antinodes2 = set()

for freq, coords in antennas.items():
    for (x1, y1), (x2, y2) in itertools.combinations(coords, 2):
        antinodes2.add((x1, y1))
        antinodes2.add((x2, y2))
        for m, n in [
            (2, -1),    # antinode 1 direction
            (-1, 2),    # antinode 2 direction
        ]:
            msigned1 = m // abs(m)
            nsigned1 = n // abs(n)
            while True:
                ax, ay = m * x1 + n * x2, m * y1 + n * y2
                if not (0 <= ax <= max_x and 0 <= ay <= max_y): break
                antinodes2.add((ax, ay))
                m += msigned1
                n += nsigned1

print(len(antinodes2))
