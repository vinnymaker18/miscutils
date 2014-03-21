# All the prime number related algorithms are implemented here.

# Uses the sieve of eratosthenes algorithm. Should easily run under less
# than a minute for n upto 10 million on even a semi decent machine.
def getPrimeList(n):
    """ Returns a list of primes not greater than n """

    isPrime = [True for x in xrange(n+1)]
    isPrime[0] = isPrime[1] = False

    s = int(n ** 0.5)
    for p in xrange(2, s+1):
        if isPrime[p]:
            for q in xrange(p*p, n+1, p):
                isPrime[q] = False

    return [x for x in xrange(2, n+1) if isPrime[x]]


# O(sqrt(n))
def checkIfPrime(n):
    """ Tests the primality of n """

    if n < 2:
        return False

    s = int(n ** 0.5)
    for p in xrange(2, s+1):
        if n%p == 0:
            return False
    return True


# Prime factorises a positive integer.
# O(sqrt(n))
def factorize(n):
    """ Prime factorises n """

    # Loop upto sqrt(n) and check for factors
    ret = []

    sqRoot = int(n ** 0.5)
    for f in xrange(2, sqRoot+1):
        if n%f == 0:
            e = 0
            while n%f == 0:
                n,e = n/f, e+1

            ret.append((f, e))
    if n > 1:
        ret.append((n, 1))
    
    return ret

# Returns the no. of divisors(factors) of a positive integer.
def numFactors(n):
    """ Number of divisors of n """
    primeFactors = factorize(n)
    ret = 1
    for (p,e) in primeFactors:
        ret = ret*(e+1)
    return ret

# Returns an array of proper divisor sums of 1..n
def getDivSum(n):
    """ Proper divisor sums """
    ret = [0] * (n+1)
    for d in xrange(1, n+1):
        for m in xrange(2*d, n+1, d):
            ret[m] += d
    return ret

# Primality upto 10 million.
def main():
    allPrimes = getPrimeList(10000000)
    print allPrimes[100100]

# script
if __name__ == '__main__':
    main()
