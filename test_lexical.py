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
            if token == "=":
                ctoken = "ASSIGN"
            elif token == "+=":
                ctoken = "ADD_ASSIGN"
            elif token == "-=":
                ctoken = "MINUS_ASSIGN"
            elif token == "*=":
                ctoken = "MULTI_ASSIGN"
            elif token == "/=":
                ctoken = "DIV_ASSIGN"
            elif token == "%=":
                ctoken = "MODULO_ASSIGN"
            elif token == "+":
                ctoken = "ADD"
            elif token == "-":
                ctoken = "MINUS"
            elif token == "*":
                ctoken = "MULTI"
            elif token == "/":
                ctoken = "DIV"
            elif token == "%":
                ctoken = "MODULO"
            elif token == "+":
                ctoken = "POSITIVE"
            elif token == "-":
                ctoken = "NEGATIVE"
            elif token == "++":
                ctoken = "INCRE"
            elif token == "--":
                ctoken = "DECRE"
            elif token == "!":
                ctoken = "LOGIC_NOT"
            elif token == "||":
                ctoken = "LOGIC_OR"
            elif token == "&&":
                ctoken = "LOGIC_AND"
            elif token == "==":
                ctoken = "EQUAL_TO"
            elif token == "!=":
                ctoken = "NOT_EQUAL_TO"
            elif token == ">":
                ctoken = "GREATER_THAN"
            elif token == "<":
                ctoken = "LESS_THAN"
            elif token == ">=":
                ctoken = "GREAT_OR_EQUAL"
            elif token == "<=":
                ctoken = "LESS_OR_EQUAL"
            elif token != operators:
                ctoken = "INVALID"
                
        # SPECIAL CHARACTERS / SYMBOLS
        elif token in delimeters:
            if token == ";":
                ctoken = "SEMICOLON"
            elif token == "(":
                ctoken = "LPAREN"
            elif token == ")":
                ctoken = "RPAREN" 
            elif token == "[":    
                ctoken = "LBRAC"
            elif token == "]":    
                ctoken = "RBRAC"
            elif token == "{":    
                ctoken = "LCURLBRAC"
            elif token == "}":    
                ctoken = "RCURLBRAC"
            elif token == "//":    
                ctoken = "SINGLE_COMMENT"
            elif token == "/*":    
                ctoken = "RMULTI_COMMENT"
            elif token == "*/":    
                ctoken = "LMULTI_COMMENT"
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
