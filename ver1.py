KEYWORDS = set(["auto", "break", "case", "char", "const", "continue", "default", "do", "double", "else",
                    "enum", "extern", "float", "for", "goto", "if", "int", "long", "register", "return", "short",
                    "signed", "sizeof", "static", "struct", "switch", "typedef", "union", "unsigned", "void",
                    "volatile", "while", "string", "class", "struct", "include"])
OPERATORS = set(["++", "--", "+", "-", "*", "/", "%", "=", "<", ">", "<=", ">="])
DELIMITERS = set(["[", "]", "(", ")", "{", "}", " ", "//", "/*", "*/" , "}", "'", '"', ";"])
NUMERALS = set("0123456789")
GENERAL = set(["ERROR", "EOF", ])
IDENTIFIERS = set()

token_dict = {
        #keywords
        "int": "DT_INT",
        "char": "DT_CHAR",
        "float": "DT_FLOAT",
        "double": "DT_DOUBLE",
        "if": "IF_STM",
        "else": "ELSE_STM",
        "for": "LP_STM",
        "while": "WHILE_STM",
        "do": "DO_STM",
        #operators
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
        # delimiters
        ";": "SEMICOLON",
        "(": "LPAREN",
        ")": "RPAREN",
        "[": "LBRAC",
        "]": "RBRAC",
        "{": "LCURLBRAC",
        "}": "RCURLBRAC",
        "'": "SQOUT",
        '"': "DQOUT",
}

def tokenize(source_code):
    tokens = []
    lexemes = []
    current_token = ""

    for char in source_code:
        
        if char.isalnum() or char in ['_', '.']:
            current_token += char
        else:
            if current_token:
                token_type = token_dict.get(current_token, "IDENTIFIER")
                tokens.append((token_type, current_token))
                lexemes.append(current_token)

            current_token = ""

            if char.isspace():
                continue
            elif char in DELIMITERS:
                token_type = token_dict.get(char, "DELIMITER")
                tokens.append((token_type, char))
                lexemes.append(char)
            elif char in OPERATORS:
                current_token += char
                if current_token in OPERATORS:
                    token_type = token_dict.get(current_token, "OPERATOR")
                    tokens.append((token_type, current_token))
                    lexemes.append(current_token)

    return tokens, lexemes

source_code = input("Enter source code: ")
tokens, lexemes = tokenize(source_code)

# Display in table format
print("Lexeme\t\tToken")
print("----------------------")
for token, lexeme in zip(tokens, lexemes):
    print(f"{lexeme}\t\t{token[0]}")
