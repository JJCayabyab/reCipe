import glob
import os

class LexicalAnalyzer:
    KEYWORDS = frozenset(["INT", "BOOL", "CHAR", "DOUBLE", "MARIN", "SAVOR", "RELISH", 
                          "STIR","STR", "STRUCT", "FLOAT", "DO", "WHILE", "DIGEST", 
                          "MILD", "OMIT", "SPICY", "SWITCH", "CASE"])
    OPERATORS = frozenset({ "+", "-", "*", "/", "%", "=", "<", ">", "!"})
    DELIMITERS = frozenset(["[", "]", "(", ")", "{", "}", " ", "//", "#", "}", "'", '"', ";", ":"])
    NUMERALS = frozenset("0123456789")
    GENERAL = frozenset(["ERROR", "EOF"])
    IDENTIFIERS = set()
    FLOAT_VAL = 7
    ID_VAL = 31

    token_d = {
        # keywords
        "INT": "DT_INT",
        "CHAR": "DT_CHAR",
        "FLOAT": "DT_FLOAT",
        "DOUBLE": "DT_DOUBLE",
        "IF": "IF_STM",
        "SAVOR": "ELSE_STM",
        "STIR": "LP_STM",
        "BOOL": "DT_BOOL",
        "STR": "DT_STR",
        "STRUCT": "DT_STRUCT",
        "DO": "DO_STM",
        "WHILE": "WHILE_STM",
        # operators
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
        # delimiters
        ";": "SEMICOLON",
        "(": "LPAREN",
        ")": "RPAREN",
        "[": "LBRAC",
        "]": "RBRAC",
        "{": "LCURLBRAC",
        "}": "RCURLBRAC",
        "//": "SINGLE_COM",
        "#": "MULTI_COM",
        " ": "SPACE",
        "'": "SQOUT",
        '"': "DQOUT",
        ":": "COLON",
        ",": "COM",
        # reserved words
        "DIGEST": "BREAK_STM",
        "MILD": "FALSE_STM",
        "OMIT": "CONTINUE_STM",
        "RELISH": "ELSE_STM",
        "SPICY": "TRUE_STM"
    }
   
    @staticmethod
    def is_valid_identifier(identifier):
        # Rules for a valid identifier
        return (
            identifier.isidentifier()
            and (identifier[0].isalpha() or identifier[0] == '_')
            and identifier.upper() not in LexicalAnalyzer.KEYWORDS
            and ' ' not in identifier
            and len(identifier) <= LexicalAnalyzer.ID_VAL
            and all(char.isalnum() or char in ['_'] for char in identifier)
        )
    
    @staticmethod
    def handle_whitespace(input_program, current_pos):
        while current_pos < len(input_program) and input_program[current_pos].isspace():
            current_pos += 1
        return current_pos

    @staticmethod
    def handle_single_line_comment(input_program, current_pos):
        return input_program.find('\n', current_pos) if current_pos != -1 else current_pos

    @staticmethod
    def handle_multi_line_comment(input_program, current_pos):
        return input_program.find('#', current_pos + 1) + 1 if current_pos != -1 else current_pos

    @staticmethod
    def handle_character_literal(input_program, current_pos, lexeme_token_pairs):
        lexeme = "'"  # Start with the opening single quotation mark
        current_pos += 1
        while current_pos < len(input_program) and input_program[current_pos] != "'":
            lexeme += input_program[current_pos]
            current_pos += 1
        lexeme += "'"  # Include the closing single quotation mark in the lexeme

        # Check if the lexeme contains exactly 1 character
        if len(lexeme) != 3:
            lexeme_token_pairs.append((lexeme, "INVALID"))
        else:
            lexeme_token_pairs.append((lexeme, "CHAR_LITERAL"))

        return current_pos + 1  # Move past the closing single quotation mark


    @staticmethod
    def handle_string_literal(input_program, current_pos, lexeme_token_pairs):
        lexeme = '"'  # Start with the opening double quotation mark
        current_pos += 1
        while current_pos < len(input_program) and input_program[current_pos] != '"':
            lexeme += input_program[current_pos]
            current_pos += 1

        if current_pos < len(input_program) and input_program[current_pos] == '"':
            lexeme += '"'  # Include the closing double quotation mark in the lexeme
            lexeme_token_pairs.append((lexeme, "STRING_LITERAL"))
            current_pos += 1  # Move past the closing double quotation mark
        else:
            lexeme_token_pairs.append((lexeme, "INVALID"))

        return current_pos


    @staticmethod
    def handle_reserved_keywords_and_identifiers(input_program, current_pos, lexeme_token_pairs):
        identifier = ""
        while current_pos < len(input_program) and (
                input_program[current_pos].isalnum() or input_program[current_pos] in ['_']):
            identifier += input_program[current_pos]
            current_pos += 1

        # Check if the identifier is a keyword, boolean literal, or reserved keyword
        if identifier.upper() in LexicalAnalyzer.KEYWORDS:
            lexeme_token_pairs.append((identifier, LexicalAnalyzer.token_d.get(identifier.upper(), "INVALID")))
        elif identifier.lower() == "true":
            lexeme_token_pairs.append((identifier, "B_TRUE"))
        elif identifier.lower() == "false":
            lexeme_token_pairs.append((identifier, "B_FALSE"))
        elif identifier.upper() in LexicalAnalyzer.token_d:
            lexeme_token_pairs.append((identifier, LexicalAnalyzer.token_d.get(identifier.upper(), "INVALID")))
        elif LexicalAnalyzer.is_valid_identifier(identifier):
            lexeme_token_pairs.append((identifier, "IDENTIFIER"))
            LexicalAnalyzer.IDENTIFIERS.add(identifier)
        else:
            lexeme_token_pairs.append((identifier, "INVALID"))

        return current_pos


    @staticmethod
    def handle_numerals(input_program, current_pos, lexeme_token_pairs):
        numeral = ""
        while current_pos < len(input_program) and (input_program[current_pos].isdigit() or input_program[current_pos] == '.'):
            numeral += input_program[current_pos]
            current_pos += 1

        if '.' in numeral:
            # Check for float or double based on the number of decimal places
            num_parts = numeral.split('.')
            decimal_places = len(num_parts[1]) if len(num_parts) > 1 else 0

            if decimal_places <= LexicalAnalyzer.FLOAT_VAL:
                lexeme_token_pairs.append((numeral, "FLOAT_LITERAL"))
            else:
                lexeme_token_pairs.append((numeral, "DOUBLE_LITERAL"))
        else:
            lexeme_token_pairs.append((numeral, "INTEGER_LITERAL"))

        return current_pos


    @staticmethod
    def handle_compound_operators(input_program, current_pos, lexeme_token_pairs):
        lexeme, token = "", ""
        while current_pos < len(input_program) and input_program[current_pos] in LexicalAnalyzer.OPERATORS:
            lexeme += input_program[current_pos]
            current_pos += 1

        if lexeme in LexicalAnalyzer.token_d:
            token = LexicalAnalyzer.token_d[lexeme]
        elif len(lexeme) == 1:
            token = LexicalAnalyzer.token_d.get(lexeme, "INVALID")

        lexeme_token_pairs.append((lexeme, token))
        return current_pos


    @staticmethod
    def handle_unknown_tokens(input_program, current_pos, lexeme_token_pairs):
        found_lexeme = False

        for lexeme, token in LexicalAnalyzer.token_d.items():
            if input_program.startswith(lexeme, current_pos):
                lexeme_token_pairs.append((lexeme, token))
                current_pos += len(lexeme)
                found_lexeme = True
                break

        if not found_lexeme:
            # If the character is not a valid lexeme, consider it as an invalid token
            invalid_token = input_program[current_pos]
            if invalid_token.isalpha() or invalid_token == '_':
                # Invalid identifier character
                while current_pos < len(input_program) and (
                        input_program[current_pos].isalnum() or input_program[current_pos] in ['_']):
                    invalid_token += input_program[current_pos]
                    current_pos += 1
                lexeme_token_pairs.append((invalid_token, "INVALID"))
            else:
                # Invalid single character
                lexeme_token_pairs.append((invalid_token, "INVALID"))

            current_pos += 1  # Move to the next character to avoid an infinite loop

        return current_pos + 1
    
    @staticmethod
    def tokenize_and_categorize(input_program):
        lexeme_token_pairs = []
        current_pos = 0
        input_length = len(input_program)

        while current_pos < input_length:
            char = input_program[current_pos]

            if char.isspace():
                current_pos = LexicalAnalyzer.handle_whitespace(input_program, current_pos)
            elif input_program[current_pos:current_pos + 2] == "//":
                current_pos = LexicalAnalyzer.handle_single_line_comment(input_program, current_pos)
            elif char == '#':
                current_pos = LexicalAnalyzer.handle_multi_line_comment(input_program, current_pos)
            elif char == "'":
                current_pos = LexicalAnalyzer.handle_character_literal(input_program, current_pos, lexeme_token_pairs)
            elif char == '"':
                current_pos = LexicalAnalyzer.handle_string_literal(input_program, current_pos, lexeme_token_pairs)
            elif char.isalpha() or char == '_':
                current_pos = LexicalAnalyzer.handle_reserved_keywords_and_identifiers(input_program, current_pos, lexeme_token_pairs)
            elif char.isdigit():
                current_pos = LexicalAnalyzer.handle_numerals(input_program, current_pos, lexeme_token_pairs)
            elif char in LexicalAnalyzer.OPERATORS:
                current_pos = LexicalAnalyzer.handle_compound_operators(input_program, current_pos, lexeme_token_pairs)
            else:
                current_pos = LexicalAnalyzer.handle_unknown_tokens(input_program, current_pos, lexeme_token_pairs)

        return lexeme_token_pairs


# Constants
FILE_EXTENSION = ".ipe"

def process_file(file_path):
    try:
        with open(file_path, 'r') as file:
            input_program = file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")

    if not input_program:
        raise ValueError(f"File {file_path} is empty. Please provide valid code.")

    lexer = LexicalAnalyzer()
    tokens = lexer.tokenize_and_categorize(input_program)

    # Save tokens to a table-like file
    output_file_path = f"{os.path.splitext(file_path)[0]}_lexer.txt"
    with open(output_file_path, 'w') as output_file:
        output_file.write("Lexeme{:>50}Token\n".format(''))
        for lexeme, token in tokens:
            output_file.write(f"{lexeme:<50}{token}\n")

    print(f"Tokens saved to: {output_file_path}")

if __name__ == "__main__":
    files_with_extension = glob.glob(f"*{FILE_EXTENSION}")

    if not files_with_extension:
        print(f"No files found with '{FILE_EXTENSION}' extension.")
        exit()

    for file_path in files_with_extension:
        try:
            process_file(file_path)
        except (FileNotFoundError, ValueError) as e:
            print(f"Error: {e}")
            # Continue to the next file if the current one is not
