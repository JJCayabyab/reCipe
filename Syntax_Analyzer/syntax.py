from token_dict import *
from tree import *

class Token:
    def __init__(self, token_type, value=None, line=None):
        self.type = token_type
        self.value = value
        self.line = line

    def __repr__(self):
        return f"Token({self.type}, {self.value}, {self.line})"

class Main:
    pass

class Statement(Main):
    pass

class Expr(Main):
    pass

    
class Program(Main):
    def __init__(self, declarations, statements):
        self.declarations = declarations
        self.statements = statements

    def __repr__(self):
        return f"Program({self.declarations}, {self.statements})"

class Declaration(Main):
    def __init__(self, type_, ident):
        self.type = type_
        self.ident = ident

    def __repr__(self):
        return f"Declaration({self.type}, {self.ident})"

class Ident(Main):
    def __init__(self, ident):
        self.ident = ident

    def __repr__(self):
        return f"Ident('{self.ident}')"

class Assignment(Main):
    def __init__(self, ident, expr):
        self.ident = ident
        self.expr = expr

    def __repr__(self):
        return f"Assignment({self.ident}, {self.expr})"

class Block(Main):
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Block({self.statements})"

class IfStatement(Main):
    def __init__(self, expr, if_stmt, else_stmt=None):
        self.expr = expr
        self.if_stmt = if_stmt
        self.else_stmt = else_stmt

    def __repr__(self):
        return f"IfStatement({self.expr}, {self.if_stmt}, {self.else_stmt})"

class PrintStatement(Main):
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return f"PrintStatement({self.expr})"


class WhileStatement(Main):
    def __init__(self, expr, stmt):
        self.expr = expr
        self.stmt = stmt

    def __repr__(self):
        return f"WhileStatement({self.expr}, {self.stmt})"
    
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
    
    type_first = {"INT", "CR", "FT", "DB", "IF", "FOR", "BL", "STR"}
    stmt_first = {"SEMI", "LB", "ID", "IF", "WH", "DP"}
    EquOp_first = {"E", "MINUS_ASS"}
    RelOp_first = {"GT", "GOE", "LT", "LOE"}
    addOp_first = {"ADD", "MIN"}
    mulOp_first = {"MUL", "DIV", "MOD"}
    unaryOp_first = {"L_NOT", "MIN"}
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = -1
        self.advance()

    def advance(self):
        self.index += 1
        if self.index < len(self.tokens):
            self.current = self.tokens[self.index]
            print("Current token:", self.current)
            return self.current
        else:
            self.current = None
            return None

    def match(self, expected_token_type):
        if self.current != expected_token_type:
            self.syntax_error(f"'{Token.__dict__.get(expected_token_type)}' expected")
        self.current = self.advance()
        
    def program(self):
        if self.current != "ST":
            self.syntax_error("'START' expected")
        self.match("ST")
        self.match("SM")

        decls = self.declarations()
        stmts = self.statements()
        
        if self.current != "ED":
            self.syntax_error("'END' expected")
        self.match("ED")
        self.match("EM")
        return Program(decls, stmts)
    
    def syntax_error(self, message):
        print(f"Syntax Error: {message}, found {Token.__dict__.get(self.current)} on line {self.current.line}")
        exit(1)
        
    def declarations(self):
        decls = dict()
        while self.current in Parser.type_first:
            decl = self.declaration()
            decls[decl.ident] = decl
        return decls
    
    def declaration(self):
        type_ = self.type_()
        self.match("SEMI")
        return Declaration(type_, self.current.value)
    
    def type_(self):
        if self.current in Parser.type_first:
            type_ = self.current
            self.current = self.advance()
        else:
            self.syntax_error(" Data type is expected")
        if self.current != "ID":
            self.syntax_error("Identifier expected")
            ident = self.current.value
            self.current = self.advance()
        return type_
    
    def statements(self):
        stmts = []
        while self.current in Parser.stmt_first:
            stmts.append(self.statement())
        return stmts

    def statement(self):
        if self.current == "SEMI":
            self.match(Token.SEMI)
            return Statement()
        elif self.current == "LB":
            return self.block()
        elif self.current == "ID":
            return self.assignment()
        elif self.current == "IF":
            return self.ifStatement()
        elif self.current == "WH":
            return self.whileStatement()
        elif self.current == "DP":
            return self.printStatement()
    
    def block(self):
        self.match("LB")
        stmts = self.statements()
        self.match("RB")
        return Block(stmts)
    
    def assignment(self):
        ident = self.current.value
        self.match("ID")
        self.match("ASS")
        expr = self.expr()
        self.match("SEMI")
        return Assignment(ident, expr)
    
    def ifStatement(self):
        self.match("IF")
        self.match("LP")
        expr = self.expr()
        self.match("RP")
        if_stmt = self.statement()
        else_stmt = None
        if self.current == "EL":
            self.match("EL")
            else_stmt = self.statement()
        return IfStatement(expr, if_stmt, else_stmt)
    
    def whileStatement(self):
        self.match("WH")
        self.match("LP")
        expr = self.expr()
        self.match("RP")
        stmt = self.statement()
        return WhileStatement(expr, stmt)
    
    def printStatement(self):
        self.match("DP")
        self.match("LP")
        expr = self.expr()
        self.match("RP")
        self.match("SEMI")
        return PrintStatement(expr)

    def expr(self):
        left_tree = self.conj()
        while self.current == "L_OR":
            self.current = self.advance()
            right_tree = self.conj()
            left_tree = OpExpr(left_tree, right_tree, "L_OR")
        return left_tree
    
    def conj(self):
        left_tree = self.equality()
        while self.current == "L_AND":
            self.current = self.advance()
            right_tree = self.equality()
            left_tree = OpExpr(left_tree, right_tree, "L_AND")
        return left_tree
    
    def equality(self):
        left_tree = self.relat()
        if self.current in Parser.EquOp_first:
            op = self.current.value
            self.current = self.advance()
            right_tree = self.relat()
            left_tree = OpExpr(left_tree, right_tree, op)
        return left_tree
    
    def relat(self):
        left_tree = self.addition()
        if self.current in Parser.RelOp_first:
            op = self.current.value
            self.current = self.advance()
            right_tree = self.addition()
            left_tree = OpExpr(left_tree, right_tree, op)
        return left_tree

    def addition(self):
        left_tree = self.term()
        while self.current in Parser.addOp_first:
            op = self.current.value
            self.current = self.advance()
            right_tree = self.term()
            left_tree = OpExpr(left_tree, right_tree, op)
        return left_tree
    
    def term(self):
        left_tree = self.ExpOp()
        while self.current in Parser.mulOp_first:
            op = self.current.value
            self.current = self.advance()
            right_tree = self.ExpOp()
            left_tree = OpExpr(left_tree, right_tree, op)
        return left_tree

    def ExpOp(self):
        left = self.fact()
        if self.current == "POW":
            self.current = self.advance()
            right = self.ExpOp()
            left = OpExpr(left, right, 'POW')
        return left

    def fact(self):
        if self.current in Parser.unaryOp_first:
            op = self.current.value
            self.current = self.advance()
            expr = self.prim()
            return NegExpr(expr) if op == 'MIN' else NotExpr(expr)
        else:
            return self.prim()

    def prim(self):
        if self.current == "ID":
            ident = self.current.value
            self.current = self.advance()
            return Ident(ident)
        elif self.current == "INT":
            value = self.current.value
            self.current = self.advance()
            return IntLit(value)
        elif self.current == "FT":
            value = self.current.value
            self.current = self.advance()
            return FloatLit(value)
        elif self.current == "T":
            self.current = self.advance()
            return TrueExpr()
        elif self.current == "F":
            self.current = self.advance()
            return FalseExpr()
        elif self.current == "LP":
            self.current = self.advance()
            expr = self.expr()
            self.match("RP")
            return expr
        else:
            self.syntax_error("unexpected input")


tokens = [
    Token("ST"),   # Start of program
    Token("INT"),  # Data type
    Token("ID",),  # Identifier
    Token("ASS"),  # Assignment operator
    Token("INT",),  # Integer literal
    Token("SEMI"), # Semicolon
    Token("ED"),   # End of program
]

parser = Parser(tokens)
parsed_program = parser.program()
print(parsed_program)


