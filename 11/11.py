from functools import cache

@cache
def progress(number, blinks):
    if blinks == 0:
        return 1
    if number == 0:
        return progress(1, blinks - 1)
    if len(s := str(number)) % 2 == 0:
        return progress(int(s[:len(s)//2]), blinks - 1) + progress(int(s[len(s)//2:]), blinks - 1)
    return progress(number * 2024, blinks - 1)

with open("input") as file:
    pebbles = [int(num) for num in file.read().strip().split()]

print(sum(progress(pebble, 25) for pebble in pebbles))
print(sum(progress(pebble, 75) for pebble in pebbles))
