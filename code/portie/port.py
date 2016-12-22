# port.py
from . import reader    # Package-relative import

def read_portfolio(filename,*,errors='warns'):
    '''
    Read a CSV file with name,date,shares,price data into a list
    '''
    return portie.reader.read_csv(filename,[str,str,int,float],errors=errors)

if __name__ == '__main__':
    portfolio = read_portfolio('Data/portfolio.csv')

    total = 0.0
    for holding in portfolio:
        total += holding['shares'] * holding['price']

    print('Total cost:',total)
