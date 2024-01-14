KEYWORDS = set(["auto", "break", "case", "char", "const", "continue", "default", "do", "double", "else",
                    "enum", "extern", "float", "for", "goto", "if", "int", "long", "register", "return", "short",
                    "signed", "sizeof", "static", "struct", "switch", "typedef", "union", "unsigned", "void",
                    "volatile", "while", "string", "class", "struct", "include"])
OPERATORS = set(["++", "--", "+", "-", "*", "/", "%", "=", "<", ">", "<=", ">="])
DELIMITERS = set(["[", "]", "(", ")", "{", "}", " ", "//", "/*", "*/" , "}", "'", '"', ";"])
NUMERALS = set("0123456789")
GENERAL = set(["ERROR", "EOF", ])
IDENTIFIERS = set()

def is_valid_identifier(identifier):
    # Rule 2: Cannot use a keyword as an identifier
    if identifier in KEYWORDS:
        return False
    # Rule 3: Identifier has to begin with a letter or underscore (_)
    if not identifier[0].isalpha() and identifier[0] != '_':
        return False
    # Rule 4: It should not contain white space
    if ' ' in identifier:
        return False
    # Rule 5: Special characters are not allowed
    if not identifier.isalnum() and '_' not in identifier:
        return False
    # Rule 6: Identifiers can consist of only letters, digits, or underscore
    for char in identifier:
        if not char.isalnum() and char != '_':
            return False
    # Rule 7: Only 31 characters are significant
    if len(identifier) > 31:
        return False
    # Rule 8: They are case sensitive
    # Assuming case sensitivity for simplicity in this context

    # Check for uniqueness
    if identifier in IDENTIFIERS:
        return False
    else:
        IDENTIFIERS.add(identifier)

    return True

# Define tokens
def tokenize_and_categorize(input_program):
    # Define sets for different token types
    # Split input_program into tokens
    input_program_tokens = input_program.split()

    # Create a list to store lexeme-token pairs
    lexeme_token_pairs = []

    # Categorize the tokens
    for token in input_program_tokens:
        lexeme = token
        ctoken = ""
        
        # KEYWORDS 
        if token in KEYWORDS:
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
            elif token not in KEYWORDS:
                ctoken = "INVALID"
            
        # OPERATORS
        elif token in OPERATORS:
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
            elif token not in OPERATORS:
                ctoken = "INVALID"
                
        # SPECIAL CHARACTERS / SYMBOLS
        elif token in DELIMITERS:
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
            elif token == "'":    
                ctoken = "SQOUT"
            elif token == '"':    
                ctoken = "DQOUT"
            else:
                ctoken = "INVALID"
            
        # GENERAL
        elif token in GENERAL:
            if token == "ERROR":
                ctoken = "ERROR"
            elif token == "EOF":
                ctoken = "EOF" 
            else:
                ctoken = "INVALID"
                                                          
        elif token.isdigit():
                ctoken = "NUMERAL"
                
        elif token.isalpha() or token[0] == '_':
            if not is_valid_identifier(token):
                ctoken = "INVALID_IDENTIFIER"
            else:
                ctoken = "IDENTIFIER"

        elif "=" in token:
            assignment_parts = token.split("=")
            if len(assignment_parts) == 2 and is_valid_identifier(assignment_parts[0]):
                lexeme_token_pairs.append((assignment_parts[0], "IDENTIFIER"))
                lexeme_token_pairs.append(("=", "ASSIGN"))
                lexeme_token_pairs.append((assignment_parts[1], "NUMERAL"))
            else:
                ctoken = "INVALID"

        else:
            ctoken = "INVALID"
        
        # Append lexeme-token pair
        if ctoken != "INVALID" and ctoken != "":
            lexeme_token_pairs.append((lexeme, ctoken))
    
    # Print the table
    print("Lexeme\t\t\tToken\n")
    for lexeme, token in lexeme_token_pairs:
        print(f"{lexeme}\t\t\t{token}")

# Example usage
input_program = input("Enter Your Code: ")
tokenize_and_categorize(input_program)
