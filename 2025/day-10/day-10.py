s = open("input.txt").read()

# s = """
# [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
# [...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
# [.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
# """

# s = """
# [.#...#] (2,4) (3,4) (0,2,3,5) (0,1,2,3) (1,3,4,5) {26,32,28,47,23,20}
# [#.####.] (0,1,2,4,6) (1,2,4,6) (0,6) (2,3) (0,2,3,4,5,6) (0,2,3,4,5) (3,4,5,6) (2,4) (0,1,2,5,6) {58,41,286,233,79,43,63}
# [.#..] (1) (1,2) (0,1,3) (2,3) (0,2,3) {32,29,35,51}
# [...###] (1,2,4) (2,4,5) (4,5) (0,5) (0,1,2,3,4) (0,1,5) (0,3) (3,5) {55,40,39,33,42,56}
# [###.] (1,2,3) (0,1,2) {0,4,4,4}
# [###..] (0,1) (0,1,3) (4) (0,2,3) (2,4) (2,3) (3,4) {197,32,188,210,37}
# [#..##..] (1,2,3,5,6) (0,1,2,3,5,6) (2,5) (1,2,6) (2,3,4,5) {14,43,68,43,11,57,43}
# [##.#] (0,2,3) (1,2,3) (0,2) (0,3) {21,14,32,24}
# """

def part1():
    minimums = []
    for lineno, line in enumerate(s.strip().splitlines()):
        desired, *buttons_, _ = line.split()

        # convert desired state to binary int
        desired = desired[1:-1].replace(".", "0").replace("#", "1") # to str
        n = len(desired)
        desired = int(desired, 2)                                   # to int

        # convert each button to binary int for xor operation
        buttons: list[int] = []
        for button in buttons_:
            binary = list("0" * n)
            for p in button[1:-1].split(","):
                binary[int(p)] = "1"
            binary = int("".join(binary), 2)
            buttons.append(binary)

        # initialize
        initial = int("0" * n, 2)
        minimum = n * 2

        def search(presses: int, current: int):
            nonlocal minimum
            # limit the maximum attempts to avoid infinite recursion
            if presses >= minimum:
                return presses
            # record minimum presses when desired state is reached
            if current == desired:
                print(f"{lineno=} {desired=:0{n}b} {presses=} {minimum=}")
                minimum = min(minimum, presses)
                return minimum
            # try pressing each button
            return min(search(presses + 1, current ^ button) for button in buttons)

        minimum = search(presses=0, current=initial)
        minimums.append(minimum)

    return sum(minimums)

def part2():
    minimums = []

    for lineno, line in enumerate(s.strip().splitlines()):
        _, *buttons_, desired = line.split()

        # convert desired state to tuple
        desired = tuple(int(x) for x in desired[1:-1].split(","))
        n = len(desired)

        buttons = [tuple(map(int, button[1:-1].split(","))) for button in buttons_]
        nb = len(buttons)

        # represents linear equations in a matrix
        # [ [ co1, co2, ..., con, expected ], ... ]
        matrix = []
        for i in range(n):
            r = desired[i]
            k = []
            for button in buttons:
                k.append(int(i in button))
            k.append(r)
            matrix.append(k)

        # solve linear equations using z3 optimizer
        import z3
        opt = z3.Optimize()
        # declare int variables for each button press count
        pvs = [z3.Int(f"p{i}") for i in range(nb)]
        # each button press count is non-negative
        for pv in pvs: opt.add(pv >= 0)
        # add each linear equation to the optimizer
        for eq in matrix:
            equation = [co * pv for co, pv in zip(eq[:-1], pvs)]
            expected = eq[-1]
            opt.add(sum(equation) == expected)
        # optmize for minimum total button presses
        opt.minimize(sum(pvs))
        # solve
        opt.check()

        m = opt.model()
        ps = [m[pv].as_long() for pv in pvs]
        minimum = sum(ps)
        print(f"{lineno=} {desired=} {ps=} {minimum=}")

        minimums.append(minimum)

    return sum(minimums)

print(part1())
print(part2())
