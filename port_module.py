# I learn to use cvs module
import csv

#with open('data/portfolio.csv','r') as rows:
#    #skip the first header m_line
#    header = next(rows)
#    for row in rows:
#        print(row[0])

trow = 0
f = open ('data/portfolio.csv','r')
rows = csv.reader(f)
for row in rows:
    print(row)
    trow += 1

print(trow)

