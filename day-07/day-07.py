s = open("input.txt").read()

import itertools

def evaluate(numbers, operators):
    result = numbers[0]
    for i, op in enumerate(operators):
        if op == '+':
            result += numbers[i + 1]
        if op == '*':
            result *= numbers[i + 1]
        if op == '||':
            result = int(f"{result}{numbers[i + 1]}")
    return result

def can_make_value(target, numbers, operators):
    # generate all possible operator combinations with itertools.product()
    for ops in itertools.product(operators, repeat=len(numbers)-1):
        if evaluate(numbers, ops) == target:
            return True
    return False

# part 1

r1 = 0

for ln in s.splitlines():
    value, numbers = ln.split(':')
    value = int(value)
    numbers = [int(x) for x in numbers.strip().split()]
    if can_make_value(value, numbers, operators=['+', '*']):
        r1 += value

print(f"{r1=}")

# part 2

r2 = 0

for ln in s.splitlines():
    value, numbers = ln.split(':')
    value = int(value)
    numbers = [int(x) for x in numbers.strip().split()]
    if can_make_value(value, numbers, operators=['||', '+', '*']):
        r2 += value

print(f"{r2=}")
