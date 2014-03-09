# Generates a few tests

from os import sys

import jsonparser

def getNumericStrings():
    
    good_numbers = [
        '0.,',
        '.0,',
        '123123.,',
        '.1213,',
        '1213.3232,',
        '313123,',
        '123e+80,',
        '67456234}',
        '1,',
        '0}',
    ]

    bad_numbers = [
        '}',
        '.,',
        ',.',
        'aasd}',
        '123123.123123.}'
    ]

    number_tests = []
    number_tests += (map(lambda t : (t, True), good_numbers))
    number_tests += (map(lambda t : (t, False), bad_numbers))
    return number_tests

def main():
    number_tests = getNumericStrings()
    for test in number_tests:
        testfile = open('tests/test.txt', 'w')
        testfile.write(test[0])
        testfile.close()

        tokenizer = jsonparser.Tokenizer('tests/test.txt')
        num_val = tokenizer.readNumber()
        if test[1] and num_val == None:
            assert False
        if not test[1] and num_val:
            assert False

if __name__ == '__main__':
    main()
