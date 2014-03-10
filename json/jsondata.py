# Defines the json data type.

class JsonObject:
    """ Represents a json object
    """

    jsonNullValue = 'NULL_VALUE'

    def __init__(self):
        self.__keyvals = {}

    def addObject(self, key, obj):
        if key in self.__keyvals:
            return False
        self.__keyvals[key] = obj
        return True
    
    def getKeys(self):
        return self.__keyvals.keys()

    def getObjByKey(self, key):
        if key in self.__keyvals:
            return self.__keyvals[key]
        raise KeyError("key not present in the object")

