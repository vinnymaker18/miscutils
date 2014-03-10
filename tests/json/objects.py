# a few unit tests for json objects.

import json
import jsonparser

DATA_FILE = 'tests/objtests.txt'
def getObjects():
    objs = []
    obj1 = {
        "key1" : "null",
        "key2" : 12223,
        "key3" : {
            "k1" : True,
            "k2" : False,
            "k3" : [],
        },
        "A" : []
    }
    objs.append(obj1)

    obj2 = {}
    objs.append(obj2)

    obj3 = {"1":2, "2": 3, "433": "Vinay Emani"}
    objs.append(obj3)
    return map(json.dumps, objs)

def main():
    jObjs = getObjects()
    for obj in jObjs:
        handle = open(DATA_FILE, 'w')
        handle.write(obj)
        handle.close()

        jsonparser.initModule(DATA_FILE)
        readObj = jsonparser.readJsonObject()
        assert readObj != None
        print readObj.getKeys()

if __name__ == '__main__':
    main()
