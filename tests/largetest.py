# This generates a large json object with a hundred thousand
# key, val pairs in it and writes it to a file, which will be
# fed to jsonparser.py
import json
import jsonparser
from os import sys

NUM_VALUES = 100000

def generateObject():
    ret = {}
    for v in xrange(NUM_VALUES):
        key = "some key" + str(v)
        val = { "another key" : [{"as" : 2, "be" : 3}]}
        ret[key] = val

    return json.dumps(ret)

def main():
    large_obj = generateObject()
    file_obj = open('tests/largetest.json', 'w')
    file_obj.write(large_obj)
    file_obj.close()

    jsonparser.initModule('tests/largetest.json')
    largeObj = jsonparser.readJsonObject()

    assert largeObj != None and len(largeObj.getKeys()) == NUM_VALUES

if __name__ == '__main__':
    main()
