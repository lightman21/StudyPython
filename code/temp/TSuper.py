class A(object):
    def __init__(self):
        print('A init')
    pass
    
    def __repr__(self):
        return type(self) + '{!r}'.format(self)


class B(object):
    def __init__(self):
        print('B init')
    pass


class C(object):
    def __init__(self):
        print('C init')
    pass


class D(object):
    def __init__(self):
        print('D init')
        t = super()
        print('the D super type is ' ,type(t))
        self.hello()

    def hello(self):
        print('hello world')
        print('the D super type is ' ,type(super()))
    pass
