import sys

# Token types
INT = "INT"
FLOAT = "FLOAT"
BOOL = "BOOL"

class Program:
    env = {}

    def __init__(self, decls, stmts):
        self.decls = decls
        self.stmts = stmts

    def __str__(self):
        indent = 0
        prog = "int main () { \n"
        for decl in self.decls:
            if self.decls[decl].tp == INT:
                prog += "\tint "
            elif self.decls[decl].tp == FLOAT:
                prog += "\tfloat "
            elif self.decls[decl].tp == BOOL:
                prog += "\tbool "
            prog += decl + '\n'

        for stmt in self.stmts:
            prog += stmt.__str__(indent) + '\n'

        prog += "}"
        return prog


class Declaration:
    def __init__(self, tp, ident):
        self.ident = ident
        self.tp = tp

    def __str__(self):
        return "Need to fill in __str__;\n"


class Stmt:
    pass


class Semi(Stmt):
    def __str__(self, indent):
        return "; \n"


class Assign(Stmt):
    def __init__(self, ident, expr):
        self.ident = ident
        self.expr = expr

    def __str__(self, indent):
        indent += 1
        return '\t' * indent + self.ident + " = " + str(self.expr) + ';'


class Block(Stmt):
    def __init__(self, stmts):
        self.stmts = stmts

    def __str__(self, indent):
        block = "\t" * indent + "{ \n"
        for s in self.stmts:
            block = block + s.__str__(indent) + '\n'
        block += "\t" * indent + "}"
        return block


class WhileStatement(Stmt):
    def __init__(self, expr, stmt):
        self.expr = expr
        self.stmt = stmt

    def __str__(self, indent):
        indent += 1
        return '\t' * indent + 'while ' + str(self.expr) + '\n' + self.stmt.__str__(indent)


class IfStatement(Stmt):
    def __init__(self, expr, stmt, elstmt):
        self.expr = expr
        self.stmt = stmt
        self.elstmt = elstmt

    def __str__(self, indent):
        indent += 1
        return '\t' * indent + 'if ' + str(self.expr) + '\n' + self.stmt.__str__(indent)


class PrintStatement(Stmt):
    def __init__(self, stmt):
        self.stmt = stmt

    def __str__(self, indent):
        indent += 1
        return '\t' * indent + 'print(' + self.stmt.__str__() + ');'


class Expr:
    def __init__(self, left, right):
        self.left = left
        self.right = right


class TrueExpr(Expr):
    def __init__(self, Bool):
        Expr.__init__(self, None, None)
        self.Bool = Bool

    def __str__(self):
        return str(self.Bool)


class FalseExpr(Expr):
    def __init__(self, Bool):
        Expr.__init__(self, None, None)
        self.Bool = Bool

    def __str__(self):
        return str(self.Bool)


class IntLit(Expr):
    def __init__(self, val):
        Expr.__init__(self, None, None)
        self.val = int(val)

    def __str__(self):
        return str(self.val)


class FloatLit(Expr):
    def __init__(self, val):
        Expr.__init__(self, None, None)
        self.val = val

    def __str__(self):
        return str(self.val)


class Ident(Expr):
    def __init__(self, id):
        Expr.__init__(self, None, None)
        self.id = id

    def __str__(self):
        return str(self.id)


class UnaryExpr(Expr):
    def __init__(self, expr):
        Expr.__init__(self, None, None)
        self.expr = expr


class NegExpr(UnaryExpr):
    def __init__(self, expr):
        UnaryExpr.__init__(self, expr)

    def __str__(self):
        return '-' + '(' + str(self.expr) + ')'


class NotExpr(UnaryExpr):
    def __init__(self, expr):
        UnaryExpr.__init__(self, expr)

    def __str__(self):
        return '!' + '(' + str(self.expr) + ')'


class OpExpr(Expr):
    def __init__(self, left, right, op):
        Expr.__init__(self, left, right)
        self.op = op

    def __str__(self):
        return "(" + str(self.left) + ' ' + str(self.op) + ' ' + str(self.right) + ")"


# Main program to test some of the classes above
if __name__ == "__main__":

    # represent a + 55
    expr = OpExpr(Ident('a'), IntLit(55), '+')
    print(expr)

    # (a + c) * 99
    expr2 = OpExpr(OpExpr(Ident('a'), Ident('c'), '+'), IntLit(99), '+')
    print(expr2)

    # (a+55) + ((a+c) * 99)
    expr3 = OpExpr(expr, expr2, '*')
    print(expr3)
