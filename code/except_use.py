# show how to use try except
import csv

def portfolio_cost(filename):
    '''
    computes total shares*price for a CSV file with name,data,shares,price data
    '''
    total = 0.0
    with open (filename,'r') as f:
        rows = csv.reader(f)
        headers = next(rows) #skip the header row
        rowno = 0

        for row in rows:
            rowno += 1
            try:
                row[2] = int(row[2])
                row[3] = float(row[3])
            except ValueError as error:
                print('Row: ', rowno,'Bad row: ',row)
                print('Row: ',  rowno,'Reson: ',error)
                continue    #skip to the next row
            total += row[2] * row[3]
    return total



def realway(filename,*,errors='warn'):
    '''
    computes total shares*price for a CSV file with name,data,shares,price data
    '''
    if errors  not in {'warn','silent','raise'}:
        raise ValueError("errors must one of 'warn','silent','raise'")

    total = 0.0
    with open (filename,'r') as f:
        rows = csv.reader(f)
        headers = next(rows) #skip the header row

        for rowno,row in enumerate(rows,start=1):
            try:
                row[2] = int(row[2])
                row[3] = float(row[3])
            except ValueError as error:
                if errors == 'warn':
                    print('Row: ', rowno,'Bad row: ',row)
                    print('Row: ',  rowno,'Reson: ',error)
                elif errors == 'raise':
                    raise   #Reraises the last exception
                else:
                    pass    #Ignore it
                continue    #skip to the next row

            total += row[2] * row[3]
    return total


#total = realway('data/missing.csv')
total = realway('data/missing.csv',errors='silent')
print('Total cost: ',total)



















