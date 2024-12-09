s = open("input.txt").read().strip()

# s = "2333133121414131402"


disk: list[str] = []
file_blocks: list[int, int] = []
free_blocks = []

# decode

id = 0
for ch in s:
    if id % 2 == 0:
        disk += [str(id // 2)] * int(ch)
        file_blocks.append((id // 2, int(ch)))
    else:
        disk += ["."] * int(ch)
        free_blocks.append(dict(size=int(ch), moved=[]))
    id += 1

disksize = len(disk)

# part 1

checksum1 = 0

rc = disksize - 1

def move():
    global rc
    while rc > 0:
        if disk[rc] != ".": yield int(disk[rc])
        rc -= 1

fileblock = move()

for c, b in enumerate(disk):
    if c == rc:
        break
    if b == ".":
        fileid = next(fileblock)
    else:
        fileid = int(b)

    checksum1 += fileid * c

print(checksum1)

# part 2

cursor = len(file_blocks) - 1

while cursor >= 0:
    file_id, file_size = file_blocks[cursor]
    # find a free block to the left of the file
    for free_block in free_blocks[:cursor]:
        if file_size <= free_block["size"]:
            free_block["size"] -= file_size
            free_block["moved"].append((file_id, file_size))
            file_blocks[cursor] = '.', file_size
            break
    cursor -= 1

moved: list[str] = []

for idx, file_block in enumerate(file_blocks):
    file_id, file_size = file_block
    moved += [str(file_id)] * file_size
    if idx < len(free_blocks):
        free_block = free_blocks[idx]
        for file_id, file_size in free_block["moved"]:
            moved += [str(file_id)] * file_size
        moved += ["."] * free_block["size"]

checksum2 = 0

for c, b in enumerate(moved):
    if b == ".": continue
    checksum2 += int(b) * c

print(checksum2)
