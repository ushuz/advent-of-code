from collections import deque

def groupwise(iterable, n):
    accum = deque((), n)
    for element in iterable:
        accum.append(element)
        if len(accum) == n:
            yield tuple(accum)

s = open("input.txt").read()
n = 2000

# s = "123"
# n = 10

buyers = [int(ln) for ln in s.strip().splitlines()]

def mix(a, b):
    return a ^ b

def prune(a):
    return a % 16777216

def calculate(secret, n):
    if n == 0: return secret
    secret = prune(mix(secret, secret * 64))
    secret = prune(mix(secret, secret // 32))
    secret = prune(mix(secret, secret * 2048))
    return calculate(secret, n - 1)

r1 = sum(calculate(buyer, n) for buyer in buyers)
print(r1)

def calculate2(secrets, prices: list, changes: list, n):
    secret = secrets[-1]
    prices.append(secret % 10)
    if len(prices) > 1: changes.append(prices[-1] - prices[-2])
    if n == 0: return secrets, prices, changes
    secret = prune(mix(secret, secret * 64))
    secret = prune(mix(secret, secret // 32))
    secret = prune(mix(secret, secret * 2048))
    return calculate2(secrets + [secret], prices, changes, n - 1)

buyer_secrets = []
buyer_prices = []
buyer_changes = []

seqlen = 4
unique_seqs = set()
# list of mappings of change sequence to price
# [{ (c1,c2,c3,c4): price }, ...]
mappings = []

for buyer in buyers:
    secrets, prices, changes = calculate2([buyer], [], [None], n)
    buyer_secrets.append(secrets)
    buyer_prices.append(prices)
    buyer_changes.append(changes)
    m = dict()
    for idx, group in enumerate(groupwise(changes, seqlen)):
        if group[0] is None: continue
        if group in m: continue
        unique_seqs.add(group)
        m[group] = prices[seqlen - 1 + idx]
    mappings.append(m)

best = 0
best_seq = None
for seq in unique_seqs:
    revenue = sum(m.get(seq, 0) for m in mappings)
    if revenue > best:
        best = revenue
        best_seq = seq

print(best, best_seq)
