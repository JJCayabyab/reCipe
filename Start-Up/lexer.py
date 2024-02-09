from token_dict import KD, OD, DD, RD

KEYWORDS = frozenset(["INT", "BOOL", "CHAR", "DOUBLE", "CONST", "IF", "ELSE", 
                          "FOR","STR", "STRUCT", "FLOAT", "DO", "WHILE", "BREAK", 
                          "FALSE", "CONT", "TRUE", "PICK", "CASE", "START", "END",
                          "DISPLAY", "GET", "QUOTIENTREM", "UNITCONVERT","TABLE", 
                          "CREATETABLE", "SETCELLVALUE", "DISPLAYTABLE", "FREETABLE"])
OPERATORS = frozenset({ "+", "-", "*", "/", "%", "=", "<", ">", "!"})
DELIMITERS = frozenset(["[", "]", "(", ")", "{", "}", " ", "//", "#", "}", "'", '"', ";", ":", "<<", ">>", "@"])
NUMERALS = frozenset("0123456789")
IDENTIFIERS = set()
FLOAT_VAL = 7
DOUBLE_VAL = 15
ID_VAL = 31
token_d = {**KD, **OD, **DD, **RD}

class LexicalAnalyzer:
   
    @staticmethod
    def is_valid_identifier(identifier):
        # Rules for a valid identifier
        return (
            identifier.isidentifier()
            and (identifier[0].isalpha() or identifier[0] == '_')
            and identifier.lower() not in KEYWORDS  
            and ' ' not in identifier
            and len(identifier) <= ID_VAL
            and all(char.isalnum() or char in ['_'] for char in identifier)
        )

    @staticmethod
    def tokenize_and_categorize(input_program): # tokenize the input code
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
                comment_end = input_program.find('\n', current_pos)
                if comment_end == -1:
                    comment_end = input_length  
                lexeme = input_program[current_pos:comment_end]
                lexeme_token_pairs.append((lexeme, "SC"))
                current_pos = comment_end
                continue

            # Handle multi-line comments using #
            elif char == '#':
                comment_end = input_program.find('#', current_pos + 1)
                if comment_end == -1:
                    print("Error: Unclosed multi-line comment.")
                    current_pos = input_program.find('\n', current_pos)
                    if current_pos == -1:
                        break
                    continue

                lexeme = input_program[current_pos:comment_end + 1]
                lexeme_token_pairs.append((lexeme, "MC"))
                current_pos = comment_end + 1
                continue
            
            # Handle character literal
            elif char == "'":
                lexeme = char  
                current_pos += 1

                if current_pos < input_length and input_program[current_pos] != "'":
                    lexeme += input_program[current_pos]
                    current_pos += 1

                    if current_pos < input_length and input_program[current_pos] == "'":
                        lexeme += "'"
                        current_pos += 1

                        if len(lexeme) == 3:
                            lexeme_token_pairs.append((lexeme, "CL"))
                        else:
                            lexeme_token_pairs.append((lexeme, "INVALID"))
                    else:
                        lexeme_token_pairs.append((lexeme, "INVALID"))
                else:
                    lexeme_token_pairs.append((lexeme, "INVALID"))
                    
            # Handles string literal 
            elif char == '"':
                lexeme = char 
                current_pos += 1
                while current_pos < input_length and input_program[current_pos] != '"':
                    lexeme += input_program[current_pos]
                    if input_program[current_pos:current_pos + 2] == "\\n":
                        lexeme_token_pairs.append(("\\n", "E_N")) 
                        current_pos += 1
                    elif input_program[current_pos:current_pos + 2] == "\\t":
                        lexeme_token_pairs.append(("\\t", "E_T"))  #
                        current_pos += 1  
                    elif input_program[current_pos] == '@':
                        lexeme_token_pairs.append(('@', "PH"))  
                    current_pos += 1

                if current_pos < input_length and input_program[current_pos] == '"':
                    lexeme += '"'  
                    lexeme_token_pairs.append((lexeme, "SL"))
                    current_pos += 1  
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
                if identifier.isupper() and identifier in KEYWORDS:
                    lexeme_token_pairs.append((identifier, token_d.get(identifier, "INVALID")))
                elif identifier.lower() == "true":
                    lexeme_token_pairs.append((identifier, "T"))
                elif identifier.lower() == "false":
                    lexeme_token_pairs.append((identifier, "F"))
                elif identifier.lower() in KEYWORDS:  # Convert to lowercase for case-sensitivity
                    lexeme_token_pairs.append((identifier, token_d.get(identifier.lower(), "INVALID")))
                elif LexicalAnalyzer.is_valid_identifier(identifier):
                    lexeme_token_pairs.append((identifier, "ID"))
                    IDENTIFIERS.add(identifier)
                else:
                # Check if the identifier is one of the new function names
                    if identifier.lower() in token_d:
                        lexeme_token_pairs.append((identifier, token_d[identifier.lower()]))
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

                        if decimal_places <= FLOAT_VAL:
                            lexeme_token_pairs.append((numeral, "FL"))
                        elif decimal_places <= DOUBLE_VAL:
                            lexeme_token_pairs.append((numeral, "DL"))
                else:
                    lexeme_token_pairs.append((numeral, "IL"))
            
            # compound operators
            elif char in OPERATORS:
                # Handle unary and compound assignment operators without spaces
                lexeme, token = "", ""
                while current_pos < input_length and input_program[current_pos] in OPERATORS:
                    lexeme += input_program[current_pos]
                    current_pos += 1

                # Check if lexeme is in the dictionary, otherwise mark it as "INVALID"
                token = token_d.get(lexeme, "INVALID")
                lexeme_token_pairs.append((lexeme, token))

            else:
                found_lexeme = False
                for lexeme, token in token_d.items():
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

        return lexeme_token_pairs
