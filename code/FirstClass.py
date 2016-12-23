# FirstClass.py my first Python class

class Holding(object):
    def __init__(self, name, date, shares, price):
        self.name = name
        self.date = date
        self.shares = shares
        self.price = price

    def cost(self):
        return self.shares * self.price

if __name__ == '__main__':
    h = Holding('tanghao','1988-02-01',28,250)
    print(h)
    print(h.name,h.date,h.shares,h.price)
