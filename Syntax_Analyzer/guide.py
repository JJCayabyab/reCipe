class Parser:
    def __init__(self, tokens=None):
        self.tokens = tokens or []
        self.index = 0

    def read_tokens_from_file(self, filename):
        with open(filename, "r") as f:
            tokens = []
            for line in f:
                for token in line.strip().split():
                    if token.isalpha():  # Check if the token is a variable name
                        tokens.append(token)
            self.tokens = tokens

    def match(self, token_type):
        if self.current_token() == token_type:
            self.index += 1
        else:
            self.error()

    def current_token(self):
        return self.tokens[self.index] if self.index < len(self.tokens) else None

    def error(self):
        raise SyntaxError(f"Unexpected token at index {self.index}: {self.current_token()}")

    def parse(self):
        while self.current_token() is not None:
            self.declaration_statement()

    def declaration_statement(self):
        data_type = self.data_type()
        identifiers = self.identifier()
        while self.current_token() == ",":
            self.match(",")
            identifiers.append(self.identifier())
        self.match(";")

    def data_type(self):
        data_type = self.current_token()
        self.match(data_type)
        return data_type

    def identifier(self):
        identifier = []
        while self.current_token() in ["x", "y", "z", "w", "a", "b", "c", "d"]:
            identifier.append(self.current_token())
            self.match(self.current_token())
        return identifier
    
    def input_statement(self):
        if self.current_token() == "GET":
            self.match("GET")
            self.match("(")
            self.identifier_list()
            self.match(")")
            self.match(";")
        else:
            self.assignment_statement()
            self.match(";")
    def identifier_list(self):
        identifiers = self.identifier()
        while self.current_token() == ",":
            self.match(",")
            identifiers.append(self.identifier())
        self.match("=")
        self.match("GET")
        self.match("(")
        self.match(")")
        self.match(";")
        self.assignment_statement()

    def assignment_statement(self):
        identifiers = self.identifier()
        self.match("=")
        self.value()
        while self.current_token() == ",":
            self.match(",")
            identifiers.append(self.identifier())
        self.match(";")

    def identifier(self):
        identifier = []
        while self.current_token() in ["x", "y", "z", "w", "a", "b", "c", "d", "_"]:
            identifier.append(self.current_token())
            self.match(self.current_token())
        return identifier

    def value(self):
        if self.current_token().isdigit():
            self.match(self.current_token())
        elif self.current_token().startswith("\""):
            self.match(self.current_token())
        elif self.current_token() in ["GET", "=", ",", "@", ":", "\"", "_"]:
            self.match(self.current_token())
        else:
            self.identifier()
            
    def function_call(self):
        self.match("(")
        self.match("GET")
        self.match("(")
        self.match(")")

    def string(self):
        chars = []
        while self.current_token() != ")":
            chars.append(self.current_token())
            self.match(self.current_token())
        self.match(")")
        return "".join(chars)

# Test the parser
parser = Parser()
parser.read_tokens_from_file("test.txt")
parser.parse()