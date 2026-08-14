import sys
from cs50 import get_string

if (len(sys.argv) != 2):
    print(f"Usage: python {sys.argv[0]} key")
    sys.exit(1)
if (sys.argv[1].isdigit() == False):
    print(f"Usage: python {sys.argv[0]} key")
    sys.exit(1)
key = int(sys.argv[1])
message = get_string("plaintext: ")
print("ciphertext: ", end='')
for c in message:
    if c.islower():
        print(chr((ord(c) - ord('a') + key) % 26 + ord('a')), end="")
    elif c.isupper():
        print(chr((ord(c) - ord('A') + key) % 26 + ord('A')), end="")
    else:
        print(c, end="")
print()