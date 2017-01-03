class Holding(object):
    def __init__(self,name,date,shares,price):
        self.name = name
        self.date = date
        self.shares = shares
        self._price = price

    @property
    def price():
        return _price

    @price.setter
    def price(self,newprice):
        if not isinstance(newprice,float):
            raise TypeError('Excepted float')
        if newprice < 0:
            raise ValueError('must >= 0')
        self._price = newprice

    @property
    def cost():
        return self.shares * self.price


