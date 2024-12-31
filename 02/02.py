def safe(levels):
    if all(1 <= abs(a - b) <= 3 for a, b in zip(levels, levels[1:])):
        return levels == sorted(levels) or levels == sorted(levels, reverse=True)
    return False

with open("input") as file:
    records = [[int(lvl) for lvl in record.split()] for record in file.read().strip().split("\n")]

    print(sum(1 for r in records if safe(r)))

    print(sum(1 for r in records if any(safe(r[:i]+r[i+1:]) for i in range(len(r) + 1))))
