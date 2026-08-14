from cs50 import get_float

dollars = 0
coins = 0
rest = 0

while dollars <= 0:
    dollars = get_float("Changed owed: ")
coins = round(dollars * 100)
if (coins // 25 > 0):
    rest += coins // 25
    coins = coins % 25
if (coins // 10 > 0):
    rest += coins // 10
    coins = coins % 10
if (coins // 5 > 0):
    rest += coins // 5
    coins = coins % 5
if (coins // 1 > 0):
    rest += coins // 1
    coins = coins % 1
print(f"{rest}")