from collections import defaultdict

s = open("input.txt").read()
max_xy = 70
fallen_bytes = 1024

# s = """5,4\n4,2\n4,5\n3,0\n2,1\n6,3\n2,4\n1,5\n0,6\n3,3\n2,6\n5,1\n1,2\n5,5\n2,5\n6,5\n1,4\n0,4\n6,4\n1,1\n6,1\n1,0\n0,5\n1,6\n2,0"""
# max_xy = 6
# fallen_bytes = 12

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

bytes = [tuple(map(int, ln.split(","))) for ln in s.strip().splitlines()]

def dijkstra(corrupted):
    best = 1e9

    distances = defaultdict(lambda: 1e9)

    # (distance, y, x) starting from (0, 0)
    q = [(0, 0, 0)]

    while q:
        q.sort(key=lambda e: e[0])
        distance, y, x = q.pop(0)

        # if current distance is greater than the known distance, skip
        if distances[(y, x)] < distance: continue

        # otherwise, update the known distance
        distances[(y, x)] = distance

        # if we reached the end, update the best distance
        if (y, x) == (max_xy, max_xy) and distance <= best:
            best = distance

        # traverse all directions
        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            if 0 <= ny <= max_xy and 0 <= nx <= max_xy and (ny, nx) not in corrupted:
                if distance + 1 >= distances[(ny, nx)]: continue
                distances[(ny, nx)] = distance + 1
                q.append((distance + 1, ny, nx))

    return best

r1 = dijkstra(bytes[:fallen_bytes])
print(r1)

# note: too slow to exhaustively search for the next byte

# for n in range(fallen_bytes, len(bytes)):
#     steps = dijkstra(bytes[:n])
#     if steps < 1e9:
#         print(f"{n=} {steps=}")
#         continue
#     break
# print(bytes[n])

# note: to speed things up, we can bisect the search space

start, end = fallen_bytes + 1, len(bytes)
while start < end:
    mid = (start + end) // 2
    steps = dijkstra(bytes[:mid])
    # print(f"{mid=} {steps=}")
    if steps < 1e9:
        start = mid + 1
    else:
        end = mid

print(",".join(map(str, bytes[mid])))
