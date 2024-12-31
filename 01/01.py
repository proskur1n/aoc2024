with open("input") as file:
    lines = file.read().strip().split("\n")
    # Zip is its own inverse!
    # https://stackoverflow.com/a/19343
    lists = list(zip(*(line.split() for line in lines)))

    print(sum(abs(int(a) - int(b)) for a, b in zip(sorted(lists[0]), sorted(lists[1]))))

    print(sum(int(a)*lists[1].count(a) for a in lists[0]))
