# print_table 2016-12-24 study attribute

def print_table(objects,colnames):
    for colname in colnames:
        print('{:>10s}'.format(colname), ends='')
