# FirstClass.py my first Python class

class Holding(object):
    def __init__(self, name, date, shares, price):
        self.name = name
        self.date = date
        self.shares = shares
        self.price = price

    def cost(self):
        return self.shares * self.price

    import csv

    def read_portfolio(self,filename):
        ports = []
        with open(filename) as f:
            rows = csv.reader(f)
            header = next(rows)
            for row in rows:
                h = Holding(row[0],row[1],row[2],row[3])
                ports.append(h)

        return ports

if __name__ == '__main__':
    h = Holding('tanghao','1988-02-01',28,250)
    print(h)
    print(h.name,h.date,h.shares,h.price)

    filename = '../data/protfolio.csv'
    data = read_portfolio(filename)
    print(data)


