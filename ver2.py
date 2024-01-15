class LexicalAnalyzer:
    KEYWORDS = frozenset(["auto", "break", "case", "char", "const", "continue", "default", "do", "double", "else",
                          "enum", "extern", "float", "for", "goto", "if", "int", "long", "register", "return", "short",
                          "signed", "sizeof", "static", "struct", "switch", "typedef", "union", "unsigned", "void",
                          "volatile", "while", "string", "class", "struct", "include", "printf", "return"])
    OPERATORS = frozenset({ "+", "-", "*", "/", "%", "=", "<", ">", "!"})
    DELIMITERS = frozenset(["[", "]", "(", ")", "{", "}", " ", "//", "#", "}", "'", '"', ";", ":"])
    NUMERALS = frozenset("0123456789")
    GENERAL = frozenset(["ERROR", "EOF"])
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
        "//": "SINGLE_COM",
        "#": "MULTI_COM",
        " ": "SPACE",
        "'": "SQOUT",
        '"': "DQOUT",
        ":": "COLON",
        ",": "COM",
}
   
    @staticmethod
    def is_valid_identifier(identifier):
    # Rules for a valid identifier
        return (
            identifier.isidentifier()
            and (identifier[0].isalpha() or identifier[0] == '_')
            and identifier.lower() not in LexicalAnalyzer.KEYWORDS  # Check if the lowercase version is a keyword
            and ' ' not in identifier
            and len(identifier) <= 31  # Check maximum length
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

            # Handle single-line comments
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
                    break
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
                lexeme += '"'  # Include the closing double quotation mark in the lexeme
                lexeme_token_pairs.append((lexeme, "STRING_LITERAL"))
                current_pos += 1  # Move past the closing double quotation mark

            elif char == "@":
                identifier = ""
                current_pos += 1  # Move past the "@"
                while current_pos < input_length and (
                        input_program[current_pos].isalnum() or input_program[current_pos] in ['-', '_']):
                    identifier += input_program[current_pos]
                    current_pos += 1
                lexeme_token_pairs.append((f"@{identifier}", "IDENTIFIER"))

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
                    if decimal_places <= 7:
                        lexeme_token_pairs.append((numeral, "FLOAT_LITERAL"))
                    else:
                        lexeme_token_pairs.append((numeral, "DOUBLE_LITERAL"))
                else:
                    lexeme_token_pairs.append((numeral, "INTEGER_LITERAL"))

            elif char.isalpha() or char == '_':
                identifier = ""
                while current_pos < input_length and (
                        input_program[current_pos].isalnum() or input_program[current_pos] in ['_']):
                    identifier += input_program[current_pos]
                    current_pos += 1

                # Check if the identifier is a keyword or boolean literal
                if identifier.lower() in LexicalAnalyzer.KEYWORDS:
                     lexeme_token_pairs.append((identifier, LexicalAnalyzer.token_d.get(identifier.lower(), "INVALID")))
                     current_pos += 1  # Add this line to skip the blank space after a keyword
                elif identifier.lower() == "true":
                    lexeme_token_pairs.append((identifier, "B_TRUE"))
                elif identifier.lower() == "false":
                    lexeme_token_pairs.append((identifier, "B_FALSE"))
                elif identifier.lower() == "bool":
                    lexeme_token_pairs.append((identifier, "DT_BOOL"))
                elif LexicalAnalyzer.is_valid_identifier(identifier):
                    lexeme_token_pairs.append((identifier, "IDENTIFIER"))
                    LexicalAnalyzer.IDENTIFIERS.add(identifier)
                else:
                    lexeme_token_pairs.append((identifier, "INVALID"))
                    
            #compound operators
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

if __name__ == "__main__":
    file_path = "sample.ipe"  # Change this to the desired file name
    try:
        with open(file_path, 'r') as file:
            input_program = file.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        exit()

    if not input_program:
        print("File is empty. Please provide valid code.")
    else:
        lexer = LexicalAnalyzer()
        tokens = lexer.tokenize_and_categorize(input_program)

        # Save tokens to a table-like file
        output_file_path = "tokens_output.txt"  # Change this to the desired output file name

        with open(output_file_path, 'w') as output_file:
            output_file.write("Lexeme\t\t\t\t\tToken\n")
            for lexeme, token in tokens:
                output_file.write(f"{lexeme.ljust(30)}{token}\n")

        print(f"Tokens saved to: {output_file_path}")