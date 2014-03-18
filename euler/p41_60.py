import primes
import combinatorics
import time

# No need to consider 9 digit numbers because every such number is divisible
# by 3. While I couldn't prove that no such 8 digit number exists, this program
# runs within a couple of seconds.
def p41():

    """ Largest pandigital prime """
    res = 0
    for d in xrange(4, 9):
        digits = range(1, d+1)
        allPerms = combinatorics.genAllPerms(digits)
        for perm in allPerms:
            num = 0
            for d in perm:
                num = 10*num + d

            if primes.checkIfPrime(num):
                res = max(res, num)

    return res

def p42():
    digits = range(10)
    allPerms = combinatorics.genAllPerms(digits)

    def getVal(perm):
        return reduce(lambda x, y : 10*x+y, perm)

    def check(perm):
        primes = [2, 3, 5, 7, 11, 13, 17]
        for i in xrange(1, 8):
            subseq = 100*perm[i] + 10*perm[i+1] + perm[i+2]
            if subseq % primes[i-1] != 0:
                return False
        return True
        
    ret = 0
    for perm in allPerms:
        if check(perm):
            ret += getVal(perm)
    return ret


# Find the prime below 1 million that can be written as a sum of
# most consecutive primes.
def p50():
    """ Which prime below 1 million can be summed up with 
    most consecutive primes """

    # all the primes less than 1 million
    primeList = primes.getPrimeList(999999)
    primality = [False] * 1000000
    for p in primeList:
        primality[p] = True

    p,l = 2, 1
    for i in xrange(len(primeList)):
        total = 0
        for j in xrange(i, len(primeList)):
            if total >= 1000000:
                break
            if j-i+1 > l and primality[total]:
                p, l = total, j-i+1
            total += primeList[j]
    return p

# Simple brute force checking should work for this problem.
def p52():
    """ Smallest integer n s.t n,2*n,...,6*n all have same digits. """

    # Returns the digits in the decimal representation of a positive integer n
    def digits(n):
        ret = []
        while n > 0:
            ret.append(n % 10)
            n = n / 10
        ret.sort()

        return ret

    # Checks if integers x,2x,3x,4x,5x,6x all have same digits.
    def check(n):
        digs = digits(n)
        
        for i in xrange(2, 7):
            if digs != digits(i*n):
                return False
        return True

    n = 1
    while not check(n):
        n = n+1

    return n


# Again, simple brute force check.
def p55():
    """ No. of lychrel numbers below 10000 """
    def isPalindrome(s):
        return s == s[::-1]

    def isLychrel(n):
        for i in xrange(50):
            sn = str(n)
            n2 = int(sn) + int(sn[::-1])
            if isPalindrome(str(n2)):
                return False
            n = n2

        return True

    return sum(1 for n in xrange(1, 10000) if isLychrel(n))

# It seems like such a 5-prime set can be found within 100000
def p60():
    """ The 5-prime set with the least sum s.t concatenation
    of any pair of primes in any order results in a prime"""

    # we start with n = 100000
    pslist = primes.getPrimeList(100000)
    matchingPrimes = {}

    def add(p, q):
        if p not in matchingPrimes:
            matchingPrimes[p] = set()
        matchingPrimes[p].add(q)
        return

    def recurse(ps):
        if len(ps) == 5:
            return sum(ps)

        ret = 10**100
        p1 = ps[0]

        if p1 not in matchingPrimes:
            return ret

        for q in matchingPrimes[p1]:
            matchesAll = True
            for p in ps[1:]:
                if q not in matchingPrimes[p]:
                    matchesAll = False
                    break

            if matchesAll:
                ret = min(ret, recurse(ps+[q]))

        return ret

    for p in pslist:
        for q in pslist:
            if p >= q:
                break
            pq = int(str(p)+str(q))
            qp = int(str(q)+str(p))
            if primes.checkIfPrime(qp) and primes.checkIfPrime(pq):
                add(p, q)
                add(q, p)
    
    
    ret = 1<<100
    for p in pslist:
        if p in matchingPrimes:
            ret = min(ret, recurse([p]))

    return ret

# Each cube maps to a unique string, which is the concatenation of its
# digits in increasing order. Iterate through postive integers and storing
# these strings in a map and stop when a particular string is mapped from 5
# integers.
def p62():
    """ Asks for the least cube s.t its digit permutation contain
    exactly 5 perfect cubes """

    def getDigits(n):
        digits = map(int, str(n))
        digits.sort()
        return digits

    permuteMap = {}

    for n in xrange(1,10**9):
        digitStr = ''.join(map(str, getDigits(n*n*n)))
        if digitStr not in permuteMap:
            permuteMap[digitStr] = set()
        permuteMap[digitStr].add(n)

        if len(permuteMap[digitStr]) >= 5:
            return n

    return -1

# A map from problem numbers to their implementations.
problems = {
    41 : p41,
    42 : p42,
    50 : p50,
    52 : p52,
    55 : p55,
    60 : p60,
}

def main():
    print "Input the problem number"
    prob = int(raw_input())

    if prob not in problems:
        print "Sorry, I've decided this problem is not interesting enough"
        return

    startTime = time.time()
    result = problems[prob]()
    finishTime = time.time()

    print "The result is ", result, " and it took ", (finishTime - startTime), " seconds"

if __name__ == '__main__':
    main()
