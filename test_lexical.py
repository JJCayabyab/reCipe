# Define tokens
def tokenize_and_categorize(input_program):
    # Define sets for different token types
    keywords = set(["auto", "break", "case", "char", "const", "continue", "default", "do", "double", "else",
                    "enum", "extern", "float", "for", "goto", "if", "int", "long", "register", "return", "short",
                    "signed", "sizeof", "static", "struct", "switch", "typedef", "union", "unsigned", "void",
                    "volatile", "while", "string", "class", "struct", "include"])

    operators = set(["++", "-", "=", "*", "/", "%", "--", "<=", ">="])
    special_characters = set("[]]@&~!#$\^|{}:;<>,.'()")
    numerals = set("0123456789")

    # Split input_program into tokens
    input_program_tokens = input_program.split()

    # Categorize the tokens
    for token in input_program_tokens:
        ctoken = ""
        if token in keywords:
            ctoken = "KEYWORD"
        elif token in operators:
            ctoken = "OPERATOR"
        elif token in special_characters:
            ctoken = "SPECIAL_CHARACTER"
        elif token.isdigit():
            ctoken = "NUMERAL"
        else:
            ctoken = "IDENTIFIER"  # Assuming anything else is an identifier

        print(f"Token: {token}, Type: {ctoken}")

# Example usage
input_program = input("Enter Your Code: ")
tokenize_and_categorize(input_program)
