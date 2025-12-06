s = open("input.txt").read()

# s = "\n".join([
#     "123 328  51 64 ",
#     " 45 64  387 23 ",
#     "  6 98  215 314",
#     "*   +   *   +  ",
# ])

def part1():
    grid = [[cell.strip() for cell in row.split()] for row in s.strip().splitlines()]
    rows = len(grid)
    cols = len(grid[0])

    results = []
    for x in range(cols):
        inputs = []
        for y in range(rows - 1):
            inputs.append(int(grid[y][x]))
        operator = grid[-1][x]
        if operator == "+":
            result = sum(inputs)
        if operator == "*":
            result = 1
            for i in inputs:
                result *= i
        results.append(result)
    return sum(results)

def part2():
    lines = s.splitlines()
    operators = lines[-1]

    results = []
    inputs = []
    operator = None

    def calculate():
        if not inputs: return
        if operator == "+":
            results.append(sum(inputs))
        if operator == "*":
            result = 1
            for i in inputs:
                result *= i
            results.append(result)

    for x, next_operator in enumerate(operators):
        # when we encounter the next operator:
        # - calculate the inputs based on the previous operator
        # - save the new operator for next calculation
        # - reset inputs
        if next_operator in "+*":
            calculate()
            operator = next_operator
            inputs = []
        # read the column top-to-bottom as input
        input_ = ""
        for y in range(len(lines) - 1):
            input_ += lines[y][x]
        # convert to int if not empty
        input_ = input_.strip()
        if input_: inputs.append(int(input_))

    # calculate the last operator
    calculate()

    return sum(results)

print(part1())
print(part2())
