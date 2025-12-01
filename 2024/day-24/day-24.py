s = open("input.txt").read()

initials, connections_ = s.strip().split("\n\n")

wires = dict()
for line in initials.splitlines():
    wire, initial = line.split(": ")
    wires[wire] = int(initial)

GATES = dict(
    AND=lambda a, b: int(a and b),
    OR=lambda a, b: int(a or b),
    XOR=lambda a, b: a ^ b,
)

connections = dict()
for line in connections_.splitlines():
    a, gate, b, _, wire = line.split()
    connections[wire] = GATES[gate], a, b

def run(wires: dict, connections: dict):
    def evalutate(wire):
        if wire not in wires:
            gate, a, b = connections[wire]
            wires[wire] = gate(evalutate(a), evalutate(b))
        return wires[wire]
    z = [evalutate(wire) for wire in sorted(connections, reverse=True) if wire.startswith("z")]
    zbin = "".join(map(str, z))
    zdec = int(zbin, 2)
    return zbin, zdec

zbin, zdec = run(wires.copy(), connections)
print(zbin, zdec)

# part 2

# initial_x = int("".join([str(wires[wire]) for wire in sorted(wires, reverse=True) if wire.startswith("x")]), 2)
# initial_y = int("".join([str(wires[wire]) for wire in sorted(wires, reverse=True) if wire.startswith("y")]), 2)
# z = initial_x + initial_y

# max_swapped = 8

# pairs = list(itertools.combinations(connections, 2))

# counter = 0

# def swap(connections: dict, swapped: set, memo: dict):
#     state = frozenset(swapped)
#     if state in memo: return memo[state]
#     if len(swapped) == max_swapped:
#         try:
#             _, zdec = run(wires.copy(), connections)
#             ret = swapped if zdec == z else False
#             memo[state] = ret
#             global counter
#             counter += 1
#             if counter % 100: print(swapped, z, zdec)
#             return ret
#         except Exception: pass
#         memo[state] = False
#         return False
#     for a, b in pairs:
#         if a in swapped or b in swapped: continue
#         swapped.add(a)
#         swapped.add(b)
#         connections[a], connections[b] = connections[b], connections[a]
#         ret = swap(connections, swapped, memo)
#         if ret: return ret
#         swapped.remove(a)
#         swapped.remove(b)
#         connections[a], connections[b] = connections[b], connections[a]
#     memo[state] = False
#     return False

# swap(connections.copy(), set(), dict())

# note: the search space is 10^16 magnitude, it won't work

# note: instead, part 2 requires knowledge of the full adder circuit:
#   X1 XOR Y1 => M1
#   X1 AND Y1 => N1
#   C0 AND M1 => R1
#   C0 XOR M1 -> Z1
#   R1 OR N1 -> C1
# ref:
#   https://www.reddit.com/r/adventofcode/comments/1hl698z/comment/m3k5k0n/
#   https://en.wikipedia.org/wiki/Adder_(electronics)#Full_adder

def find(a, b, gate) -> str | None:
    for ln in connections_.splitlines():
        if ln.startswith(f"{a} {gate} {b}") or ln.startswith(f"{b} {gate} {a}"):
            return ln.split()[-1]

swapped = set()

nbits = len(initials) // 2

c0 = None
for i in range(nbits):
    i = f"{i:02d}"
    r1 = z1 = c1 = None

    m1 = find(f"x{i}", f"y{i}", "XOR")
    n1 = find(f"x{i}", f"y{i}", "AND")

    if c0:
        r1 = find(c0, m1, "AND")
        if not r1:
            m1, n1 = n1, m1
            swapped.add(m1)
            swapped.add(n1)
            r1 = find(c0, m1, "AND")

        z1 = find(c0, m1, "XOR")

        if m1 and m1.startswith("z"):
            m1, z1 = z1, m1
            swapped.add(m1)
            swapped.add(z1)

        # n1 should be an internal carry signal, if it starts with z, it's likely miswired
        if n1 and n1.startswith("z"):
            n1, z1 = z1, n1
            swapped.add(n1)
            swapped.add(z1)

        # r1 should never be an output signal, if it starts with z, it's likely miswired
        if r1 and r1.startswith("z"):
            r1, z1 = z1, r1
            swapped.add(r1)
            swapped.add(z1)

        # once r1 and n1 can be assumed to be correct, find c1
        c1 = find(r1, n1, "OR")

    # c1 should be an internal carry signal, if it starts with z, it's likely miswired
    # except the final one, which can be an output signal
    if c1 and c1.startswith("z") and c1 != f"z{nbits}":
        c1, z1 = z1, c1
        swapped.add(c1)
        swapped.add(z1)

    # carry signal to the next bit
    #   c1: carry from previous bit
    #   n1: initial carry (AND of inputs) for first bit
    c0 = c1 if c0 else n1

print(swapped)
