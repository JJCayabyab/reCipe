# Define tokens
def tokenize_and_categorize(input_program):
    # Define sets for different token types
    keywords = set(["auto", "break", "case", "char", "const", "continue", "default", "do", "double", "else",
                    "enum", "extern", "float", "for", "goto", "if", "int", "long", "register", "return", "short",
                    "signed", "sizeof", "static", "struct", "switch", "typedef", "union", "unsigned", "void",
                    "volatile", "while", "string", "class", "struct", "include"])

    operators = set(["++", "-", "=", "*", "/", "%", "--", "<=", ">="])
    delimeters = set(["[", "]", "(", ")", "{", "}", " ", "//", "/*", "*/" , "}", "'", '"', ";"])
    numerals = set("0123456789")

    # Split input_program into tokens
    input_program_tokens = input_program.split()

    # Create a list to store lexeme-token pairs
    lexeme_token_pairs = []

    # Categorize the tokens
    for token in input_program_tokens:
        
        lexeme = token
        ctoken = ""
        
        # KEYWORDS 
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
            elif token != keywords:
                ctoken = "INVALID"
            
        # OPERATORS
        elif token in operators:
            if token == "++":
                ctoken = "INC"
            elif token == "+":
                ctoken = "PLUS"
            elif token == "--":
                ctoken = "DEC"
            elif token == "-":
                ctoken = "MINUS"
            elif token == "*":
                ctoken = "MULTI"
            elif token == "/":
                ctoken = "DIV"
            elif token == "%":
                ctoken = "MOD"
            elif token == "=":
                ctoken = "EQUALS"
            elif token == "==":
                ctoken = "EQUALITY"
            elif token == "+=":
                ctoken = "PLUS_ASSIGN"
            elif token == "-=":
                ctoken = "MINUS_ASSIGN"
            elif token == "*=":
                ctoken = "MULTI_ASSIGN"
            elif token == "/=":
                ctoken = "DIV_ASSIGN"
            elif token == ">":
                ctoken = "GREATER"
            elif token == "<":
                ctoken = "LESS"
            elif token == "!=":
                ctoken = "NOT_EQUAL"
            elif token == ">=":
                ctoken = "GREATER_OR_EQUAL"
            elif token == "<=":
                ctoken = "LESS_OR_EQUAL"
            elif token == "&&":
                ctoken = "LOG_AND"
            elif token == "||":
                ctoken = "LOG_OR"
            elif token != operators:
                ctoken = "INVALID"
                
        # SPECIAL CHARACTERS / SYMBOLS
        elif token in delimeters:
            if token == "!":
                ctoken = "EXSYM"
            elif token == "@":
                ctoken = "ATSYM"
            elif token == "#":
                ctoken = "HASHSYM"
            elif token == "$":
                ctoken = "DOSYM"
            elif token == "%":
                ctoken = "PERSYM"
            elif token == "^":
                ctoken = "CARSYM"
            elif token == "&":
                ctoken = "ANDSYM"
            elif token == "*":
                ctoken = "ASTSYM"
            elif token == "(":
                ctoken = "LPAREN"
            elif token == ")":
                ctoken = "RPAREN"
            elif token == "-":
                ctoken = "HPSYM"  
            elif token == "_":    
                ctoken = "UDSYM"  
            elif token == "[":    
                ctoken = "LBRAC"
            elif token == "]":    
                ctoken = "RBRAC"
            elif token == ":":
                ctoken = "COLON"
            elif token == ";":
                ctoken = "SEMICOLON"
            elif token == "'":
                ctoken = "SQOUT"
            elif token == '"':
                ctoken = "DQOUT"
            elif token == ",":
                ctoken = "COMMA"
            elif token == '.':
                ctoken = "DOTSYM"
            elif token == "/":
                ctoken = "SLSYM"
            elif token == " ":
                ctoken = "SPACE"
                
            else:
                ctoken = "INVALID"
                                                          
        elif token.isdigit():
                ctoken = "NUMERAL"
                
        else:
                ctoken = "IDENTIFIER"  # Assuming anything else is an identifier

        lexeme_token_pairs.append((lexeme, ctoken))
    #
    
    # Print the table
    print("Lexeme\t\tToken")
    print("-----------------------")
    for lexeme, token in lexeme_token_pairs:
        print(f"{lexeme}\t\t{token}")

# Example usage
input_program = input("Enter Your Code: ")
tokenize_and_categorize(input_program)
