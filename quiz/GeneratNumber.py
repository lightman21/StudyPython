'''
Create a function generateNumbers(start, end) that takes in two numbers as arguments
and returns a list of numbers starting from start to the end number (inclusive)
specified in the arguments.
Note: The function range(x, y) can takes in 2 arguments.
For example, range(1, 5) will return a list of numbers [1,2,3,4].
'''
import sys

def generateNumber(start,end):

    if start >= end:
        start = end

    if start == end:
        return  range(start,start+1)

    return range(start,end+1)

print(len(sys.argv))

if len(sys.argv) != 3 :
    print('Shit Happend')
else:
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    print(start,end)
    generateNumber(start,end)



