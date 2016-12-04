# port.py

#f = open('data/portfolio.csv','r')

total = 0.0
with open('data/portfolio.csv','r') as f:
    #caution: skip a single of input (they are titles)
    headers = next(f)
    for line in f:
        line = line.strip()     # Strip whitespace
        parts = line.split(',')
        parts[0] = parts[0].strip('"')
        parts[1] = parts[1].strip('"')
        parts[2] = int(parts[2])
        parts[3] = float(parts[3])
        total += parts[2] * parts[3]
        print(parts)

print('total is:',total)
