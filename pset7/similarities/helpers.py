from nltk.tokenize import sent_tokenize

def lines(a, b):
    """Return lines in both a and b"""
    lines_a = set(a.splitlines())
    lines_b = set(b.splitlines())
    list1 = list(lines_a & lines_b)
    return list1


def sentences(a, b):
    """Return sentences in both a and b"""
    sentences1 = set(sent_tokenize(a))
    sentences2 = set(sent_tokenize(b))
    list2 = list(sentences1 & sentences2)
    return list2


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""
    sub_a = set()
    for i in range(len(a) - n + 1):
        sub_a.add(a[i:i+n])
    sub_b = set()
    for i in range(len(b) - n + 1):
        sub_b.add(b[i:i+n])
    list3 = list(sub_a & sub_b)
    return list3
