import sys
from cs50 import get_string

if (len(sys.argv) != 2):
    print(f"Usage: python {sys.argv[0]} keyword")
    sys.exit(1)
if (sys.argv[1].isalpha() == False):
    print(f"Usage: python {sys.argv[0]} keyword")
    sys.exit(1)
def shift(a):
    var = 0
    if a.islower():
        var = ord(a) - 97
    elif a.isupper():
        var = ord(a) - 65
    return(var)

keyword = sys.argv[1]
message = get_string("plaintext: ")
print("ciphertext: ", end='')
pos = 0
for c in message:
    if c.islower():
        print(chr((ord(c) - ord('a') + shift(keyword[pos])) % 26 + ord('a')), end="")
        pos += 1
    elif c.isupper():
        print(chr((ord(c) - ord('A') + shift(keyword[pos])) % 26 + ord('A')), end="")
        pos += 1
    else:
         print(c, end="")
    if pos == len(str(keyword)):
        pos = 0
print()