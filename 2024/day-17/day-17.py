s = open("input.txt").read()

# s = """Register A: 729
# Register B: 0
# Register C: 0

# Program: 0,1,5,4,3,0"""

registers, program = s.strip().split("\n\n")
a, b, c = [int(ln.split(": ")[1]) for ln in registers.split("\n")]
program = [int(v) for v in program.replace("Program: ", "").split(",")]

def run(ra, rb, rc):
    registers = dict(a=ra, b=rb, c=rc)
    pointer = 0
    out = []

    combo = [
        lambda: 0,  # combo 0
        lambda: 1,  # combo 1
        lambda: 2,  # combo 2
        lambda: 3,  # combo 3
        lambda: registers["a"], # combo 4: register a
        lambda: registers["b"], # combo 5: register b
        lambda: registers["c"], # combo 6: register c
        # combo 7 is reserved
    ]

    def instruction_adv(operand):
        registers["a"] = registers["a"] // 2 ** combo[operand]()

    def instruction_bxl(operand):
        registers["b"] = registers["b"] ^ operand

    def instruction_bst(operand):
        registers["b"] = combo[operand]() % 8

    def instruction_jnz(operand):
        if registers["a"] == 0: return
        return operand

    def instruction_bxc(operand):
        registers["b"] = registers["b"] ^ registers["c"]

    def instruction_out(operand):
        out.append(combo[operand]() % 8)

    def instruction_bdv(operand):
        registers["b"] = registers["a"] // 2 ** combo[operand]()

    def instruction_cdv(operand):
        registers["c"] = registers["a"] // 2 ** combo[operand]()

    ops = [
        instruction_adv,    # opcode 0
        instruction_bxl,    # opcode 1
        instruction_bst,    # opcode 2
        instruction_jnz,    # opcode 3
        instruction_bxc,    # opcode 4
        instruction_out,    # opcode 5
        instruction_bdv,    # opcode 6
        instruction_cdv,    # opcode 7
    ]

    while pointer < len(program):
        opcode = program[pointer]
        operand = program[pointer + 1]
        # print(f"{pointer} {opcode=} {operand=} {registers["a"]=} {registers["b"]=} {registers["c"]=} {out=}")
        pointer = (pointer + 2) if ops[opcode](operand) is None else operand
        # print(f"{pointer} {opcode=} {operand=} {registers["a"]=} {registers["b"]=} {registers["c"]=} {out=}")

    return out

# part 1

out = run(a, b, c)
print(",".join(map(str, out)))

# part 2

valid = [0]

for l in range(1, len(program)+1):
    old = valid
    valid = []
    for v in old:
        for offset in range(8):
            n = 8 * v + offset
            if run(n, 0, 0) == program[-l:]:
                valid.append(n)

print(min(valid))
