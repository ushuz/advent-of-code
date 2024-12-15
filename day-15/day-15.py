s = open("input.txt").read()

# s = """
# ########
# #..O.O.#
# ##@.O..#
# #...O..#
# #.#.O..#
# #...O..#
# #......#
# ########

# <^^>>>vv<v>>v<<"""

# s = """
# #######
# #...#.#
# #.....#
# #..OO@#
# #..O..#
# #.....#
# #######

# <vv<<^^<<^^"""

# s = """
# ##########
# #..O..O.O#
# #......O.#
# #.OO..O.O#
# #..O@..O.#
# #O#..O...#
# #O..O..O.#
# #.OO.O.OO#
# #....O...#
# ##########

# <vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
# vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
# ><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
# <<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
# ^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
# ^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
# >^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
# <><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
# ^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
# v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""

def render(movement, warehouse, inspect: bool = False):
    if not inspect: return
    print(f"{movement=}")
    print("\n".join("".join(row) for row in warehouse))
    input("Next? ")

def calculate_coordinates(warehouse):
    ret = 0
    for y, row in enumerate(warehouse):
        for x, ch in enumerate(row):
            if ch in "O[": ret += 100 * y + x
    return ret

# (y, x)
directions = {
    "^": (-1, 0),
    "v": (1, 0),
    "<": (0, -1),
    ">": (0, 1),
}

warehouse, movements = s.strip().split("\n\n")
movements = movements.replace("\n", "")

def predict(warehouse, inspect=False):
    # (y, x)
    robot = None

    for y, row in enumerate(warehouse):
        for x, ch in enumerate(row):
            if ch != "@": continue
            robot = (y, x)

    render(movement="initial", warehouse=warehouse, inspect=inspect)

    for movement in movements:
        dy, dx = directions[movement]
        def move(y, x):
            ny, nx = y + dy, x + dx
            # hit a box: O
            if warehouse[ny][nx] in "O":
                # track all boxes
                boxes = [(ny, nx, warehouse[ny][nx])]
                # see if box can move
                ny2, nx2 = ny + dy, nx + dx
                # hit another box, keep looking for empty space
                while warehouse[ny2][nx2] in "O":
                    boxes.append((ny2, nx2, warehouse[ny2][nx2]))
                    ny2, nx2 = ny2 + dy, nx2 + dx
                # hit wall, stay in place
                if warehouse[ny2][nx2] == "#": return y, x
                # hit empty space, move all the way
                if warehouse[ny2][nx2] == ".":
                    for by, bx, ch in boxes:
                        warehouse[by+dy][bx+dx] = ch
                    warehouse[ny][nx] = "@"
                    warehouse[y][x] = "."
                    return ny, nx
            # hit a box: []
            def get_box_tuple(y, x):
                return (y, x, y, x+1) if warehouse[y][x] == "[" else (y, x-1, y, x)
            if warehouse[ny][nx] in "[]":
                # track all boxes
                boxes = []
                def can_push_box(box):
                    boxes.append(box)
                    ly, lx, ry, rx = box
                    nly, nlx = ly + dy, lx + dx
                    nry, nrx = ry + dy, rx + dx
                    if movement in "<":
                        if warehouse[nly][nlx] == "#": return False
                        if warehouse[nly][nlx] == ".": return True
                        if warehouse[nly][nlx] in "[]": return can_push_box(get_box_tuple(nly, nlx))
                        raise NotImplementedError()
                    if movement in ">":
                        if warehouse[nry][nrx] == "#": return False
                        if warehouse[nry][nrx] == ".": return True
                        if warehouse[nry][nrx] in "[]": return can_push_box(get_box_tuple(nry, nrx))
                        raise NotImplementedError()
                    if movement in "^v":
                        can_push_left = can_push_right = False
                        if warehouse[nly][nlx] == "#": can_push_left = False
                        if warehouse[nly][nlx] == ".": can_push_left = True
                        if warehouse[nly][nlx] in "[]": can_push_left = can_push_box(get_box_tuple(nly, nlx))
                        if warehouse[nry][nrx] == "#": can_push_right = False
                        if warehouse[nry][nrx] == ".": can_push_right = True
                        if warehouse[nry][nrx] in "[]": can_push_right = can_push_box(get_box_tuple(nry, nrx))
                        return can_push_left and can_push_right
                    raise NotImplementedError()
                # cannot push box, stay in place
                if not can_push_box(get_box_tuple(ny, nx)): return y, x
                # push all boxes in the way
                for ly, lx, ry, rx in boxes:    # !!! IMPORTANT !!! clear all boxes first
                    warehouse[ly][lx] = "."
                    warehouse[ry][rx] = "."
                for ly, lx, ry, rx in boxes:    # !!! IMPORTANT !!! then move all boxes to new position
                    warehouse[ly+dy][lx+dx] = "["
                    warehouse[ry+dy][rx+dx] = "]"
                warehouse[ny][nx] = "@"
                warehouse[y][x] = "."
                return ny, nx
            # hit wall, stay in place
            if warehouse[ny][nx] == "#": return y, x
            # hit empty space, move to it
            if warehouse[ny][nx] == ".":
                warehouse[ny][nx] = "@"
                warehouse[y][x] = "."
                return ny, nx
        robot = move(*robot)
        render(movement=movement, warehouse=warehouse, inspect=inspect)

    return calculate_coordinates(warehouse)

warehouse1 = [list(row) for row in warehouse.splitlines()]
print(predict(warehouse1))

warehouse2 = [list(row) for row in warehouse
                .replace("#", "##")
                .replace("O", "[]")
                .replace(".", "..")
                .replace("@", "@.")
                .splitlines()]
print(predict(warehouse2))
