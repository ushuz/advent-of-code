s = open("input.txt").read()

# s = """
# aaa: you hhh
# you: bbb ccc
# bbb: ddd eee
# ccc: ddd eee fff
# ddd: ggg
# eee: out
# fff: out
# ggg: out
# hhh: ccc fff iii
# iii: out
# """

# s = """
# svr: aaa bbb
# aaa: fft
# fft: ccc
# bbb: tty
# tty: ccc
# ccc: ddd eee
# ddd: hub
# hub: fff
# eee: dac
# dac: fff
# fff: ggg hhh
# ggg: out
# hhh: out
# """

def part1():
    devices = dict()
    for line in s.strip().splitlines():
        name, out = line.split(": ")
        outputs = tuple(out.split())
        devices[name] = outputs

    paths = set()

    def dfs(path: tuple[str]) -> bool:
        cursor = path[-1]
        # reach the end
        if cursor == "out":
            paths.add(path)
            return
        # search deeper
        for out in devices[cursor]:
            if out in path: continue    # avoid cycles
            dfs(path + (out,))

    dfs(("you",))

    return len(paths)

def part2():
    devices = dict(out=[])
    for line in s.strip().splitlines():
        name, out = line.split(": ")
        outputs = tuple(out.split())
        devices[name] = outputs

    import functools
    @functools.cache
    def paths(start, end):
        p = 0
        for out in devices[start]:
            if out == end:
                p += 1
            else:
                p += paths(out, end)
        return p

    result = (
        paths("svr", "fft") * paths("fft", "dac") * paths("dac", "out")
        or paths("svr", "dac") * paths("dac", "fft") * paths("fft", "out")
    )

    return result

print(part1())
print(part2())
