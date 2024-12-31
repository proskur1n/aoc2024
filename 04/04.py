def word(x, y, dx, dy, size):
    if x < 0 or x >= len(lines[0]) or y < 0 or y >= len(lines):
        return ""
    if size == 0:
        return ""
    return lines[y][x] + word(x+dx, y+dy, dx, dy, size-1)

with open("input") as f:
    lines = f.read().strip().split()

    count = 0
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            if lines[y][x] != "X":
                continue
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    count += word(x, y, dx, dy, 4) == "XMAS"
    print(count)

    count = 0
    for y in range(1, len(lines)-1):
        for x in range(1, len(lines[0])-1):
            if lines[y][x] != "A":
                continue
            if word(x-1, y-1, 1, 1, 3) in ("MAS", "SAM") and word(x+1, y-1, -1, 1, 3) in ("MAS", "SAM"):
                count += 1
    print(count)
