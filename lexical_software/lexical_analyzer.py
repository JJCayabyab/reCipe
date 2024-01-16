from tokens_dictionary import DICTIONARY

class LexicalAnalyzer:
    KEYWORDS = frozenset(["INT", "BOOL", "CHAR", "DOUBLE", "MARIN", "SAVOR", "RELISH", 
                          "STIR","STR", "STRUCT", "FLOAT", "DO", "WHILE", "DIGEST", 
                          "MILD", "OMIT", "SPICY", "SWITCH", "CASE"])
    OPERATORS = frozenset({ "+", "-", "*", "/", "%", "=", "<", ">", "!"})
    DELIMITERS = frozenset(["[", "]", "(", ")", "{", "}", " ", "//", "#", "}", "'", '"', ";", ":"])
    NUMERALS = frozenset("0123456789")
    IDENTIFIERS = set()
    FLOAT_VAL = 7
    DOUBLE_VAL = 15
    ID_VAL =31
    token_d = DICTIONARY
    
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
                            lexeme_token_pairs.append((numeral, "FLOAT_VAL"))
                        elif decimal_places <= LexicalAnalyzer.DOUBLE_VAL:
                            lexeme_token_pairs.append((numeral, "DOUBLE_VAL"))
                else:
                    lexeme_token_pairs.append((numeral, "INTEGER_VAL"))

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