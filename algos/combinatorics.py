# Provides all the combinatoric functions. e.g., combinations, permutations
# N choose K is the no. of ways of choosing K elements from N distinct ones.
# This equals N! / (N-K)! / K! after cancelling common terms, we are left with
# this code.


def choose(n, k):
    """ N Choose K """
    ret = 1
    for i in xrange(1, k + 1):
        ret = ret * (n-k+i) / i
    return ret


# N choose K with dynamic programming approach.
# choose(n,k) = choose(n-1, k) + choose(n-1, k-1)
def choose2(n, k):
    if k < 0 or k > n:
        return 0

    row = [1]
    for i in xrange(1, n+1):
        newRow = [0] * (i+1)
        for j in xrange(i+1):
            if j < i:
                newRow[j] += row[j]
            if j > 0:
                newRow[j] += row[j-1]
        row = newRow

    return row[k]


# Generator for all permutations of the given array.
# Creates a new copy of the array and works with the new copy.
def genAllPerms(array):
    """ Generates all the permutations of the given array
    in the lexicographic order """

    a = list(array)
    n = len(a)
    a.sort()

    while True:
        yield list(a)

        thisIsLeast = True
        for x in xrange(n-1, 0, -1):
            if a[x] > a[x-1]:
                thisIsLeast = False
                break

        if thisIsLeast:
            break

        y = n-1
        while a[y] <= a[x-1]:
            y = y-1

        a[y], a[x-1] = a[x-1], a[y]
        a[x:] = a[x:][::-1]

    return
