
'''
demonstrate Python inheritance
'''

class Parent(object):
    def __init__(self,value):
        self.value = value

    def spam(self):
        print ('Parent.spam',self.value)

    def grok(self):
        print('Parent.grok')
        self.spam()

    pass

class Child(Parent):
    def spam(self):
        print('Child.spam',self.value)

    def grok(self):
        print('Child.grok',self.value)
        super(self).grok()

    pass

class Child2(Parent,object):
    def __init__(self,value,extra):
        self.extra = extra

    def grok(self):
        print ('just print super ',super)
        print ('Multiple Inheritance  child.grok')



if __name__ == '__main__':
    # child = Child(20)
    # child.spam()
    # child.grok()

    parent = Parent(111)
    parent.spam()
    print ('spam type',type(parent.spam()))
    print ('value type ',type(parent.value))

    # child2 = Child2(10,555)


