s = open("input.txt").read()

# part 1: total distance

left = []
right = []

for ln in s.splitlines():
    a, b = ln.split()
    left.append(int(a))
    right.append(int(b))

left.sort()
right.sort()

r1 = 0
for a, b in zip(left, right):
    r1 += abs(a - b)

print(f"{r1=}")
# 1320851

# part 2: similarity score

r2 = 0
for i in left:
    r2 += i * right.count(i)

print(f"{r2=}")
# 26859182
