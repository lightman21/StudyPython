def csvReader(filename):
    records = []
    quote = '\"'
    for line in open(filename):
        line = line.rstrip()
        if len(line) > 0 and line.__contains__(quote):
            lt = line.split(quote)
            if len(lt) > 0:
                cp = []
                for li in lt:
                    if len(li) > 0:
                        li = li.replace(quote,'')
                        if li.startswith(','):
                            li = li[1:]
                        cp.append(li)
                        print('li = {}'.format(li))

                records.append(cp)
    return records

if __name__ == '__main__':
    import sys
    name = sys.argv[1]
    rt = csvReader(name)
    print(rt)

