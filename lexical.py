#define tokens
def tokenize_and_categorize(input_program):
    # Define sets for different token types
    keywords = set(["auto", "break", "case", "char", "const", "continue", "default", "do", "double", "else",
                    "enum", "extern", "float", "for", "goto", "if", "int", "long", "register", "return", "short",
                    "signed", "sizeof", "static", "struct", "switch", "typedef", "union", "unsigned", "void",
                    "volatile", "while", "string", "class", "struc", "include"])
    
    operators = set(["++", "-", "=", "*", "/", "%", "--", "<=", ">="])
    special_characters = set(r"[@&~!#$\^|{}]:;<>,.'()")
    numerals = set("0123456789")

    # Tokenize the input program
    input_program_tokens = []
    current_token = ""
    
    for char in input_program:
        if char.isspace() or char in special_characters or char in operators:
            if current_token:
                input_program_tokens.append(current_token)
                current_token = ""
            if char != ' ':
                input_program_tokens.append(char)
        else:
            current_token += char
    
    if current_token:
        input_program_tokens.append(current_token)

    # Print the header for the table
    print("{:<20} {:<30}".format("Lexeme", "Token"))
    print("="*50)

    # To Categorize The Tokens
    for token in input_program_tokens:
        category = ""
        if token in keywords:
            category = "Keyword/Reserved Word"
        elif token.lower() in ["int", "char", "double", "float", "long", "short", "signed", "unsigned", "void"]:
            category = "Data Type"
        elif token in operators:
            category = "Operator"
        elif all(char in numerals for char in token):
            category = "Numeral"
        elif all(char in special_characters for char in token):
            category = "Special Character/Symbol"
        elif token.isidentifier():
            category = "Identifier"
        elif '.' in token and token.split('.')[0].isalpha() and token.split('.')[1] == 'h':
            category = "Header"
        elif token == ';':
            category = "Terminator (End of Statement)"
            break  # Exit the loop after encountering the terminator
        else:
            category = "Unknown Value"

        # Print the token and its category in a formatted way
        print("{:<20} {:<30}".format(token, category))

# Example usage
input_program = input("Enter Your Code: ")
tokenize_and_categorize(input_program)