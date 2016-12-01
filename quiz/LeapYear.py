'''
write a function that determines if a given year is a leap year.
 A leap year is divisible by 4, but not by 100, unless it is also divisible by 400.
'''
def LeapYear(yr):
    if (yr % 4 == 0) and (yr % 100 != 0) or (yr % 4 == 0 and yr % 400 == 0):
            return True
    else:
            return False

print(LeapYear(2012))
print(LeapYear(2010))

