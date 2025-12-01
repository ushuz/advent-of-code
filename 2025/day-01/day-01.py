s = open("input.txt").read()

# s = """
# L68
# L30
# R48
# L5
# R60
# L55
# L1
# L99
# R14
# L82
# """

def rotate_left(current, distance):
    return (current - distance) % 100

def rotate_right(current, distance):
    return (current + distance) % 100

def part1():
    dial = 50
    password = 0

    for line in s.strip().splitlines():
        direction = line[0]
        distance = int(line[1:])

        match direction:
            case "L":
                dial = rotate_left(dial, distance)
            case "R":
                dial = rotate_right(dial, distance)

        password += dial == 0

    print(password)

def part2():
    dial = 50
    password = 0

    for line in s.strip().splitlines():
        direction = line[0]
        distance = int(line[1:])

        password += distance // 100
        distance = distance % 100

        match direction:
            case "L":
                password += (dial - distance <= 0) and (dial != 0)
                dial = rotate_left(dial, distance)
            case "R":
                password += (dial + distance >= 100)
                dial = rotate_right(dial, distance)

    print(password)

part1()
part2()
