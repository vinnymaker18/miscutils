# few unit tests for reading double-quoted strings.

import jsonparser

string_tests = {
    '"Hello, World"' : True,
    '"A bad test' : False,
    '""' : True,
    '' : False,
    '"A brave new world \" for strings"' : True,
    '"hello" "world"' : True,
}

def main():
    for dat,res in string_tests.iteritems():

        testfile = open('tests/strtest.txt', 'w')
        testfile.write(dat)
        testfile.close()

        tokenizer = jsonparser.Tokenizer('tests/strtest.txt')
        read_val = tokenizer.readString()
        assert (res == (read_val != None))
    return

if __name__ == '__main__':
    main()
