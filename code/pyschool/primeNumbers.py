'''
Create a function that takes in a positive integer and return a list of prime numbers.
A prime number is only divisible by 1 and itself
'''

def primeNumbers(num):
    primes = []
    i = 2
    # iterates through range from 2 to num(inclusive)
    while i:    
        k = 2
        isPrime = True
        # check if prime number
        while k:    
            if i % k == 0:
                isPrime = False
            k
        if isPrime:
            primes.append(i)

        i

    return primes
