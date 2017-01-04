#validate.py

class Typed(object):
    expected_type = object
    def __init__(self,name):
        self.name = name

    def __get__(self,instance,cls):
        self.name = name

    def __set__(self,instance,value):
        if not isinstance(value,self.expected_type):
            raise TypeError('Excepted {}'.format(self.expected_type))
        instance.__dict__[self.name] = value

class RInteger(Typed):
    expected_type = int

class RFloat(Typed):
    expected_type = float

class Integer(object):
    def __init__(self,name):
        self.name = name

    def __get__(self,instance, cls):
        return instance.__dict__[self.name]

    def __set__(self,instance,value):
        if not isinstance(value,int):
            raise TypeError('Excepted int')
        instance.__dict__[self.name] = value


class Float(object):
    def __init__(self,name):
        self.name = name

    def __get__(self,instance, cls):
        return instance.__dict__[self.name]

    def __set__(self,instance,value):
        if not isinstance(value,float):
            raise TypeError('Excepted float')
        instance.__dict__[self.name] = value

class Point(object):
    x = Integer('x')
    y = Integer('y')

    def __init__(self,x,y):
        self.x = x
        self.y = y
