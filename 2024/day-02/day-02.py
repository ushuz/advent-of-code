s = open("input.txt").read()

import functools
import sys

# part 1: How many reports are safe?

n1 = 0

unsafe = []

def is_safe_report(report):
    if report != sorted(report) and report != sorted(report, reverse=True):
        return False
    r = functools.reduce(lambda a, b: b if 1 <= abs(a - b) <= 3 else sys.maxsize, report)
    if r == sys.maxsize:
        return False
    return True

for ln in s.splitlines():
    report = ln.split()
    report = [int(x) for x in report]
    if is_safe_report(report):
        n1 += 1
    else:
        unsafe.append(report)

print(f"{n1=}")

# part 2: How many reports are now safe?

n2 = n1

for report in unsafe:
    for i in range(len(report)):
        rd = report[:]
        rd.pop(i)
        if is_safe_report(rd):
            n2 += 1
            print(rd)
            break

print(f"{n2=}")
