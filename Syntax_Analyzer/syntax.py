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

# AST Node classes
class DataTypeNode:
    def __init__(self, datatype):
        self.datatype = datatype

class IdentifierNode:
    def __init__(self, name):
        self.name = name

class AssignmentNode:
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value

class DeclarationNode:
    def __init__(self, datatype, identifiers, assignments=None):
        self.datatype = datatype
        self.identifiers = identifiers
        self.assignments = assignments if assignments is not None else []

class ValueNode:
    def __init__(self, values) :
        self.values = values

# Parsing functions
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = -1
        self.advance()

    def advance(self):
        self.index += 1
        if self.index < len(self.tokens):
            self.current = self.tokens[self.index]
            print("Current token:", self.current)
        return self.current

    def data_types(self):
        if self.current in KEY:
            datatype = self.current
            self.advance()
            return DataTypeNode(datatype)
        else:
            raise SyntaxError("Expected data type keyword but found: " + str(self.current))

    def identifiers(self):
        if self.current == TT_ID:
            identifier = self.current
            self.advance()
            return IdentifierNode(identifier)
        else:
            raise SyntaxError("Expected identifier but found: " + str(self.current))

    def assign(self):
        if self.current == TT_ID:
            identifier = self.current
            self.advance()
            if self.current == TT_ASS:
                self.advance()
                if self.current in [DIGITS, LETTERS_DIGITS, BOOL, TT_ID]:
                    value = self.current
                    self.advance()
                    return AssignmentNode(identifier, value)
                else:
                    raise SyntaxError("Expected value after '=' but found: " + str(self.current))
            else:
                raise SyntaxError("Expected '=' after identifier but found: " + str(self.current))
        else:
            raise SyntaxError("Expected identifier but found: " + str(self.current))
        
    def values(self):
        if self.current in [DIGITS, LETTERS_DIGITS, BOOL, TT_ID]:
            value = self.current
            self.advance()  # Move to the next token
            return ValueNode (value)
        else:
            raise SyntaxError("Invalid value encountered: " + str(self.current))

    def declarations(self):
        datatype_node = self.data_types()
        identifier_node = self.identifiers()

        if self.current == TT_SEMI:
            self.advance()
            return DeclarationNode(datatype_node, [identifier_node])

        elif self.current == TT_COM:
            self.advance()
            identifiers = [identifier_node]
            while self.current == TT_ID:
                identifier_node = self.identifiers()
                identifiers.append(identifier_node)
                if self.current == TT_COM:
                    self.advance()
                else:
                    break

            if self.current == TT_SEMI:
                self.advance()
                return DeclarationNode(datatype_node, identifiers)
            else:
                raise SyntaxError("Expected ';' after identifiers but found: " + str(self.current))

        elif self.current == TT_ASS:
            assignments = [self.assign()]
            while self.current == TT_COM:
                self.advance()
                assignments.append(self.assign())
            if self.current == TT_SEMI:
                self.advance()
                return DeclarationNode(datatype_node, [], assignments)
            else:
                raise SyntaxError("Expected ';' after assignments but found: " + str(self.current))
        else:
            raise SyntaxError("Invalid syntax at declaration: " + str(self.current))


# Function to read tokens from a file
def read_tokens_from_file(file_path):
    with open(file_path, 'r') as file:
        tokens = file.read().split(":")
    return tokens

# Example usage with a text file
file_path = 'lexer.txt'
tokens = read_tokens_from_file(file_path)
parser = Parser(tokens)
ast = parser.declarations()
