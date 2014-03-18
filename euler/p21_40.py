from algos import primes, combinatorics

# Problem 21 asks for the sum of all amicable numbers below 10000
def p21():
    divSum = primes.getDivSum(10000)
    ret = 0
    for n in xrange(1, 10000):
        dSum = divSum[n]
        if dSum != n and dSum < 10000 and divSum[dSum] == n:
            ret += n
    return ret

# problem 23 asks for sum of all numbers that cannot be written as a sum
# of two abundant numbers.
def p23():
    divSum = primes.getDivSum(28123)
    def isAbundant(n):
        return divSum[n] > n

    # There are about 6900 abundant numbers in this range
    # and brute force looping through all these numbers works quite well.
    abundantNumbers = filter(isAbundant, xrange(1, 28124))

    ret = 0
    for n in xrange(1, 28124):
        valid = True
        for a in abundantNumbers:
            if a >= n:
                break
            if isAbundant(n-a):
                valid = False
                break
        
        if valid:
            ret += n
    return ret

# Millionth lexicographic permutation of digits 0-9
# There are 10! (~3600000) permutations, we could list all them in order
# and pick the millionth one. Alternatively, we can compute the digits directly.
def p24():
    """ If we write all the permutations of digits 0-9 in lexicographic order,
    we want the millionth one in that list """
    def factorial(n):
        if n <= 1:
            return 1
        return reduce(lambda x, y:x*y, xrange(1, n+1))

    digits = range(10)
    ret, pos = '', 1000000
    while digits:
        n = len(digits)

        # i*(n-1)! >= pos
        i = (pos + factorial(n-1) - 1) / factorial(n-1) - 1
        ret += str(digits[i])
        pos -= i * factorial(n-1)
        digits[i:i+1] = []
    
    return ret

# The first fibonacci number with 1000 digits.
def p25():
    """ First fibonacci number with 1000 digits """
    a,b,i = 1,1,1
    while len(str(a)) < 1000:
        a,b,i = b,a+b,i+1
    return i

# Problem 26 asks to compute the recurring parts of the fractions 1/n for all 1 <= n < 1000
def getRecurringLen(n):
    """ Returns the length of the recurring part of the fraction 1/n """

    index = {}
    rem, curIndex = 1, 0
    while rem > 0 and rem not in index:
        index[rem] = curIndex
        rem = rem * 10
        ext = 0
        while rem < n:
            rem = rem * 10
            ext += 1

        curIndex += 1 + ext
        rem = rem % n

    if rem == 0:
        return 0
    return curIndex - index[rem%n]

def p26():
    """ Recurring parts of fractions 1/n for 1 <= n < 1000 """
    maxLen, n = 0, 1
    for d in xrange(2, 1000):
        if getRecurringLen(d) > maxLen:
            maxLen, n = getRecurringLen(d), d

    return n

# Problem 27 asks to find the pair (a, b) s.t -999 <= a, b < 1000
# and the sequence n*n + a*n + b produces the longest sequence of primes
# starting at n = 0
def getLen(a, b):
    n = 0
    while primes.checkIfPrime(n*n + a*n + b):
        n = n+1
    return n

def p27():
    """ a and b s.t n*n + a*n + b produces the longest sequence of primes """
    maxLen, res = 0, 0
    for a in xrange(-999, 1000):
        for b in xrange(-999, 1000):
            seqLen = getLen(a, b)
            if seqLen > maxLen:
                maxLen = seqLen
                res = a*b
    return res

# Problem 28 is about computing the sum of numbers on the 
# main diagonals of an infinite grid
def p28():
    """ Compute the sum of the numbers on the diagonals of the given infinite grid """

    # Treat the central 1x1 square different as it has only 1 number.
    ret = 1
    for s in xrange(3, 1002, 2):
        d = s-1
        ret += sum(s*s-i*d for i in xrange(4))
    return ret

# Problem 29 is about counting the no. of distinct numbers in the set
# [a^b | 2 <= a <= 100, 2 <= b <= 100]
def getRoot(n):
    """ Returns the least a s.t. there exists x s.t a^x = n """
    for a in xrange(2, n+1):
        t,e  = 1, 0
        while t < n:
            t = t*a
            e = e+1

        if t == n:
            return (a, e)

    return (n, 1)


# This doesn't have to actually compute the powers.
def p29():
    allPowers = set()
    for n in xrange(2, 101):
        a,x = getRoot(n)
        for b in xrange(2, 101):
            allPowers.add((a, b*x))

    return len(allPowers)

# problem 30 asks for the sum of all integers whose digits fifth power sum
# equals the number. for e.g. 54748 = 5^5 + 4^5 + 7^5 + 4^5 + 8^5
# If such a number x has n digits, then it must satisfy 10^(n-1) <= x
# and its max digit sum can be n * 9^5. This implies 10^(n-1) <= n * (9^5)
# The lhs is an exponential function while the rhs is a linear function
# and so for all n > 6, the inequality is never satisfied. So, we only need to 
# loop through all numbers with less than 7 digits and check if they satisfy the
# desired property.
def p30():
    ret = 0
    for n in xrange(2, 10**6):
        digPowerSum = sum(dig**5 for dig in map(int, str(n)))
        if digPowerSum == n:
            ret += n

    return ret

# No. of ways to make up 2 pounds(=200 pence) with the given denominations
# This can be solved with a recurrence relation and dynamic programming.
# F(amount, x) := no. of ways to make up 'amount' pence using only denominations
# not greater than x.
def p31():
    denoms = [1, 2, 5, 10, 20, 50, 100, 200]

    F = [0] * 201
    F[0] = 1
    
    for d in denoms:
        F2 = [0] * 201
        for amt in xrange(201):
            F2[amt] = F[amt]
            if amt >= d:
                F2[amt] += F2[amt-d]
        
        F = F2

    return F[200]

# If a given number n has d digits, then 10^(d-1) <= n
# and for an interesting number, n < d * (9!)
# This means 10^(d-1) <= d * 9! which means all the interesting numbers
# are of 7 digits at max. We can brute force through all combinations of digits
# upto 7-digits and check if they sum up correctly.
def p34():
    """ check if the digits' factorials sum to the given number """ 
    def factorial(n):
        if n < 1:
            return 1
        return reduce(lambda x, y : x*y, map(int, str(n)))

    def check(n):
        digFacSum = sum(factorial(dig) for dig in map(int, str(n)))
        return digFacSum == n

    goodSet = set()
    def recurse(digits, facSum, curDigit):
        if digits == 0:
            if check(facSum):
                goodSet.add(facSum)
            return

        for d in xrange(curDigit, 10):
            recurse(digits - 1, facSum + factorial(d), d)

    for d in xrange(1, 8):
        recurse(d, 0, 0)

    # deduct the trivial 1 and 2
    return sum(goodSet) - 3

def p35():
    """ All the numbers whose all rotations are prime numbers """
    primeList = primes.getPrimeList(1000000)
    primality = [False] * 1000001
    for p in primeList:
        primality[p] = True

    def rotations(s):
        n = len(s)
        return [s[i:] + s[0:i] for i in xrange(n)]

    def circularPrime(p):
        return all(map(lambda p : primality[p], map(int, rotations(str(p)))))

    return sum(1 for p in xrange(1, 1000000) if circularPrime(p))

def p36():
    """ All double palindromic numbers less than 1 million """
    def isDoublePalindrome(n):
        decimal = str(n)
        if decimal != decimal[::-1]:
            return False
        binary = bin(n)[2:]
        return binary == binary[::-1]

    return sum(n for n in xrange(1, 1000000) if isDoublePalindrome(n))

# It seems that there are no 9-digit truncable primes, which implies there are no
# truncable primes longer than 9 digits. A recursive brute-force solution should work
# well under the time limit.
def p37():
    """ All truncatable prime numbers """
    plist = primes.getPrimeList(10**7)
    primality = [False] * (10**7)
    for p in plist:
        primality[p] = True

    def checkIfPrime(n):
        if n < 10**7:
            return primality[n]

        sqrt = int(n ** 0.5)
        for s in xrange(2, sqrt+1):
            if n % s == 0:
                return False
        return True

    # Checks if every suffix of n is a prime.
    def checkRightTruncable(n):
        numDigits = len(str(n))
        for i in xrange(1, numDigits+1):
            rnum = n % (10**i)
            if not checkIfPrime(rnum):
                return False

        return True
        
    def recurse(digits, p = 0):
        if digits == 0:
            if checkRightTruncable(p):
                return p
            return 0

        ret = 0
        for d in xrange(10):
            if checkIfPrime(10*p+d):
                ret += recurse(digits-1, 10*p+d)

        return ret

    return sum(map(recurse, xrange(2, 9)))

# Compute the nth digit in the infinite string formed when we concatenate
# all the natural numbers together - 12345..101112...
def p40():
    """ Asks for computing the nth digit for any given n in the infinite
    series 12345.... """
    
    # no. of integers with exactly n digits(no leading zeroes)
    def countNth(n):
        return (10**n) - (10 ** (n-1))

    # this is the primary function.
    def nthDigit(n):
        d = 1
        while d*countNth(d) < n:
            n -= d*countNth(d)
            d = d+1
        
        numberWithNth = (n-1) / d + 10 ** (d-1)
        n -= (n-1) / d * d
        n -= 1
        return str(numberWithNth)[n]

    ret = 1
    for i in xrange(1,7):
        ret = ret * int(nthDigit(10**i))
    return ret



probFuncs = [p21, None, p23, p24, p25, p26, p27, 
             p28, p29, p30, p31, None, None, p34,
             p35, p36, p37, None, None, p40];
def main():
    print "Input the problem no."
    prob = int(raw_input())
    print probFuncs[prob-21]()

if __name__ == '__main__':
    main()
