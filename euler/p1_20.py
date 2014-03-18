# for prime number and combinatoric functions.
from algos import primes, combinatorics

# A number that is evenly divisible by 15 gets added twice.
def p1():
    """ Sum of all integers that are multiples of either 3 or 5 b/w
    1 and 999"""

    # Sum of the natural numbers 1 to n
    def summate(n):
        return n * (n+1) / 2

    return 3 * summate(999/3) + 5 * summate(999/5) - 15*summate(999/15)

# Loop through all the fibonacci numbers < 4 million.
def p2():
    """ Sum of all even fibonacci numbers less than 4 million"""

    ret = 0
    a,b = 1,2

    while a < 4000000:
        if a%2 == 0:
            ret += a

        a,b = b,a+b

    return ret

# Loop upto sqrt of the given number and check for any prime divisors.
def p3():
    """ Largest prime factor of the number 600851475143"""
    number = 600851475143
    squareRoot = int(number ** 0.5)

    ret = 0
    for s in xrange(2, squareRoot+1):
        if number % s == 0:
            if primes.checkIfPrime(s):
                ret = max(ret, s)

            while number % s == 0:
                number = number / s

    if number != 1 and primes.checkIfPrime(number):
        ret = max(ret, number)
    return ret

# Tests if the number n is a palindrome in base 10.
def isPalindrome(n):
    s = str(n)
    return s == s[::-1]

def p4():
    """ Largest palindrome that is a product of 2 3-digit numbers"""
    return max(x*y for x in xrange(100, 1000) for y in xrange(100, 1000) if isPalindrome(x*y))

# gcd of two non-negative integers. gcd(0, x) = 0 for any x.
def gcd(x, y):
    if x == 0:
        return y

    return gcd(y%x, x)

# lcm of two postive integers.
def lcm(x, y):
    return x / gcd(x, y) * y

def p5():
    """ The smallest number that is evenly divisible by every integer from 1 to 20"""
    return reduce(lcm, xrange(1, 21))

def p6():
    """ Diff b/w square of (SIGMA n) and SIGMA (n square) for 1 <= n <= 100"""
    sumOfSquares = sum(x*x for x in xrange(1, 101))
    sumOfNumbers = sum(x for x in xrange(1, 101))
    return sumOfNumbers ** 2 - sumOfSquares

def p7():
    """ 10001st prime """
    # Assuming the 10001st prime is less than a million
    isPrime = [True for n in xrange(1000001)]

    isPrime[1] = False

    for p in xrange(2, 1001):
        if isPrime[p]:
            for q in xrange(p*p, 1000001, p):
                isPrime[q] = False

    primeList = [n for n in xrange(2,1000001) if isPrime[n]]
    return primeList[10000]

def p9():
    """ a*b*c s.t a*a + b*b = c*c and a+b+c = 1000 """
    for a in xrange(1, 1001):
        for b in xrange(1, 1000-a):
            c = 1000 - a - b
            if c*c == a*a + b*b:
                return a*b*c

    return None

def p10():
    """ Sum of all primes less than 2 million """
    return sum(primes.getPrimeList(2000000))


# Goes through all the triangular numbers until one with more than
# 500 factors is reached.
def p12():
    """ Smallest triangular number with more than 500 factors """
    triNumber,i = 1, 2
    while primes.numFactors(triNumber) <= 500:
        triNumber,i = triNumber+i, i+1
    return triNumber


# Length of the collatz sequence starting with n.
def collatzLen(n):
    ret = 1
    while n != 1:
        ret = ret+1
        if n%2 == 0:
            n = n/2
        else:
            n = 3*n+1

    return ret

def p13():
    """ Number under 1 million with the longest collatz sequence """
    curMaxLen, num = 1, 1
    for n in xrange(2, 1000000):
        colLen = collatzLen(n)
        if colLen > curMaxLen:
            curMaxLen, num = colLen, n

    return num

def p15():
    """ 40 choose 20 """
    return combinatorics.choose(40, 20)

def p16():
    """ Sum of digits in decimal representation of 2^1000 """
    pw = 2**1000
    return sum(map(int, str(pw)))

def p17():
    """ No. of non-whitespace characters when the numbers 1-1000 are written """
    digits = ["Zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    t11 = ["eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", 
            "eighteen", "nineteen"]
    tentes = ["ten", "twenty", "thirty", "forty", "Fifty", "sixty", "seventy", "eighty", "ninety"]
    hundred, thousand = "hundred", "thousand"

    ret = 0

    # 1-99, 101-199, ..., 901-999
    for i in xrange(1, 100):
        word = "asd"
        if i%10 == 0:
            word = tentes[i/10 - 1]
        elif i < 10:
            word = digits[i]
        elif i < 20:
            word = t11[i-11]
        else:
            word = tentes[i/10 - 1] + digits[i%10]

        ret += len(word)
        for j in xrange(1, 10):
            ret += len(digits[j] + hundred) + 3 + len(word)

    # 100, 200, .., 900
    for d in digits:
        if d != "Zero":
            ret += len(d) + len(hundred)

    # 1000
    ret += 3 + len(thousand)
    return ret

# Sum of all digits in 100!
def p20():
    f100 = reduce(lambda x, y: x*y, xrange(1, 101))
    return sum(map(int, str(f100)))

    
# Array of functions solving a single problem each.
funcs = [None, p1, p2,
        p3, p4, p5, p6, p7, None, p9,
        p10, None, p12, p13, None, p15,
        p16, p17, None, None, p20, ]


def main():
    print "Enter the problem to be solved"
    probNum = int(raw_input())
    print funcs[probNum]()

if __name__ == '__main__':
    main()
