s = open("input.txt").read()

# s = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224," \
#     "1698522-1698528,446443-446449,38593856-38593862,565653-565659," \
#     "824824821-824824827,2121212118-2121212124"

def part1():

    def is_invalid(n):
        s = str(n)
        # odd length won't be invalid
        if len(s) % 2 != 0:
            return False
        # compare left half vs right half
        half = len(s) // 2
        return s[:half] == s[half:]

    sum = 0
    for pair in s.split(","):
        a, b = map(int, pair.split("-"))
        for n in range(a, b + 1):
            if is_invalid(n):
                sum += n
    return sum

def part2():

    def is_invalid(n):
        s = str(n)
        half = len(s) // 2
        for i in range(half):
            left = s[:i+1]
            right = s[i+1:]
            # if empty after replace, right is a repeat of left, i.e. invalid
            if not right.replace(left, ""):
                return True
        return False

    sum = 0
    for pair in s.split(","):
        a, b = map(int, pair.split("-"))
        for n in range(a, b + 1):
            if is_invalid(n):
                sum += n
    return sum

print(part1())
print(part2())
