def splitWord(word, num):
    parts = len(word) / num if len(word) / num == 0 else int(len(word) / num) + 1
    if len(word) == num:
        parts = 1
    step = parts
    blist = []
    slist = []

    print('{},{},parts={}'.format(word, num, parts))

    for w in word:
        if len(slist) != num:
            slist.append(w)
            if len(slist) == num:
                blist.append(''.join(slist))
                slist = []
                step -= 1
        if len(slist) == num:
            blist.append(''.join(slist))
            slist = []
            step -= 1

        # the last loop
        if len(slist) != 0 and step == 1:
            blist.append(''.join(slist))

    return blist

if __name__ == '__main__':
    import sys
    w = sys.argv[1]
    n = int(sys.argv[2])
    rs = splitWord(w,n)
    print(rs)