from collections import defaultdict

s = open("input.txt").read()

# s = """kh-tc\nqp-kh\nde-cg\nka-co\nyn-aq\nqp-ub\ncg-tb\nvc-aq\ntb-ka\nwh-tc\nyn-cg\nkh-ub\nta-co\nde-co\ntc-td\ntb-wq\nwh-td\nta-ka\ntd-qp\naq-cg\nwq-ub\nub-vc\nde-ta\nwq-aq\nwq-vc\nwh-yn\nka-de\nkh-ta\nco-tc\nwh-qp\ntb-vc\ntd-yn"""

graph = defaultdict(set)
for ln in s.strip().splitlines():
    a, b = ln.split("-")
    graph[a].add(b)
    graph[b].add(a)

def search1(computer: str, connected: list, n: int, interconnected: set):
    if len(connected) > n: return
    for c in graph[computer]:
        if len(connected) == n and c == connected[0]:
            interconnected.add(tuple(sorted(connected)))
            break
        if c in connected: continue
        search1(computer=c, connected=connected + [c], n=n, interconnected=interconnected)

interconnected = set()

candidates = [k for k in graph if k.startswith("t")]

for candidate in candidates:
    search1(computer=candidate, connected=[candidate], n=3, interconnected=interconnected)

# print("\n".join(",".join(party) for party in sorted(interconnected)))
print(len(interconnected))

# part 2

largest = set()

def connect(connected: set):
    global largest
    for next in graph:
        if not all(next in graph[known] for known in connected): continue
        connected.add(next)
        if len(connected) > len(largest):
            largest = set(connected)
        connect(connected)

for computer in graph:
    connect(set([computer]))

print(",".join(sorted(largest)))
