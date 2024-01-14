KEYWORDS = set(["auto", "break", "case", "char", "const", "continue", "default", "do", "double", "else",
                "enum", "extern", "float", "for", "goto", "if", "int", "long", "register", "return", "short",
                "signed", "sizeof", "static", "struct", "switch", "typedef", "union", "unsigned", "void",
                "volatile", "while", "string", "class", "struct", "include"])
OPERATORS = set(["++", "--", "+", "-", "*", "/", "%", "=", "<", ">", "<=", ">="])
DELIMITERS = set(["[", "]", "(", ")", "{", "}", " ", "//", "/*", "*/", "}", "'", '"', ";", ":"])
NUMERALS = set("0123456789")
GENERAL = set(["ERROR", "EOF"])
IDENTIFIERS = set()

token_d = {
    "int": "DT_INT",
    "char": "DT_CHAR",
    "float": "DT_FLOAT",
    "double": "DT_DOUBLE",
    "if": "IF_STM",
    "else": "ELSE_STM",
    "for": "LP_STM",
    "while": "WHILE_STM",
    "do": "DO_STM",
    "=": "ASSIGN",
    "+=": "ADD_ASSIGN",
    "-=": "MINUS_ASSIGN",
    "*=": "MULTI_ASSIGN",
    "/=": "DIV_ASSIGN",
    "%=": "MODULO_ASSIGN",
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
    ";": "SEMICOLON",
    "(": "LPAREN",
    ")": "RPAREN",
    "[": "LBRAC",
    "]": "RBRAC",
    "{": "LCURLBRAC",
    "}": "RCURLBRAC",
    "//": "SINGLE_COMMENT",
    "/*": "RMULTI_COMMENT",
    "*/": "LMULTI_COMMENT",
    " ": "SPACE",
    "'": "SQOUT",
    '"': "DQOUT",
    ":": "COLON",
    ",": "COM"
}


def is_valid_identifier(identifier):
    # Rules for a valid identifier
    return (
        identifier.isidentifier()
        and identifier[0].isalpha() or identifier[0] == '_'
        and identifier.lower() not in KEYWORDS  # Check if the lowercase version is a keyword
        and ' ' not in identifier
        and all(char.isalnum() or char in ['-', '_'] for char in identifier)
        and identifier not in IDENTIFIERS
    )


def tokenize_and_categorize(input_program):
    lexeme_token_pairs = []

    current_pos = 0
    input_length = len(input_program)

    while current_pos < input_length:
        char = input_program[current_pos]

        if char.isspace():
            current_pos += 1
            continue

        if char.isdigit():
            numeral = ""
            while current_pos < input_length and input_program[current_pos].isdigit():
                numeral += input_program[current_pos]
                current_pos += 1
            lexeme_token_pairs.append((numeral, "NUMERAL"))

        elif char.isalpha() or char == '_':
            identifier = ""
            while current_pos < input_length and (
                    input_program[current_pos].isalnum() or input_program[current_pos] in ['-', '_']):
                identifier += input_program[current_pos]
                current_pos += 1

            # Check if the identifier is a keyword
            if identifier.lower() in KEYWORDS:
                lexeme_token_pairs.append((identifier, token_d.get(identifier.lower(), "INVALID")))
            elif is_valid_identifier(identifier):
                lexeme_token_pairs.append((identifier, "IDENTIFIER"))
                IDENTIFIERS.add(identifier)
            else:
                lexeme_token_pairs.append((identifier, "INVALID"))

        else:
            found_lexeme = False
            for lexeme, token in token_d.items():
                if input_program.startswith(lexeme, current_pos):
                    lexeme_token_pairs.append((lexeme, token))
                    current_pos += len(lexeme)
                    found_lexeme = True
                    break

            if not found_lexeme:
                lexeme_token_pairs.append((char, "INVALID"))
                current_pos += 1

    print("Lexeme\t\t\tToken\n")
    for lexeme, token in lexeme_token_pairs:
        print(f"{lexeme}\t\t\t{token}")

# Example usage
input_program = input("Enter Your Code: ")
tokenize_and_categorize(input_program)
