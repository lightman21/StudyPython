'''
Wite a function shiftByTwo(*args) that takes in variable-length argument and 
returns a tuple with its elements shifted to the right by two indeces.
'''
def shiftByTwo(*args):
    args = list(args)
    mlen = len(args)
    if mlen >= 2:
        last = args.__getitem__(mlen-2)
        llast = args.__getitem__(mlen-3)
        args.insert(0,last)
        args.insert(1,llast)
        return args[;len(args)-2]
    else:
            return args

if __name__ == '__main__':
    import sys

        
