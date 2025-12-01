s = open("input.txt").read()

grid = [ln.strip() for ln in s.splitlines()]

# part 1

def check_pattern1(pattern, grid, row, col, dx, dy):
    offset = len(pattern) - 1
    if not (0 <= row + offset*dx < len(grid) and 0 <= col + offset*dy < len(grid[0])):
        return False
    for i in range(len(pattern)):
        if grid[row + i*dx][col + i*dy] != pattern[i]:
            return False
    return True

def count_xmas(grid):
    count = 0

    pattern = "XMAS"
    # all 8 directions: horizontal, vertical, and diagonal
    directions = [
        (0,1),  (1,0),  (1,1),   (1,-1),     # right, down, diagonal down-right, diagonal down-left
        (0,-1), (-1,0), (-1,-1), (-1,1),     # left, up, diagonal up-left, diagonal up-right
    ]

    rows, cols = len(grid), len(grid[0])
    for row in range(rows):
        for col in range(cols):
            for dx, dy in directions:
                if check_pattern1(pattern, grid, row, col, dx, dy):
                    count += 1

    return count

r1 = count_xmas(grid)

print(f"{r1}")

# part 2

def count_x_max(grid):
    count = 0
    patterns = ["SAM", "MAS"]

    rows, cols = len(grid), len(grid[0])
    for row in range(1, rows):
        for col in range(1, cols):
            if grid[row][col] != "A": continue
            try:
                # check diagonal up-left to down-right
                up_left = grid[row-1][col-1]
                down_right = grid[row+1][col+1]
                d1 = f"{up_left}A{down_right}"
                # check diagonal up-right to down-left
                up_right = grid[row-1][col+1]
                down_left = grid[row+1][col-1]
                d2 = f"{up_right}A{down_left}"
            except IndexError:
                continue
            # check if both diagonals are valid patterns
            if d1 in patterns and d2 in patterns:
                count += 1

    return count

r2 = count_x_max(grid)

print(f"{r2}")
