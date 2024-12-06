s = open("input.txt").read()
grid = [list(line) for line in s.strip().splitlines()]

# part 1

def find_guard(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] in '^>v<':
                return (x, y, grid[y][x])
    return None

def get_next_position(x, y, direction):
    if direction == '^':
        return (x, y-1)
    elif direction == '>':
        return (x+1, y)
    elif direction == 'v':
        return (x, y+1)
    elif direction == '<':
        return (x-1, y)

def turn_right(direction):
    return {'^': '>', '>': 'v', 'v': '<', '<': '^'}[direction]

def has_left(x, y, grid):
    return (0 <= y < len(grid) and
            0 <= x < len(grid[0]))

def count_visited_positions():
    x, y, direction = find_guard(grid)
    visited = {(x, y)}

    while True:
        # check position in front
        next_x, next_y = get_next_position(x, y, direction)

        # check if guard would leave the map
        if not has_left(next_x, next_y, grid):
            break

        # check if obstacle ahead
        if grid[next_y][next_x] == '#':
            direction = turn_right(direction)
        else:
            x, y = next_x, next_y
            visited.add((x, y))

    return len(visited)

r1 = count_visited_positions()
print(f"{r1=}")

# part 2

def is_loop(grid):
    x, y, direction = find_guard(grid)
    visited_states = {(x, y, direction)}
    visited_positions = {(x, y)}

    steps = 0
    max_steps = len(grid) * len(grid[0]) * 4  # reasonable maximum before assuming no loop

    while steps < max_steps:
        next_x, next_y = get_next_position(x, y, direction)

        if not has_left(next_x, next_y, grid):
            return False  # guard leaves the map

        if grid[next_y][next_x] == '#':
            direction = turn_right(direction)
        else:
            x, y = next_x, next_y
            visited_positions.add((x, y))

        state = (x, y, direction)
        if state in visited_states:
            return True  # found a loop

        visited_states.add(state)
        steps += 1

    return False  # no loop found within max steps

def count_loop_positions():
    count = 0

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            # skip if position is occupied or is guard's start
            if grid[y][x] != '.':
                continue
            # try placing obstacle here
            grid[y][x] = '#'
            if is_loop(grid):
                count += 1
            grid[y][x] = '.'  # reset

    return count

r2 = count_loop_positions()
print(f"{r2=}")
