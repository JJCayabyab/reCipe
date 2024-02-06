from token_dict import  KEY, DELI, OPER, RES
# Constants
import string

DIGITS = '0123456789'
LETTERS = set(string.ascii_letters)
LETTERS_DIGITS = LETTERS | set(DIGITS)

TT_INT_LITERAL = "IL"
TT_FLOAT_LITERAL = "FL"
TT_DOUBLE_LITERAL = "DL"

# Parsing functions
class Parser:
    
    def __init__ (self, tokens):
        self.tokens = tokens
        self.index = -1
        self.current = None
        self.advance()
    
    def advance(self):
        self.index += 1
        if self.index < len(self.tokens):
            self.current = self.tokens[self.index]
        else:
            self.current = None
        return self.current
    
    def declaration(self):
        data_type = self.data_types()
        if self.current == ',':
            identifiers = self.iden_list()
            self.advance()
            return [{data_type, identifiers} for identifiers in identifiers]
        elif self.current == '=':
            self.advance()
            ass_list = self.assig_list()
            return [(data_type, ass[0], ass[1]) for ass in ass_list]
        else:
            identifier = self.identifiers()
            return [(data_type, identifier)]
    
    def data_types(self):
        if self.current in KEY:
            typespecifier = self.current
            self.advance()
            return typespecifier
        else:
            raise SyntaxError("Expected keyword but found: " + self.current)
    
    def identifiers(self):
        if self.current is None:
            raise SyntaxError("Unexpected end of input: Expected identifier")
        if self.current[0] == '_':
            identifier = self.current
            self.advance()
            while self.current is not None and (self.current[0] in LETTERS or self.current[0] == '_'):
                identifier += self.current
                self.advance()
            return ("ID")
        elif self.current[0] in LETTERS:
            identifier = self.current
            self.advance()
            while self.current is not None and (self.current[0] in LETTERS or self.current[0] == '_') :
                identifier += self.current
                self.advance()
            return ("ID")
        else:
            raise SyntaxError("Invalid identifier: " + str(self.current))

    def iden_list(self):
        idenlist = [self.identifiers()]
        while self.current == ',':
            self.advance()
            idenlist.append(self.identifiers())
        return idenlist
    
    def assign(self):
        identifier = self.identifiers()
        if self.current == '=':
            self.advance()
            value = self.values()
            return identifier, value
        else:
            raise SyntaxError("Expected '=' after identifier but found: " + self.current)
    
    def assig_list(self):
        ass_list = [self.assign()]
        while self.current == ',':
            self.advance()
            ass_list.append(self.assign())  
        return ass_list


    def values(self):
        if self.current in DIGITS:
            return int(self.current)
        elif self.current in ["TRUE", "FALSE"]:
            return True if self.current == 'TRUE' else False
        elif self.current in LETTERS_DIGITS or self.current == '_':
            return self.identifiers()
        else:
            raise SyntaxError("Invalid value: " + self.current)

# Example usage
tokens = ['INT', 'ANDFNDFJididid454345 fefd', "," ,'a', '=', '10', ';']
parser = Parser(tokens)
print(parser.declaration())
            

            