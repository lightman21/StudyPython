'''
Pairwise comparision of DNA sequences is a popular technique used in Bioinformatics.
It usually involves some scoring scheme to express the degree of similarity.
Write a function that compares two DNA sequences based on the following scoring scheme:
+1 for a match, +3 for each consecutive match and -1 for each mismatch.

Examples
>>> print pairwiseScore("ATTCGT", "ATCTAT")
    ATTCGT
    ||   |
    ATCTAT
    Score: 2
    >>> print pairwiseScore("GATAAATCTGGTCT", "CATTCATCATGCAA")
    GATAAATCTGGTCT
     ||  |||  |
    CATTCATCATGCAA
    Score: 4
    >>>
'''


def pairwiseScore(seqA, seqB):
    len_a = len(seqA)
    len_b = len(seqB)
    common_index = []
    step = len_b if len_a > len_b else len_a

    # assume that they have the same length
    for i in range(step):
        if seqA[i] == seqB[i]:
            common_index.append(i)

    # now all matched sequences recorded to a  list
    score = 0
    strlist = []

    for i in range(len(common_index)):
        if i-1 >= 0:
            if common_index[i]-common_index[i-1] == 1:
                # consecutive
                score += 3
            else:
                score += 1
        else:
            score += 1

    for i in range(step):
        if i not in common_index:
            score -= 1
            strlist.append(' ')
        else:
            strlist.append('|')

    return seqA + "\n" + ''.join(strlist) + seqB + "\n" + "Score: " + str(score)


if __name__ == '__main__':
    import sys
    seqA = sys.argv[1]
    seqB = sys.argv[2]
    result = pairwiseScore(seqA,seqB)
    print('seqA ={},seqB={}, result ={}'.format(seqA,seqB,result))


