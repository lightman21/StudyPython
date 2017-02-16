def invertDictionary(d):
    keys = d.keys()
    values = d.values()
    dn = {}
    for v in values:
        k = v2k(d, v)
        dn[v] = k
    return dn


def v2k(d, v):
    mlist = []
    for k in d.keys():
        if d[k] == v:
            mlist.append(k)
    return mlist

if __name__ == '__main__':
    d = {1:'a',2:'b',3:'a',4:'c',5:'b'}
    print(d)
    d = invertDictionary(d)
    print(d)