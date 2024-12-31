import re

with open("input") as f:
    data = f.read()

    s = 0
    for match in re.finditer("mul\((\d+),(\d+)\)", data):
        x, y = match.groups()
        s += int(x)*int(y)
    print(s)

    s = 0
    enabled = True
    for match in re.finditer("mul\((\d+),(\d+)\)|do\(\)|don't\(\)", data):
        if match[0] == "do()":
            enabled = True
        elif match[0] == "don't()":
            enabled = False
        elif enabled:
            s += int(match[1])*int(match[2])
    print(s)
