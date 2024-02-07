
from token_dict import KEY
import string

# Constants
DIGITS = '0123456789'
LETTERS = set(string.ascii_letters)
LETTERS_DIGITS = LETTERS | set(DIGITS)

# Token Types
TT_ID = "ID"
TT_COM = "COM"
TT_SEMI = "SEMI"
TT_ASS = "ASS"
TT_LIT = "INTL"
TT_FL = "FL"
TT_DL = "DL"
TT_UN = "_"
BOOL = {"TR", "FL"}
VALUES = {"IL", "FL", "DL"}

# Parsing functions

class Parser:
    
#################################### hold value of token

    def __init__(self, tokens):
        self.tokens = tokens
        self.index = -1
        self.advance()
        
#################################### move to next token

    def advance(self):
        self.index += 1
        if self.index < len(self.tokens):
            self.current = self.tokens[self.index]
        return self.current
    
#################################### data types    
#CFG: <DT> ::= INT | CHAR | STR | FLOAT | DOUBLE | BOOL

    def data_types(self):
        if self.current in KEY:
            typespecifier = self.current
            self.advance()
            return typespecifier
        else:
            raise SyntaxError("Expected data type keyword but found: " + str(self.current))
        
#################################### identifiers 
#CFG: <IDEN> ::= <ALPHABET> (<ALPHABET> | <DIGITS> | "_")*| "_" (<ALPHABET> | <DIGITS> | "_")*

    def identifiers(self):
        if self.current is TT_ID:
            identifier = self.current
            self.advance()
        return identifier

#################################### idetifiers list e.g a, b, c
#CFG: <IDENLIST> ::= <IDEN>, <IDENLIST>*

    def iden_list(self):
        idenlist = []
        if self.current == TT_ID:
            idenlist.append(self.current)
            self.advance()

            while self.current == TT_COM:
                self.advance()
                if self.current == TT_ID:
                    idenlist.append(self.current)
                    self.advance()
                else:
                    raise SyntaxError("Expected identifier after comma")

            if self.current != TT_SEMI:  # Check for semicolon after the identifier list
                raise SyntaxError("Expected ';' after identifier list")

        else:
            raise SyntaxError("Expected identifier at the beginning of identifier list")
        
        return idenlist

#################################### assigment statements
#CFG: <ASS> ::= <IDEN> = <VAL>

    def assign(self):
        if self.current == TT_ID:
            identifier = self.current
            self.advance()
            
            if self.current == TT_ASS:
                self.advance()  # Move past the '=' token
                
                if self.current in VALUES:
                    value = self.current
                    self.advance()
                    return identifier, value
                else:
                    raise SyntaxError("Expected value after '='")
            else:
                raise SyntaxError("Expected '=' after identifier")
        else:
            raise SyntaxError("Expected identifier")
        
#################################### assigment statements list
#CFG: <ASS_STMNT> ::= <ASS> | <ASS>, <ASS_STMNT>

    def assig_list(self):
        ass_list = [self.assign()]  # Parse the first assignment
        while self.current == TT_COM:  # Check for comma
            self.advance()  # Move past the comma
            ass_list.append(self.assign())  # Parse next assignment
        return ass_list
    
####################################  values
#CFG: <VAL> ::= <DIGITS> | <STRING> | <BOOLEAN> | <IDEN>

    def values(self):
        if self.current in [DIGITS, LETTERS_DIGITS, BOOL, TT_ID]:
            value = self.current
            self.advance()  # Move to the next token
            return value
        else:
            raise SyntaxError("Invalid value encountered: " + str(self.current))
        
#################################### 
# DECLARATIONS
#################################### 
#CFG: <DEC_STATEMENT> ::= <DT> <IDEN> ; | <DT> <IDEN> , <IDENLIST>* ; | <DT> <ASS_STMNT> ; | <DT> <IDENLIST> <ASS_STMNT>* ;
    
 

# Function to read tokens from a file
def read_tokens_from_file(file_path):
    
    with open(file_path, 'r') as file:
        tokens = file.read().split(":")
    return tokens

# Example usage with a text file
file_path = 'lexer.txt'  # Replace 'lexer.txt' with the path to your output file
tokens = read_tokens_from_file(file_path)
parser = Parser(tokens)
print(parser.DEC())


