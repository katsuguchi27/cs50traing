from cs50 import get_int

firstwo = 0
cardnum = get_int("Number: ")
temp = cardnum
lenght = len(str(cardnum))
temp = cardnum
while (temp > 100):
    temp //= 10
firstwo = temp
temp = cardnum
sum1 = 0
sum2 = 0
position = 0
while (temp > 0):
    digit = temp % 10
    if (position % 2 == 1):
        product = digit * 2
        if (product > 9):
            product = (product // 10) + (product % 10)
        sum1 += product
    else:
        sum2 += digit
    temp //= 10
    position += 1
total = sum1 + sum2
if (total % 10 != 0):
    print("INVALID")
elif (firstwo // 10 == 4 and (lenght == 13 or lenght == 16)):
    print("VISA");
elif ((firstwo == 34 or firstwo == 37) and lenght == 15):
    print("AMEX");
elif (firstwo <= 55 and firstwo >= 51 and lenght == 16):
    print("MASTERCARD");
else:
    print("INVALID")