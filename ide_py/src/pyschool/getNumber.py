def getNumbers(num):
    rt = []
    if num <= 1:
        rt.append(num)
        return rt

    min = -1 if num % 2 == 0 else 0
    mlist = range(num, min, -2)
    reverse_cp = mlist[::-1]
    mlist.extend(reverse_cp)

    if mlist.count(0) > 1:
        mlist.remove(0)

    import math

    for x in mlist:
        rt.append(int(math.pow(x, 2)))

    return rt

if __name__ == '__main__':
    num = 9
    rt = getNumbers(num)
    print(rt)
    # print('num = {}, rt = {}'.format(num,rt.__repr__()))
