
def readFile(filename):
    f = open(filename)
    size = 0
    lines = 0
    buf = f.read(1)
    while buf !="":
        size += 1
        buf = f.read(1)
        if buf == '\n':
            lines += 1

    f.close()

    return (size,lines)


if __name__ == '__main__':
    import sys
    filename = sys.argv[0]
    result = readFile(filename)
    print(result)


