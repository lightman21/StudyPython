# port.py
import reader

#f = open('data/portfolio.csv','r')

#total = 0.0
#with open('data/portfolio.csv','r') as f:
#    #caution: skip a single of input (they are titles)
#    headers = next(f)
#    for line in f:
#        line = line.strip()     # Strip whitespace
#        parts = line.split(',')
#        parts[0] = parts[0].strip('"')
#        parts[1] = parts[1].strip('"')
#        parts[2] = int(parts[2])
#        parts[3] = float(parts[3])
#        total += parts[2] * parts[3]
#        print(parts)
#
#print('total is:',total)

def read_portfolio(filename,*, errors='warn'):
    '''
    Read a CSV file with name,data,shares,price data into a list
    '''
    return reader.read_csv(filename,[str, str, int, float], errors=errors)

if __name__ == '__main__':
    portfolio = read_portfolio('../data/portfolio.csv')

    total = 0.0
    for holding in portfolio:
        total += holding['shares'] * holding['price']

    print('Total costs:', total)
