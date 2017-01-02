class Holding(object):
class Holding(object):
    def __init__(self,name,date,shares,price):
        self.name = name
        self.date = date
        self.shares = shares
        self.price = price

    def __repr__(self):
        return 'Holding ({!r},{!r},{!r},{!r})'.format(self.name,self.date,self.shares,self.price)

    def __str__(self):
        return '{} shares of {} at ${:0.2f}'.format(self.shares,self.name,self.price)

    pass

if __name__ == '__main__':
    h = Holding('tanghao','1988-02-01',100,32.2)
    print(h)
    str = str(h)
    print(str)
    repr = repr(h)
    print(repr)

    # 100 shares of tanghao at $32.20
    # Holding ('tanghao','1988-02-01',100,32.2)
    def __init__(self,name,date,shares,price):
        self.name = name
        self.date = date
        self.shares = shares
        self.price = price

    def __repr__(self):
        return 'Holding ({!r},{!r},{!r},{!r})'.format(self.name,self.date,self.shares,self.price)

    def __str__(self):
        return '{} shares of {} at ${:0.2f}'.format(self.shares,self.name,self.price)

    pass

if __name__ == '__main__':
    h = Holding('tanghao','1988-02-01',100,32.2)
    print(h)
    str = str(h)
    print(str)
    repr = repr(h)
    print(repr)

    # 100 shares of tanghao at $32.20
    # Holding ('tanghao','1988-02-01',100,32.2)
