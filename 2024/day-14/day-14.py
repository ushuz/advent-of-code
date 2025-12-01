s = open("input.txt").read().strip()
width = 101
height = 103

# s = """
# p=0,4 v=3,-3
# p=6,3 v=-1,-3
# p=10,3 v=-1,2
# p=2,0 v=2,-1
# p=0,0 v=1,3
# p=3,0 v=-2,-2
# p=7,6 v=-1,-3
# p=3,0 v=-1,-2
# p=9,3 v=2,3
# p=7,3 v=-1,2
# p=2,4 v=2,-3
# p=9,5 v=-3,-3""".strip()
# width = 11
# height = 7

mx = (width - 1) // 2   # middle column\
my = (height - 1) // 2  # middle row

robots = []

for ln in s.splitlines():
    p, v = ln.strip().split()
    x, y = [int(v) for v in p.replace("p=", "").split(",")]
    vx, vy = [int(v) for v in v.replace("v=", "").split(",")]
    robots.append((x, y, vx, vy))

quadrant_top_left = []
quadrant_top_right = []
quadrant_bottom_left = []
quadrant_bottom_right = []

seconds = 100

for x, y, vx, vy in robots:
    nx, ny = x + vx * seconds, y + vy * seconds
    nx, ny = nx % width, ny % height
    if nx < mx and ny < my:
        quadrant_top_left.append((nx, ny))
    if nx > mx and ny < my:
        quadrant_top_right.append((nx, ny))
    if nx < mx and ny > my:
        quadrant_bottom_left.append((nx, ny))
    if nx > mx and ny > my:
        quadrant_bottom_right.append((nx, ny))

r1 = len(quadrant_top_left) * len(quadrant_top_right) * len(quadrant_bottom_left) * len(quadrant_bottom_right)
print(r1)

# part 2: inspired by reddit, I'll render robot positions of every second and do a visual inspection to find the christmas tree...

def visualize(positions):
    for y in range(height):
        for x in range(width):
            if (x, y) in positions:
                print(".", end="")
            else:
                print(" ", end="")
        print()

for seconds in range(8159, 8160):
    positions = set()
    for x, y, vx, vy in robots:
        nx, ny = x + vx * seconds, y + vy * seconds
        nx, ny = nx % width, ny % height
        positions.add((nx, ny))
    print(seconds)
    visualize(positions)
    print("\n" * 20)

# ... and the answer is 8159
