import csv
#! /usr/bin/env python3

'''
write a more general csv reader module
'''

def read_csv(filename,types,errors='warn'):
    if errors not in {'warn','slient','raise'}:
        raise ValueError("errors must be one of 'warn','slient','raise'")

    records = []    # List of records
    with open(filename,'r') as f:
        rows = csv.reader(f)
        headers = next(rows)    #skip the header row
        for rowno, row in enumerate(rows, start=1):
            try:
                row = [ func(val) for func, val in zip(types, row) ]
            except ValueError as err:
                if errors == 'warn':
                   print('Row:',rowno,'Bad row:',row)
                elif errors == 'raise':
                    raise   #Raises the last exception
                else:
                    pass    #Ignore
                continue
            record = dict(zip(headers,row))
            records.append(record)

        return records

'''
usage
import csv_reader
data = csv_reader.read_csv('data/portfolio.csv',[str,str,int,float],'warn')
'''
