import unittest
from algos import primes

"""Unit tests for the primes module in algos package.
"""

class PrimesTestCase(unittest.TestCase):
    def testFewKnownPrimes(self):
        known_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 
                        47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        
        for n in xrange(1, 101):
            inclusion = n in known_primes
            primality = primes.checkIfPrime(n)
            self.assertTrue(not (inclusion ^ primality))


if __name__ == '__main__':
    unittest.main()

