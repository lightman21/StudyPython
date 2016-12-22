# reader.py
import csv

def read_csv(filename, types, *, errors='warn'):
    '''
    Read a CSV file with type convertion into a list of dicts
    '''
    if errors not in {'warn', 'silent', 'raise' }:
        raise ValueError("errors must be one of 'warn', 'silent', 'raise'")
    
    records = []
    with open(filename,'r') as f:
        rows = csv.reader(f)
        headers = next(rows)    #Skip the header row
        for rowno, row in enumerate(rows, start=1):
            try:
                row = [ func(val) for func, val in zip(types, row) ]
            except ValueError as err:
                if errors == 'warn':
                    print('Row:',rowno,'Bad row:', row)
                    print('Row:',rowno,'Reason:',err)
                elif errors == 'raise':
                    raise   # Reraises the last exception
                else:
                    pass    # Ignore

            record = dict(zip(headers, row))
            records.append(record)
        return records
