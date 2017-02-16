'''
Write the function getCommonLetters(word1, word2) that takes in two words as arguments 
and returns a new string that contains letters found in both string. 
Ignore repeated letters and sort the result in alphabetical order.
'''

def getCommon(w1,w2):
    min = w1 if len(w1)  < len(w2) else w2
    max = w1 if len(w1)  > len(w2) else w2
    comm = []
    for i in range(len(min)):
        if min[i] == max[i]:
            comm.append(min[i])

    if len(comm) == 0:
        print 'no common'
        return 'no common'
    else:
        print (sorted(set(comm)))
        return sorted(set(comm))

def commLetters(w1,w2):
    min = w1 if len(w1)  < len(w2) else w2
    max = w1 if len(w1)  > len(w2) else w2

    comm = []
    for w in min:
        if w in max:
            comm.append(w)
    if len(comm) == 0:
        return ''
    else:
        return sorted(set(comm))

import sys
if __name__ == '__main__':
    w1 = sys.argv[1]
    w2 = sys.argv[2]
    comm = commLetters(w1,w2)
    print(comm)


