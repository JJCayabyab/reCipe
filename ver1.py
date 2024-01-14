KEYWORDS = set(["auto", "break", "case", "char", "const", "continue", "default", "do", "double", "else",
                    "enum", "extern", "float", "for", "goto", "if", "int", "long", "register", "return", "short",
                    "signed", "sizeof", "static", "struct", "switch", "typedef", "union", "unsigned", "void",
                    "volatile", "while", "string", "class", "struct", "include"])
OPERATORS = set(["++", "--", "+", "-", "*", "/", "%", "=", "<", ">", "<=", ">="])
DELIMITERS = set(["[", "]", "(", ")", "{", "}", " ", "//", "/*", "*/" , "}", "'", '"', ";"])
NUMERALS = set("0123456789")

def is_valid_identifier(token):
    # Check if the token follows the pattern for a valid identifier
    if token[0].isalpha() or token[0] == '_':
        for char in token[1:]:
            if not (char.isalnum() or char == '_'):
                return False
        return True
    return False

def tokenize_and_categorize(input_program):
    keywords = {
        "int": "DT_INT",
        "char": "DT_CHAR",
        "float": "DT_FLOAT",
        "double": "DT_DOUBLE",
        "if": "IF_STM",
        "else": "ELSE_STM",
        "for": "LP_STM",
        "while": "WHILE_STM",
        "do": "DO_STM",
    }

    operators = {
        "=": "ASSIGN",
        "+=": "ADD_ASSIGN",
        "-=": "MINUS_ASSIGN",
        "*=": "MULTI_ASSIGN",
        "/=": "DIV_ASSIGN",
        "+": "ADD",
        "-": "MINUS",
        "*": "MULTI",
        "/": "DIV",
        "%": "MODULO",
        "++": "INCRE",
        "--": "DECRE",
        "!": "LOGIC_NOT",
        "||": "LOGIC_OR",
        "&&": "LOGIC_AND",
        "==": "EQUAL_TO",
        "!=": "NOT_EQUAL_TO",
        ">": "GREATER_THAN",
        "<": "LESS_THAN",
        ">=": "GREAT_OR_EQUAL",
        "<=": "LESS_OR_EQUAL",
    }

    delimiters = {
        ";": "SPECIAL_CHAR",
        "(": "LPAREN",
        ")": "RPAREN",
        "[": "LBRAC",
        "]": "RBRAC",
        "{": "LCURLBRAC",
        "}": "RCURLBRAC",
        "'": "SQOUT",
        '"': "DQOUT",
    }
    
    input_program_tokens = [token for token in input_program.split() if token.strip()]
    lexeme_token_pairs = []

    for token in input_program_tokens:
        # Check for semicolon and separate it from the identifier
        if ";" in token:
            identifier = token.rstrip(";")
            lexeme_token_pairs.append((identifier, "IDENT"))
            lexeme_token_pairs.append((";", "SPECIAL_CHAR"))
        else:
            lexeme = token
            ctoken = ""

            # Handle keywords (case-insensitive)
            if token.lower() in keywords:
                ctoken = keywords[token.lower()]

            # Handle operators
            elif token in operators:
                ctoken = operators[token]

            # Handle delimiters
            elif token in delimiters:
                ctoken = delimiters[token]
    

            # Handle identifiers
            else:
                # Check if the token follows the pattern for a valid identifier
                if is_valid_identifier(token):
                    ctoken = "IDENT"
                else:
                    print(f"Error: Unrecognized token - {token}")

            lexeme_token_pairs.append((lexeme, ctoken))

    print("Lexeme\t\t\tToken")
    for lexeme, token in lexeme_token_pairs:
        print(f"{lexeme}\t\t\t{token}")

# Example usage
input_program = input("Enter Your Code: ")
tokenize_and_categorize(input_program)