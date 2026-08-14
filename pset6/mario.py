from cs50 import get_int

n = 0
while (n < 1 or n > 8):
    n = get_int("Height: ")
for i in range(1, n+1):
    for j in range(n-i):
        print(" ", end='')
    for k in range(i):
        print("#", end='')
    print()