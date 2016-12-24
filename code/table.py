# table 2016-12-24 study attribute

#! /usr/bin/env python3

def print_table(objects,colnames):
    for colname in colnames:
        print('{:>10s}'.format(colname), end='')
    print()
    for obj in objects:
        for colname in colnames:
            print('{:>10s}'.format(str(getattr(obj,colname))),end='')
        print()
