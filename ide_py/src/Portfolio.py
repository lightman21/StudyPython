
class Reader(object):

    path = ''

    def __init__(self,path):
        self.path = path

    def read(self):
        import  csv
        with open(path,'r') as f:
            data = csv.reader(file)
            header = next(data)

            for r in data:
                print r


if __name__ == '__main__':
    path = '/Users/lightman_mac/portfolio.csv'

    r = Reader(path)
    r.read()


