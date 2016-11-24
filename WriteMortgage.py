# find out how long to a pay off a mortgage
# and show how to format output and redirect it to a file

principle = 500000
payment = 2486.11
rate = 0.05
total_paid = 0

#Extra payment info
extra_payment = 1000
extra_payment_start_month = 1
extra_payment_end_month = 60
month = 0

out=open('schedule.txt','w')

print('{:>5s} {:>10s} {:>10s} {:>10s}'.format('month','interest','principle','total_paid'),file=out)
while principle > 0:
    month += 1
    if month >= extra_payment_start_month and month <= extra_payment_end_month:
        total_payment = payment + extra_payment
    else :
        total_payment = payment
        interest = principle * (rate / 12)
        principle = principle + interest - total_payment
        total_paid += total_payment
        print('{:>5d} {:>10.2f} {:>10.2f} {:>10.2f}'.format(month,interest,principle,total_paid),
              file=out)
out.close()
print('Total paid: ',total_paid)
