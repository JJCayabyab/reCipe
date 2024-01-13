class LexicalAnalyzer:
    def __init__(self):
        # Token row
        self.lin_num = 1

    def tokenize(self, code):
        rules = [
            ('MAIN', 'main'),          # main
            ('INT', 'int'),            # int
            ('FLOAT', 'float'),        # float
            ('IF', 'if'),              # if
            ('ELSE', 'else'),          # else
            ('WHILE', 'while'),        # while
            ('READ', 'read'),          # read
            ('PRINT', 'print'),        # print
            ('LBRACKET', r'\('),        # (
            ('RBRACKET', r'\)'),        # )
            ('LBRACE', r'\{'),          # {
            ('RBRACE', r'\}'),          # }
            ('COMMA', r','),            # ,
            ('PCOMMA', r';'),           # ;
            ('EQ', r'=='),              # ==
            ('NE', r'!='),              # !=
            ('LE', r'<='),              # <=
            ('GE', r'>='),              # >=
            ('OR', r'\|\|'),            # ||
            ('AND', r'&&'),             # &&
            ('ATTR', r'\='),            # =
            ('LT', r'<'),               # <
            ('GT', r'>'),               # >
            ('PLUS', r'\+'),            # +
            ('MINUS', r'-'),            # -
            ('MULT', r'\*'),            # *
            ('DIV', r'\/'),             # /
            ('ID', r'[a-zA-Z]\w*'),     # IDENTIFIERS
            ('FLOAT_CONST', r'\d(\d)*\.\d(\d)*'),   # FLOAT
            ('INTEGER_CONST', r'\d(\d)*'),          # INT
            ('NEWLINE', r'\n'),         # NEW LINE
            ('SKIP', r'[ \t]+'),        # SPACE and TABS
        ]

        tokens = []
        lexemes = []
        rows = []
        columns = []

        i = 0
        while i < len(code):
            match = None
            for token_type, pattern in rules:
                if code[i:].startswith(pattern):
                    match = (token_type, code[i:i+len(pattern)])
                    break

            if match:
                token_type, token_lexeme = match
                if token_type == 'NEWLINE':
                    self.lin_num += 1
                    i += 1  # Skip newline character
                elif token_type != 'SKIP':
                    col = i
                    row = self.lin_num
                    tokens.append(token_type)
                    lexemes.append(token_lexeme)
                    rows.append(row)
                    columns.append(col)
                    # To print information about a Token
                    print('Token = {0}, Lexeme = \'{1}\', Row = {2}, Column = {3}'.format(token_type, token_lexeme, row, col))

                i += len(token_lexeme)
            else:
                raise RuntimeError('%r unexpected on line %d' % (code[i], self.lin_num))
                i += 1

        return tokens, lexemes, rows, columns

# Example usage:
code = """
main {
    int x = 10;
    float y = 20.5;
    if (x > y) {
        print("x is greater than y");
    } else {
        print("y is greater than x");
    }
}
"""

lexer = LexicalAnalyzer()
lexer.tokenize(code)
