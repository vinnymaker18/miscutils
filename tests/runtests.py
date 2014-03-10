#!/usr/bin/python

# This is a simple script to run tests in this project. Goals are as follows.
# 1) User must be able to select tests to run by a package(e.g., json, algos).
# Later versions of this script will also let the user select tests individually.

# Command line arguments to be interpreted as follows. The first 1 or 2 arguments
# are about this script itself. (Can either be run as python runtests.py or ./runtests.py)
# The rest of the tokens comprise a list of tasks. A hyphenated token denotes a major parameter
# and precedes a list (possibly empty) of its arguments.
from os import sys

def main():
    sys.path.insert(0, '../json/')
    # TODO(vinayemani@gmail.com) : implement this.

if __name__ == '__main__':
    main()
