def tokenize_and_categorize(input_program):
    # Define dictionaries for different token types
    keyword_mapping = {
        "int": "DT_INT",
        "char": "DT_CHAR",
        "float": "DT_FLOAT",
        "double": "DT_DOUBLE",
        "if": "IF_STM",
        "else": "ELSE_STM",
        "for": "LP_STM",
        "while": "WHILE_STM",
        "do": "DO_STM",
        # ... add more keywords
    }

    operator_mapping = {
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
        # ... add more operators
    }

    special_characters_mapping = {
        ";": "SPECIAL_CHAR",
        "(": "LPAREN",
        ")": "RPAREN",
        "[": "LBRAC",
        "]": "RBRAC",
        "{": "LCURLBRAC",
        "}": "RCURLBRAC",
        "//": "COMMENT",
        "/*": "MULTI_COMMENT",
        "*/": "MULTI_COMMENT",
        "'": "SQOUT",
        '"': "DQOUT",
        # ... add more special characters
    }

    # Create a list to store lexeme-token pairs
    lexeme_token_pairs = []

    # Initialize variables
    current_lexeme = ""
    in_comment_block = False

    # Categorize the input characters
    for char in input_program:
        if in_comment_block:
            # Check for the end of a multi-line comment
            if current_lexeme.endswith("*/"):
                current_lexeme = ""
                in_comment_block = False
            continue

        # Handle comment detection
        if current_lexeme.endswith("//"):
            current_lexeme = current_lexeme[:-2]  # Remove "//" from the lexeme
            break

        # Update lexeme based on the current character
        current_lexeme += char

        # Check if the current lexeme is a complete token
        if current_lexeme.strip() in keyword_mapping:
            lexeme_token_pairs.append((current_lexeme.strip(), keyword_mapping[current_lexeme.strip()]))
            current_lexeme = ""
        elif current_lexeme.strip() in operator_mapping:
            lexeme_token_pairs.append((current_lexeme.strip(), operator_mapping[current_lexeme.strip()]))
            current_lexeme = ""
        elif current_lexeme.strip() in special_characters_mapping:
            lexeme_token_pairs.append((current_lexeme.strip(), special_characters_mapping[current_lexeme.strip()]))
            current_lexeme = ""

        # Check for the start of a multi-line comment
        elif current_lexeme.endswith("/*"):
            in_comment_block = True

    # Print the table
    print("{:<15}{}".format("Lexeme", "Token"))
    for lexeme, token in lexeme_token_pairs:
        print("{:<15}{}".format(lexeme, token))

# Example usage
input_program = input("Enter Your Code: ")
tokenize_and_categorize(input_program)
