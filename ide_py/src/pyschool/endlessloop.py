
def mixedList(mlist):
    cp = mlist[:]
    print(id(mlist))
    for m in mlist:
        t = m
        print(id(mlist))
        if isinstance(t,str):
             t = int(t)
        cp.append(t)

    mi = min(cp)
    ma = max(cp)
    print(mi)
    print(ma)

    return (mi,ma)

if __name__ == '__main__':
    mlist = [0,'-2','4']
    mixedList(mlist)

