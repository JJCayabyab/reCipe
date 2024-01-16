import glob
import os

class LexicalAnalyzer:
    KEYWORDS = frozenset(["INT", "BOOL", "CHAR", "DOUBLE", "MARIN", "SAVOR", "RELISH", 
                          "STIR","STR", "STRUCT", "FLOAT", "DO", "WHILE", "DIGEST", 
                          "MILD", "OMIT", "SPICY", "SWITCH", "CASE"])
    OPERATORS = frozenset({ "+", "-", "*", "/", "%", "=", "<", ">", "!"})
    DELIMITERS = frozenset(["[", "]", "(", ")", "{", "}", " ", "//", "#", "}", "'", '"', ";", ":"])
    NUMERALS = frozenset("0123456789")
    IDENTIFIERS = set()
    FLOAT_VAL = 7
    ID_VAL =31

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
        "SPICY": "TRUE_STM",
        # new features
        "createTable": "CREATE_TAB",
        "setCellValue": "SET_CELL_VAL",
        "printTable": "PRINT_TAB",
        "freeTable": "FREE_TAB",    
        "QuotientRem": "QUO_REM",
        "unitConvert": "UNIT_CONV"
    }
   
    @staticmethod
    def is_valid_identifier(identifier):
        # Rules for a valid identifier
        return (
            identifier.isidentifier()
            and (identifier[0].isalpha() or identifier[0] == '_')
            and identifier.lower() not in LexicalAnalyzer.KEYWORDS  # Convert to lowercase for case-insensitivity
            and ' ' not in identifier
            and len(identifier) <= LexicalAnalyzer.ID_VAL
            and all(char.isalnum() or char in ['_'] for char in identifier)
        )

    @staticmethod
    def tokenize_and_categorize(input_program):
        lexeme_token_pairs = []
        current_pos = 0
        input_length = len(input_program)

        while current_pos < input_length:
            char = input_program[current_pos]

            # For whitespace
            if char.isspace():
                current_pos += 1
                continue

            # Handle single-line comments using //
            if input_program[current_pos:current_pos + 2] == "//":
                current_pos = input_program.find('\n', current_pos)
                if current_pos == -1:
                    break
                continue

            # Handle multi-line comments using #
            elif char == '#':
                comment_end = input_program.find('#', current_pos + 1)
                if comment_end == -1:
                    print("Error: Unclosed multi-line comment.")
                    # Find the next newline character
                    current_pos = input_program.find('\n', current_pos)
                    if current_pos == -1:
                        break
                    continue

                # Check if there is another '#' before the found comment end
                next_comment_start = input_program.find('#', current_pos + 1)
                if next_comment_start != -1 and next_comment_start < comment_end:
                    print("Error: Nested multi-line comments are not allowed.")
                    current_pos = next_comment_start + 1
                    continue

                current_pos = comment_end + 1


            elif char == "'":
                # Handle single quotation character literal
                lexeme = char  # Start with the opening single quotation mark
                current_pos += 1
                while current_pos < input_length and input_program[current_pos] != "'":
                    lexeme += input_program[current_pos]
                    current_pos += 1
                lexeme += "'"  # Include the closing single quotation mark in the lexeme

                # Check if the lexeme contains exactly 1 character
                if len(lexeme) != 3:
                    lexeme_token_pairs.append((lexeme, "INVALID"))
                else:
                    lexeme_token_pairs.append((lexeme, "CHAR_LITERAL"))

                current_pos += 1  # Move past the closing single quotation mark
                
            elif char == '"':
                # Handle double quotation string literal
                lexeme = char  # Start with the opening double quotation mark
                current_pos += 1
                while current_pos < input_length and input_program[current_pos] != '"':
                    lexeme += input_program[current_pos]
                    current_pos += 1

                if current_pos < input_length and input_program[current_pos] == '"':
                    lexeme += '"'  # Include the closing double quotation mark in the lexeme
                    lexeme_token_pairs.append((lexeme, "STRING_LITERAL"))
                    current_pos += 1  # Move past the closing double quotation mark
                else:
                    lexeme_token_pairs.append((lexeme, "INVALID"))
            
            # check keywords
            elif char.isalpha() or char == '_':
                identifier = ""
                while current_pos < input_length and (
                        input_program[current_pos].isalnum() or input_program[current_pos] in ['_']):
                    identifier += input_program[current_pos]
                    current_pos += 1

                # Check if the identifier is a keyword, boolean literal, or reserved keyword
                if identifier.isupper() and identifier in LexicalAnalyzer.KEYWORDS:
                    lexeme_token_pairs.append((identifier, LexicalAnalyzer.token_d.get(identifier, "INVALID")))
                elif identifier.lower() == "true":
                    lexeme_token_pairs.append((identifier, "B_TRUE"))
                elif identifier.lower() == "false":
                    lexeme_token_pairs.append((identifier, "B_FALSE"))
                elif identifier.lower() in LexicalAnalyzer.KEYWORDS:  # Convert to lowercase for case-sensitivity
                    lexeme_token_pairs.append((identifier, LexicalAnalyzer.token_d.get(identifier.lower(), "INVALID")))
                elif LexicalAnalyzer.is_valid_identifier(identifier):
                    lexeme_token_pairs.append((identifier, "IDENTIFIER"))
                    LexicalAnalyzer.IDENTIFIERS.add(identifier)
                else:
                # Check if the identifier is one of the new function names
                    if identifier.lower() in LexicalAnalyzer.token_d:
                        lexeme_token_pairs.append((identifier, LexicalAnalyzer.token_d[identifier.lower()]))
                    else:
                        lexeme_token_pairs.append((identifier, "INVALID"))

            # digit / numbers
            elif char.isdigit():
                numeral = ""
                while current_pos < input_length and (input_program[current_pos].isdigit() or input_program[current_pos] == '.'):
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

            # compound operators
            elif char in LexicalAnalyzer.OPERATORS:
                # Handle unary and compound assignment operators without spaces
                lexeme, token = "", ""
                while current_pos < input_length and input_program[current_pos] in LexicalAnalyzer.OPERATORS:
                    lexeme += input_program[current_pos]
                    current_pos += 1

                if lexeme in LexicalAnalyzer.token_d:
                    token = LexicalAnalyzer.token_d[lexeme]
                elif len(lexeme) == 1:
                    token = LexicalAnalyzer.token_d.get(lexeme, "INVALID")

                lexeme_token_pairs.append((lexeme, token))

            else:
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
                        while current_pos < input_length and (
                                input_program[current_pos].isalnum() or input_program[current_pos] in ['_']):
                            invalid_token += input_program[current_pos]
                            current_pos += 1
                        lexeme_token_pairs.append((invalid_token, "INVALID"))
                    else:
                        # Invalid single character
                        lexeme_token_pairs.append((invalid_token, "INVALID"))

                    current_pos += 1  # Move to the next character to avoid an infinite loop

        # Move the return statement outside the while loop
        return lexeme_token_pairs

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

    # Determine the maximum length of lexemes for dynamic alignment
    max_lexeme_length = max(len(lexeme) for lexeme, _ in tokens)

    # Adjust the lexeme column width for reserved words and headers
    lexeme_column_width = max(max_lexeme_length, len("Lexeme"))

    # Adjust for reserved words in the lexeme_column_width calculation
    for reserved_word in lexer.KEYWORDS:
        lexeme_column_width = max(lexeme_column_width, len(reserved_word))

    # Add padding for better alignment
    lexeme_column_width += 5

    # Determine the maximum length of tokens for dynamic alignment
    max_token_length = max(len(token) for _, token in tokens)

    # Adjust the token column width for centered alignment
    token_column_width = max(max_token_length, len("Token"))
    
    # Add padding for better alignment
    token_column_width += 5

    # Save tokens to a table-like file with dynamic alignment
    output_file_path = f"{os.path.splitext(file_path)[0]}_lexer.txt"
    with open(output_file_path, 'w') as output_file:
        lexeme_header = f"Lexeme{'' : <{lexeme_column_width}}Token{'' : ^{token_column_width}}"
        output_file.write(f"{lexeme_header}\n")

        for lexeme, token in tokens:
            formatted_lexeme = f"{lexeme:<{lexeme_column_width}}"
            formatted_token = f"{token:^{token_column_width}}"
            output_file.write(f"{formatted_lexeme}{formatted_token}\n")

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
            # Continue to the next file if the current one is not found or empty