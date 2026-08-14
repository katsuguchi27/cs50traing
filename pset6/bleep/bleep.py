from cs50 import get_string
import sys


def main():
    if (len(sys.argv) != 2):
        print(f"Usage: python {sys.argv[0]} dictionary")
        sys.exit(1)
    words = set()
    dictionary = sys.argv[1]
    file = open(dictionary, 'r')
    for line in file:
        words.add(line.strip('\n'))
    file.close()
    check = get_string("What message would you like to censor?\n")
    vocab = check.split()
    for i in range(len(vocab)):
        if vocab[i].lower() in words:
            for j in range(len(str(vocab[i]))):
                print('*', end='')
            print(' ', end='')
        else:
            print(f'{vocab[i]}', end=' ')
    print()


if __name__ == "__main__":
    main()
