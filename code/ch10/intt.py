class Interesting(object):
        def __getattr__(self,name):
            print('this only called when you have not this attribute')

        def __getattribute__(self,name):
            if name == 'name' or name == 'age':
                print('now hit the access control')
                raise ValueError('you can not access this')
            else:
                return super().__getattribute__(name)
        
        def __init__(self,name,age,date):
            self.name = name
            self.age = age
            self.date = date

        def __dict__(self):
            print('nothing you will get')
