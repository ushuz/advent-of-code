s = open("input.txt").read()

# part 1

r1 = 0

import re

pattern = re.compile(r"mul\(\d{1,3},\d{1,3}\)")

def mul(a, b):
    return a * b

matches = pattern.findall(s)
for m in matches:
    r1 += eval(m)

print(f"{r1=}")

# part 2

r2 = 0

pattern = re.compile(r"mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)")

matches = pattern.findall(s)

evaluate = True
for m in matches:
    if m == "do()":
        evaluate = True
        continue
    if m == "don't()":
        evaluate = False
        continue
    if evaluate:
        r2 += eval(m)

print(f"{r2=}")
