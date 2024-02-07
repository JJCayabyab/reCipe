class Token:
    # Define token types as class attributes
    INT, FLOAT, BOOL, SEMI, LCBRACK, ID, IF, WHILE, PRINT, END_OF_FILE, MAIN, LPAREN, RPAREN, RCBRACK, EQ_EQ, NEQ, GT, GTEQ, LT, LTEQ, PLUS, MINUS, TIMES, DIV, MOD, NOT, POWER, OR, AND, EQ = range(30)

    def __init__(self, token_type, value=None, line=None):
        self.type = token_type
        self.value = value
        self.line = line

    def __repr__(self):
        return f"Token({self.type}, {self.value}, {self.line})"


class Lexer:
    def __init__(self):
        self.keywords = {'int', 'float', 'bool', 'main', 'if', 'else', 'while', 'print', 'true', 'false'}

    def token_generator(self, filename):
        with open(filename, 'r') as file:
            for line_num, line in enumerate(file, 1):
                tokens = line.split()
                for token in tokens:
                    if token.isdigit():
                        yield Token(Token.INT, int(token), line_num)
                    elif token.replace('.', '', 1).isdigit():
                        yield Token(Token.FLOAT, float(token), line_num)
                    elif token.lower() in self.keywords:
                        yield Token(getattr(Token, token.upper()), token.lower(), line_num)
                    else:
                        yield Token(Token.ID, token, line_num)
                yield Token(Token.SEMI, ';', line_num)
        yield Token(Token.END_OF_FILE, None, line_num)


class ASTNode:
    pass


class Program(ASTNode):
    def __init__(self, declarations, statements):
        self.declarations = declarations
        self.statements = statements

    def __repr__(self):
        return f"Program({self.declarations}, {self.statements})"


class Declaration(ASTNode):
    def __init__(self, type_, ident):
        self.type = type_
        self.ident = ident

    def __repr__(self):
        return f"Declaration({self.type}, {self.ident})"


class Statement(ASTNode):
    pass


class Block(ASTNode):
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Block({self.statements})"


class Assignment(ASTNode):
    def __init__(self, ident, expr):
        self.ident = ident
        self.expr = expr

    def __repr__(self):
        return f"Assignment({self.ident}, {self.expr})"


class IfStatement(ASTNode):
    def __init__(self, expr, if_stmt, else_stmt=None):
        self.expr = expr
        self.if_stmt = if_stmt
        self.else_stmt = else_stmt

    def __repr__(self):
        return f"IfStatement({self.expr}, {self.if_stmt}, {self.else_stmt})"


class WhileStatement(ASTNode):
    def __init__(self, expr, stmt):
        self.expr = expr
        self.stmt = stmt

    def __repr__(self):
        return f"WhileStatement({self.expr}, {self.stmt})"


class PrintStatement(ASTNode):
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return f"PrintStatement({self.expr})"


class Expr(ASTNode):
    pass


class OpExpr(Expr):
    def __init__(self, left, right, op):
        self.left = left
        self.right = right
        self.op = op

    def __repr__(self):
        return f"OpExpr({self.left}, {self.right}, '{self.op}')"


class NegExpr(Expr):
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return f"NegExpr({self.expr})"


class NotExpr(Expr):
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return f"NotExpr({self.expr})"


class Ident(Expr):
    def __init__(self, ident):
        self.ident = ident

    def __repr__(self):
        return f"Ident('{self.ident}')"


class IntLit(Expr):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"IntLit({self.value})"


class FloatLit(Expr):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"FloatLit({self.value})"


class TrueExpr(Expr):
    def __repr__(self):
        return "TrueExpr()"


class FalseExpr(Expr):
    def __repr__(self):
        return "FalseExpr()"


class Parser:
    type_first = {Token.INT, Token.FLOAT, Token.BOOL}
    stmt_first = {Token.SEMI, Token.LCBRACK, Token.ID, Token.IF, Token.WHILE, Token.PRINT}
    EquOp_first = {Token.EQ_EQ, Token.NEQ}
    RelOp_first = {Token.GT, Token.GTEQ, Token.LT, Token.LTEQ}
    addOp_first = {Token.PLUS, Token.MINUS}
    mulOp_first = {Token.TIMES, Token.DIV, Token.MOD}
    unaryOp_first = {Token.NOT, Token.MINUS}

    def __init__(self, filename):
        self.lexer = Lexer()
        self.lex = self.lexer.token_generator(filename)
        self.curr_tok = next(self.lex)

    def parse(self):
        prog = self.program()
        if self.curr_tok.type != Token.END_OF_FILE:
            raise Exception("Extra symbols in input")
        return prog

    def program(self):
        if self.curr_tok.type != Token.INT:
            self.syntax_error("'int' expected")
        self.match(Token.INT)

        if self.curr_tok.type != Token.MAIN:
            self.syntax_error("'main' expected")
        self.match(Token.MAIN)

        self.match(Token.LPAREN)
        self.match(Token.RPAREN)
        self.match(Token.LCBRACK)

        decls = self.declarations()
        stmts = self.statements()

        self.match(Token.RCBRACK)
        return Program(decls, stmts)

    def match(self, expected_token_type):
        if self.curr_tok.type != expected_token_type:
            self.syntax_error(f"'{Token.__dict__.get(expected_token_type)}' expected")
        self.curr_tok = next(self.lex)

    def syntax_error(self, message):
        print(f"Syntax Error: {message}, found {Token.__dict__.get(self.curr_tok.type)} on line {self.curr_tok.line}")
        exit(1)

    def declarations(self):
        decls = dict()
        while self.curr_tok.type in Parser.type_first:
            decl = self.declaration()
            decls[decl.ident] = decl
        return decls

    def declaration(self):
        type_ = self.type_()
        self.match(Token.SEMI)
        return Declaration(type_, self.curr_tok.value)

    def type_(self):
        if self.curr_tok.type in Parser.type_first:
            type_ = self.curr_tok.type
            self.curr_tok = next(self.lex)
        else:
            self.syntax_error("'int', 'bool', or 'float' expected")
        if self.curr_tok.type != Token.ID:
            self.syntax_error("identifier expected")
        ident = self.curr_tok.value
        self.curr_tok = next(self.lex)
        return type_

    def statements(self):
        stmts = []
        while self.curr_tok.type in Parser.stmt_first:
            stmts.append(self.statement())
        return stmts

    def statement(self):
        if self.curr_tok.type == Token.SEMI:
            self.match(Token.SEMI)
            return Statement()
        elif self.curr_tok.type == Token.LCBRACK:
            return self.block()
        elif self.curr_tok.type == Token.ID:
            return self.assignment()
        elif self.curr_tok.type == Token.IF:
            return self.ifStatement()
        elif self.curr_tok.type == Token.WHILE:
            return self.whileStatement()
        elif self.curr_tok.type == Token.PRINT:
            return self.printStatement()

    def block(self):
        self.match(Token.LCBRACK)
        stmts = self.statements()
        self.match(Token.RCBRACK)
        return Block(stmts)

    def assignment(self):
        ident = self.curr_tok.value
        self.match(Token.ID)
        self.match(Token.EQ)
        expr = self.expr()
        self.match(Token.SEMI)
        return Assignment(ident, expr)

    def ifStatement(self):
        self.match(Token.IF)
        self.match(Token.LPAREN)
        expr = self.expr()
        self.match(Token.RPAREN)
        if_stmt = self.statement()
        else_stmt = None
        if self.curr_tok.type == Token.ELSE:
            self.match(Token.ELSE)
            else_stmt = self.statement()
        return IfStatement(expr, if_stmt, else_stmt)

    def whileStatement(self):
        self.match(Token.WHILE)
        self.match(Token.LPAREN)
        expr = self.expr()
        self.match(Token.RPAREN)
        stmt = self.statement()
        return WhileStatement(expr, stmt)

    def printStatement(self):
        self.match(Token.PRINT)
        self.match(Token.LPAREN)
        expr = self.expr()
        self.match(Token.RPAREN)
        self.match(Token.SEMI)
        return PrintStatement(expr)

    def expr(self):
        left_tree = self.conj()
        while self.curr_tok.type == Token.OR:
            self.curr_tok = next(self.lex)
            right_tree = self.conj()
            left_tree = OpExpr(left_tree, right_tree, "||")
        return left_tree

    def conj(self):
        left_tree = self.equality()
        while self.curr_tok.type == Token.AND:
            self.curr_tok = next(self.lex)
            right_tree = self.equality()
            left_tree = OpExpr(left_tree, right_tree, "&&")
        return left_tree

    def equality(self):
        left_tree = self.relat()
        if self.curr_tok.type in Parser.EquOp_first:
            op = self.curr_tok.value
            self.curr_tok = next(self.lex)
            right_tree = self.relat()
            left_tree = OpExpr(left_tree, right_tree, op)
        return left_tree

    def relat(self):
        left_tree = self.addition()
        if self.curr_tok.type in Parser.RelOp_first:
            op = self.curr_tok.value
            self.curr_tok = next(self.lex)
            right_tree = self.addition()
            left_tree = OpExpr(left_tree, right_tree, op)
        return left_tree

    def addition(self):
        left_tree = self.term()
        while self.curr_tok.type in Parser.addOp_first:
            op = self.curr_tok.value
            self.curr_tok = next(self.lex)
            right_tree = self.term()
            left_tree = OpExpr(left_tree, right_tree, op)
        return left_tree

    def term(self):
        left_tree = self.ExpOp()
        while self.curr_tok.type in Parser.mulOp_first:
            op = self.curr_tok.value
            self.curr_tok = next(self.lex)
            right_tree = self.ExpOp()
            left_tree = OpExpr(left_tree, right_tree, op)
        return left_tree

    def ExpOp(self):
        left = self.fact()
        if self.curr_tok.type == Token.POWER:
            self.curr_tok = next(self.lex)
            right = self.ExpOp()
            left = OpExpr(left, right, '**')
        return left

    def fact(self):
        if self.curr_tok.type in Parser.unaryOp_first:
            op = self.curr_tok.value
            self.curr_tok = next(self.lex)
            expr = self.prim()
            return NegExpr(expr) if op == '-' else NotExpr(expr)
        else:
            return self.prim()

    def prim(self):
        if self.curr_tok.type == Token.ID:
            ident = self.curr_tok.value
            self.curr_tok = next(self.lex)
            return Ident(ident)
        elif self.curr_tok.type == Token.INT:
            value = self.curr_tok.value
            self.curr_tok = next(self.lex)
            return IntLit(value)
        elif self.curr_tok.type == Token.FLOAT:
            value = self.curr_tok.value
            self.curr_tok = next(self.lex)
            return FloatLit(value)
        elif self.curr_tok.type == Token.TRUE:
            self.curr_tok = next(self.lex)
            return TrueExpr()
        elif self.curr_tok.type == Token.FALSE:
            self.curr_tok = next(self.lex)
            return FalseExpr()
        elif self.curr_tok.type == Token.LPAREN:
            self.curr_tok = next(self.lex)
            expr = self.expr()
            self.match(Token.RPAREN)
            return expr
        else:
            self.syntax_error("unexpected input")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        testFile = sys.argv[1]
    else:
        sys.exit("No file specified")

    p = Parser(testFile)
    t = p.parse()
    print(t)
