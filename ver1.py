KEYWORDS = set(["auto", "break", "case", "char", "const", "continue", "default", "do", "double", "else",
                    "enum", "extern", "float", "for", "goto", "if", "int", "long", "register", "return", "short",
                    "signed", "sizeof", "static", "struct", "switch", "typedef", "union", "unsigned", "void",
                    "volatile", "while", "string", "class", "struct", "include"])
OPERATORS = set(["++", "--", "+", "-", "*", "/", "%", "=", "<", ">", "<=", ">="])
DELIMITERS = set(["[", "]", "(", ")", "{", "}", " ", "//", "/*", "*/" , "}", "'", '"', ";", ":"])
NUMERALS = set("0123456789")
GENERAL = set(["ERROR", "EOF", ])
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
}

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
    if not identifier.replace('_', '').isalnum():
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


def tokenize_and_categorize(input_program):
    # Create a list to store lexeme-token pairs
    lexeme_token_pairs = []

    # Initialize variables to keep track of the current position in the input_program
    current_pos = 0
    input_length = len(input_program)

    while current_pos < input_length:
        char = input_program[current_pos]

        # Skip whitespaces
        if char.isspace():
            current_pos += 1
            continue

        # Check for numeric literals
        if char.isdigit():
            numeral = ""
            while current_pos < input_length and input_program[current_pos].isdigit():
                numeral += input_program[current_pos]
                current_pos += 1
            lexeme_token_pairs.append((numeral, "NUMERAL"))

        else:
            # Check for lexemes in the token_d dictionary
            found_lexeme = False
            for lexeme, token in token_d.items():
                if input_program.startswith(lexeme, current_pos):
                    lexeme_token_pairs.append((lexeme, token))
                    current_pos += len(lexeme)
                    found_lexeme = True
                    break

            if not found_lexeme:
                # If none of the lexemes match, it might be an invalid character
                lexeme_token_pairs.append((char, "INVALID"))
                current_pos += 1

    # Print the table
    print("Lexeme\t\t\tToken\n")
    for lexeme, token in lexeme_token_pairs:
        print(f"{lexeme}\t\t\t{token}")

# Example usage
input_program = input("Enter Your Code: ")
tokenize_and_categorize(input_program)