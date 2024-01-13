# Define tokens
def tokenize_and_categorize(input_program):
    # Define sets for different token types
    keywords = set(["auto", "break", "case", "char", "const", "continue", "default", "do", "double", "else",
                    "enum", "extern", "float", "for", "goto", "if", "int", "long", "register", "return", "short",
                    "signed", "sizeof", "static", "struct", "switch", "typedef", "union", "unsigned", "void",
                    "volatile", "while", "string", "class", "struct", "include"])

    operators = set(["++", "-", "=", "*", "/", "%", "--", "<=", ">="])
    special_characters = set("[]@&~!#$\^|{}:;<>,.'()")
    numerals = set("0123456789")

    # Split input_program into tokens
    input_program_tokens = input_program.split()

    # Create a list to store lexeme-token pairs
    lexeme_token_pairs = []

    # Categorize the tokens
    for token in input_program_tokens:
        
        lexeme = token
        ctoken = ""
        
        #KEYWORDS/DATA TYPE/STATEMENTS
        if token in keywords:
            if token == "int":
                ctoken = "DT_INT"          
            elif token == "char":
                ctoken = "DT_CHAR"
            elif token == "float":     
                ctoken = "DT_FLOAT"
            elif token == "double":
                ctoken = "DT_DOUBLE"          
            elif token == "if":
                ctoken = "IF_STM"
            elif token == "else":
                ctoken = "ELSE_STM"
            elif token == "for":
                ctoken = "LP_STM"
            elif token == "while":
                ctoken = "WHILE_STM"
            elif token == "do":
                ctoken = "DO_STM"
            
        #OPERATORS
        elif token in operators:
            ctoken = "OPERATOR"
        elif token in special_characters:
            ctoken = "SPECIAL_CHARACTER"
        elif token.isdigit():
            ctoken = "NUMERAL"
        else:
            ctoken = "IDENTIFIER"  # Assuming anything else is an identifier

        lexeme_token_pairs.append((lexeme, ctoken))

    # Print the table
    print("Lexeme\t\tToken")
    print("-----------------------")
    for lexeme, token in lexeme_token_pairs:
        print(f"{lexeme}\t\t{token}")

# Example usage
input_program = input("Enter Your Code: ")
tokenize_and_categorize(input_program)
