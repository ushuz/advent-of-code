s = open("input.txt").read().strip()

# s = """
# Button A: X+94, Y+34
# Button B: X+22, Y+67
# Prize: X=8400, Y=5400

# Button A: X+26, Y+66
# Button B: X+67, Y+21
# Prize: X=12748, Y=12176

# Button A: X+17, Y+86
# Button B: X+84, Y+37
# Prize: X=7870, Y=6450

# Button A: X+69, Y+23
# Button B: X+27, Y+71
# Prize: X=18641, Y=10279""".strip()

# s = """
# Button A: X+88, Y+40
# Button B: X+19, Y+86
# Prize: X=1843, Y=1534""".strip()

machines = s.split("\n\n")

token_a = 3
token_b = 1

# part 1: brute force

r1 = 0

for machine in machines:
    button_a, button_b, prize = machine.strip().splitlines()
    ax, ay = [int(v) for v in button_a.split(": ")[1].replace("X+", "").replace("Y+", "").split(",")]
    bx, by = [int(v) for v in button_b.split(": ")[1].replace("X+", "").replace("Y+", "").split(",")]
    px, py = [int(v) for v in prize.split(": ")[1].replace("X=", "").replace("Y=", "").split(",")]

    min_token = 999999
    for press_a in range(101):
        for press_b in range(101):
            if ax * press_a + bx * press_b == px and ay * press_a + by * press_b == py:
                min_token = min(min_token, press_a * token_a + press_b * token_b)

    if min_token < 999999:
        r1 += min_token

print(r1)

# part 2: liner equation

r2 = 0

for machine in machines:
    button_a, button_b, prize = machine.strip().splitlines()
    ax, ay = [int(v) for v in button_a.split(": ")[1].replace("X+", "").replace("Y+", "").split(",")]
    bx, by = [int(v) for v in button_b.split(": ")[1].replace("X+", "").replace("Y+", "").split(",")]
    px, py = [int(v) + 10000000000000 for v in prize.split(": ")[1].replace("X=", "").replace("Y=", "").split(",")]

    # ax * a + bx * b = px
    # ay * a + by * b = py

    # => a + bx / ax * b = px / ax
    #    a + by / ay * b = py / ay
    # => (bx / ax - by / ay) * b = px / ax - py / ay
    # => b = (px / ax - py / ay) / (bx / ax - by / ay)

    b = (px / ax - py / ay) / (bx / ax - by / ay)

    # => ax / bx * a + b = px / bx
    #    ay / by * a + b = py / by
    # => (ax / bx - ay / by) * a = px / bx - py / by
    # => a = (px / bx - py / by) / (ax / bx - ay / by

    a = (px / bx - py / by) / (ax / bx - ay / by)

    a, b = round(a), round(b)

    if (px == ax * a + bx * b) and (py == ay * a + by * b):
        r2 += a * token_a + b * token_b

print(r2)
