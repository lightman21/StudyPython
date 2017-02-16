# Use seek() and read() methods to retrieve a hidden code from a list of indexes.
# A negative index implies searching from the end of document.


def getCode(filename, indexes):
    mlist = []
    with open(filename, 'r') as f:
        for idx in indexes:
            idx = int(idx)
            f.seek(idx, 0)
            t = f.read(1)
            mlist.append(t)
    return ''.join(mlist)

if __name__ == '__main__':
    name = '/tmp/dv.txt'.strip()
    indexes = [4, 992, -26, 1242, 332]
    f = open(name,'r')
    f.seek(-1)
    t = f.read(1)
    print(t)
    # rt = getCode(name, indexes)
    # print(rt)
