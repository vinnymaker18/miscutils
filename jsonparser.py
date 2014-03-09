# This module is for reading input from files and breaking the input
# into tokens. This should provide an interface of the following sorts. 
# readToken(token) :: returns success or raises an exception on failure.
# readJsonValue() :: can read a json value of any type.
# readKey() :: reads a double quoted string and returns it or throws an excn.
# readBack(string) :: when reading a json value, some times, more data is read
#                       is read than necessary. In such a case, users of the above
#                       apis can rewind the stream back by setting the read back.


from os import sys
import jsondata

# few primitives
def isWhiteSpace(c):
    return c in list("\n\t\r ")

def isDigit(c):
    return c in list("0123456789")

# Implements the interface above.
class Tokenizer:

    # Token types.
    STRING_TOKEN = 0,
    LEFT_BRACE = 1,
    RIGHT_BRACE = 2,
    LEFT_SQ_BRACKET = 3,
    RIGHT_SQ_BRACKET = 4,
    COLON = 5,
    COMMA = 6,
    BOOLEAN_TOKEN = 7,
    NULL = 8
    
    def __init__(self, filename = None):
        if not filename:
            filename = sys.stdin
        self.file_handle = open(filename, 'r')
        # read_back is empty by default, when the users of
        # this module have read extra data, they can set this
        # to read it again.
        self.read_back = ''
        # for debugging purposes.

    # When more data is consumed than necessary, 
    # the extra data can be pushed back so as to be able to read it again.
    def setReadBack(self, read_back):
        self.read_back = read_back

    # Reads a single byte from the input stream.
    # Returns a new byte or None on failure (e.g., end of input)
    def _readByte(self, ignore_wspc = True):
        if self.read_back:
            ret = self.read_back[0]
            self.read_back = self.read_back[1:]
            return ret

        while True:
            new_byte = self.file_handle.read(1)
            if not new_byte:
                self.file_handle.close()
                return ''
            elif not isWhiteSpace(new_byte) or not ignore_wspc:
                return new_byte


    # Reads the provided string argument from the input stream.
    # returns True or False, assumes token doesn't have whitespace
    # in it.
    def readToken(self, token):
        for i,c in enumerate(token):
            new_c = self._readByte()
            if new_c != c:
                self.setReadBack(token[0:i]+new_c)
                return False
        return True
    
    # Boolean values are either true or false. Returns the boolean
    # value on success and None on failure.
    def readBoolean(self):
        if self.readToken('true'):
            return True
        if self.readToken('false'):
            return False
        return None

    # Null value is 'null'. Returns True on success and None on
    # failure.
    def readNullValue(self):
        if self.readToken('null'):
            return True
        return None
        
    # Reads a double quoted string from the input stream. Returns the read
    # string on success. On failure, sets the read_back and returns None.
    def _readString(self):
        ret = []
        if not self.readToken('"'):
            return None
        cur_byte = '"'

        while True:
            new_byte = self._readByte(False)

            if not new_byte:
                # end of input.
                self.setReadBack('"' + (''.join(ret)))
                return None

            if new_byte == '"' and cur_byte != '\\':
                # end of the string token.
                return ''.join(ret)

            cur_byte = new_byte
            ret.append(cur_byte)



    # Reads a json key. Implemented as a wrapper over
    # _readString().
    def readKey(self):
        return self._readString()

    # Reads a json string. Wrapper over _readString().
    def readString(self):
        return self._readString()
    
    # Reads until the next delimiter (Comma or a bracket
    # or a right brace or whitespace) and checks for validity of the 
    # syntax.
    def readNumber(self):
        def canStop(c):
            return isWhiteSpace(c) or c == ',' or c == '}'

        # TODO: for now, only accepts digits.
        ret = []
        while True:
            cur_b = self._readByte(False)
            if not isDigit(cur_b):
                self.setReadBack(cur_b)
                break
            ret.append(cur_b)

        return ''.join(ret)

########################### Main APIs that can be used by the user. ###########
######################## Also initializes the tokenizer object. ###############

# initializes the tokenizer object to read from a given filename, or standard
# input if the argument is an empty string. Users should explicitly call this
# with a filename to initialize the tokenizer object.
def initModule(filename):
    global tokenizer
    tokenizer = Tokenizer(filename)


# Can read any of the simple json values and can set the read back in case of 
# failure. Can read json arrays and JsonObjects, but won't rewind the stream 
# back to original state in failure.
def readJsonValue():
    if tokenizer.readToken('null'):
        return jsonparser.JsonObject.jsonNullValue
    
    # Try for a boolean value
    boolVal = tokenizer.readBoolean()
    if boolVal != None:
        return boolVal

    strVal = tokenizer.readString()
    if strVal != None:
        return strVal

    # try for a number
    numVal = tokenizer.readNumber()
    if numVal:
        return numVal

    # try for a compound json object, which must start with a {
    if tokenizer.readToken('{'):
        tokenizer.setReadBack('{')
        return readJsonObject()

    if tokenizer.readToken('['):
        tokenizer.setReadBack('[')
        return readJsonArray()
    else:
        return None
    

# Reads a json object from the input stream. Input error may be detected in 
# the middle of parsing the object, in which case, parsing state will be broken,
# and None will be returned
def readJsonObject():
    
    if not tokenizer.readToken('{'):
        return None
    json_obj = jsondata.JsonObject()

    while True:
        # read a key, val pair separated by a colon.
        key = tokenizer.readKey()
        if not key:
            if tokenizer.readToken('}'):
                return json_obj
            else:
                return None

        if not tokenizer.readToken(':'):
            return None

        val = readJsonValue()
        if None == val:
            return None
        json_obj.addObject(key, val)
        tokenizer.readToken(',')

# Reads a json array from the input stream. In case of invalid data, parsing
# state will be broken and None will be returned.
def readJsonArray():
    if not tokenizer.readToken('['):
        return None
    json_array = []
    while True:
        if tokenizer.readToken(']'):
            return json_array
        tokenizer.readToken(',')
        new_val = readJsonValue()
        if None == new_val:
            return None
        json_array.append(new_val)


# If run as a script, tries to read from standard input.
if __name__ == '__main__':
    # do something here if run as a script.
    print "do something here"
