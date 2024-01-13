#lexical analyzer
#library for regular expression
import re
#define tokens
def tokenize_and_categorize(input_program):
    # Define regular expressions for different token types
    keywords = set(["auto", "break", "case", "char", "const", "continue", "default", "do", "double", "else",
                    "enum", "extern", "float", "for", "goto", "if", "int", "long", "register", "return", "short",
                    "signed", "sizeof", "static", "struct", "switch", "typedef", "union", "unsigned", "void",
                    "volatile", "while", "string", "class", "struc", "include"])
    
    operators = re.compile(r"(\++)|(-)|(=)|(\*)|(/)|(%)|(--)|(<=)|(>=)")
    numerals = re.compile(r"^\d+$")
    special_characters = re.compile(r"[\[@&~!#$\^\|{}\]:;<>?,\.']|\(\)|\(|\)|{}|\[\]|\"")
    identifiers = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_\-]*$")
    headers = re.compile(r"([a-zA-Z]+\.[h])")

    # Tokenize the input program
    input_program_tokens = re.findall(r'\b\w+\b', input_program)

    # To Categorize The Tokens
    for token in input_program_tokens:
        if token in keywords:
            print(token, "-------> Keyword/Reserved Word")
        elif token.lower() in ["int", "char", "double", "float", "long", "short", "signed", "unsigned", "void"]:
            print(token, "-------> Data Type")
        elif operators.match(token):
            print(token, "-------> Operator")
        elif numerals.match(token):
            print(token, "-------> Numeral")
        elif special_characters.match(token):
            print(token, "-------> Special Character/Symbol")
        elif identifiers.match(token):
            print(token, "-------> Identifier")
        elif headers.match(token):
            print(token, "-------> Header")
        elif token == ';':
            print(token, "-------> Terminator (End of Statement)")
            break  # Exit the loop after encountering the terminator
        else:
            print("Unknown Value")

# Example usage
input_program = input("Enter Your Code: ")
tokenize_and_categorize(input_program)
