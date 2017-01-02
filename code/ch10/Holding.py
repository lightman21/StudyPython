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
    print(h.__dict__)
    print()
    print(Holding.__dict__)
