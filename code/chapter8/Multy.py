class Parent(object):
    def tfuc(self):
        print('Parent print')

pass

class A(Parent):
        def tfuc(self):
            print('A print')

pass
   
   
class B(Parent,A):
        def tfuc(self):
            print('B print')

pass
   
class C(Parent,A,B):
        def tfuc(self):
            print('C print')

# if __name__ == '__main__':
