from token_dict import *

class Parser:
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = -1
        self.current = None
        self.advance()
    
    def advance(self):
        self.index += 1
        if self.index < len(self.tokens):
            self.current = self.tokens[self.index]
            print("Current token:", self.current)
        else:
            self.current = None
        return self.current
    
    def parse(self):
        if self.current == 'EM':
            return True
        if self.start():
            raise SyntaxError ("ERROR ON PARSE")
 
    def start(self):
        if self.current == 'ST':
            self.advance() 
            if self.current == 'SM': 
                self.advance()   
                if self.body():
                    if self.current == 'ED':
                        self.advance() 
                        if self.current == 'EM':  
                            self.advance()  
                            return True
                else:
                    raise SyntaxError("Syntax Error: Invalid body")
            else:
                raise SyntaxError("Syntax Error: 'ST' must be followed by 'SM'")
        raise SyntaxError("Syntax Error: Invalid start rule")
    
    def body(self):
        self.multi_statement()
      
            
    def multi_statement(self):
        if self.single_smt():
            self.multi_statement()
        return True
      
    
    def single_smt(self):
        if self.current in ["INT"]:
            self.dec()
            self.single_smt()      
        elif self.current == "ID":
            self.assign_st()
        elif self.current == "CF":
            self.func_call()
            self.single_smt()
        elif self.current in ['INC', 'DEC']:
            self.inc_dec_st()
            self.if_else()
            self.single_smt()
        elif self.current == "IF":
            self.if_else()
            self.single_smt()
        elif self.current in [tt_key]:
            self.func_def()
            self.single_smt()
        
    def dec(self):
        if self.current == "INT":
            self.advance()
            if self.current == "ID":
                self.advance()
                self.init()
                self.list_()
        else:
            raise SyntaxError("Syntax Error dec")
    
    def init(self):
        if self.current == "ASS":
            self.advance()
            if self.exp():
                if self.list_():
                    return True
        else:
            raise SyntaxError("Syntax Error init")
        return True

    
    def list_(self):
        if self.current == "SEMI":
            self.advance()
            self.dec()
        elif self.current == 'COM':
            self.advance()
            if self.current == 'ID':
                self.advance()
                self.list_() 
        elif self.current in [tt_oper]:
            self.exp()
        else:
             SyntaxError("Syntax Error list")
             
    def if_else(self):
        if self.current == 'IF':
            self.advance()
            if self.current == 'LP':
                self.advance()
                self.exp()
                if self.current == 'RP':
                    self.advance()
                    if self.current == 'LC':
                        self.advance()
                        self.body()
                        if self.current =='RC':
                            self.advance()
                            self.if_else_tail()
        raise SyntaxError ("Syntax Error: Missing 'IF' in 'if' statement")
        
    def if_else_tail(self):
        if self.current == 'ELIF':
            self.advance()
            if self.current == 'LP':
                self.advance()
                self.exp()
                if self.current == 'RP':
                    self.advance()
                    if self.current == 'LC':
                        self.advance()
                        self.body()
                        if self.current == 'RC':
                            self.advance()
                            self.if_else_tail()
                    else:
                        raise SyntaxError("Syntax Error: Missing ':' after condition in 'check' statement")
                else:
                    raise SyntaxError("Syntax Error: Missing ')' after condition in 'check' statement")
                    
        elif self.current == 'EL':
            self.advance()
            if self.current == 'LC':
                self.advance()
                self.body()
                if self.current == 'RC':
                    self.if_else_tail()
            else:
                raise SyntaxError ("Syntax Error: Missing ':' after 'else'")
        else:
            return True
    def for_loop(self):
        if self.current == 'FOR':
            self.advance()
            if self.current == 'LP':
                self.advance()
                self.for_loop_init()
                if self.current == "SEMI":
                    self.advance()
                    self.cond()
                    if self.current == "SEMI":
                        self.advance()
                        self.update()
                    if self.current == "RP":
                        self.advance()
                        if self.current == "LB":
                            self.advance()
                            self.body()
                            if self.current == "RB":
                                self.advance()
                                return True
                            else:
                                raise SyntaxError("Syntax Error: Missing '}'")
                        else:
                           raise SyntaxError("Syntax Error: Missing '{'")
                    else:
                       raise SyntaxError("Syntax Error: Missing ')'")
                else:
                   raise SyntaxError("Syntax Error: Missing ';'")
            else:
               raise SyntaxError("Syntax Error: Missing ';' after condition")
        else:
           raise SyntaxError("Syntax Error: Missing '('")
                       
    def for_loop_init(self):
        if self.current == "DT":
            self.advance()
            if self.current == "ID":
                self.advance()
                if self.current == "ASS":
                    self.advance()
                    if self.current in ['ID', 'INT', 'FT', 'STR', 'CR']:
                        self.advance()
                        return True
        else:
            raise SyntaxError("Syntax Error")
    def cond(self):
        

        if self.current in ["ID", "INT", "FT", "STR","CR","L_NOT"]: 
        
            self.exp()
            
        else:
            return True # Epsilon case
        
    def update(self):
        
        if self.current == "ID":
            self.advance()
            if self.current in ["INC", "DEC"]:
                self.advance()
                return True
        else:
            return True # Epsilon case
        
    def assign_st(self):
        
        if self.current == "ID":
            self.advance()
            self.assignop()
            self.exp()
        else:
            raise SyntaxError("Syntax Error: Missing ID in assignment statement")

    def assignop(self):
        
        if self.current in ["ASS", "ADD_ASS", "MINUS_ASS", "MULTI_ASS", "DIV_ASS", "MOD_ASS"]:
            self.advance()
        else:
            raise SyntaxError("Syntax Error: Invalid assignment operator")
            
    def param(self):
        self.exp()
        self.param2()

    def param2(self):
        
        if self.current == "COM":
            self.advance()
            self.exp()
            self.param2()
        else:
            return True # Epsilon case
    
    def func_def(self):
        
        if (self.current == "DT" or self.current == "VD"):
            self.advance()
            if self.current == "DEF":
                self.advance()
                if self.current == "ID":
                    self.advance()
                    if self.current == "LP":
                        self.advance()
                        self.args()
                        if self.current == "RP":
                            self.advance()
                            if self.current == "LB":
                                self.advance()
                                self.body()
                                if self.current == "RB":
                                    self.advance()
                                    return True
                                
        raise SyntaxError("Syntax Error: Missing 'DEFINE' keyword in function definition")
    
    def args(self):
        if self.current == "DT":
            self.advance()
            if self.current == "ID":
                self.advance()
                self.n_args()
                
                raise SyntaxError("Syntax Error: Missing data type in function arguments")
    
    def n_args(self):
        if self.current == "SEPARATOR":
            self.advance()
            if self.current == "DT":
                self.advance()
                if self.current == "ID":
                    self.advance()
                    self.n_args()
            raise SyntaxError("Syntax Error: Missing data type in function arguments")
        else:
            return True # Epsilon case
        #raise SyntaxError("Syntax Error: Missing data type in function arguments")            ()
    
    def inc_dec_st(self):
        if self.current in ["ID", "STR", "CR", "FT", "INT"]:
            self.advance()
            self.exp()
            self.inc_dec_op()
        else:
            raise SyntaxError("Syntax Error")
    
    def inc_dec_op(self):
        if self.current in ["INC", "DEC"]:
            self.advance()
        else:
            raise SyntaxError("Syntax Error")
    
    def exp(self):
        if self.and_op():
            return True
        if self.exp_or():
            return True
        return False
    
    def exp_or(self):
        if self.current() == "OR":
            self.advance()
            if self.and_op():
                return True
            if self.exp_or():
                return True
        return False
    
    def and_op(self):
        if self.rel_op():
            return True
        if self.a_prime():
            return True
        return False

    def a_prime(self):
        if self.current == "AND":
            self.advance()
            if self.rel_op():
                return True
            if self.a_prime():
                return True
        return False

    def rel_op(self):
        if self.e():
            return True
        if self.rel_exp():
            return True
        return False

    def rel_exp(self):
        if self.current in ["L_OR", "L_AND", "E", "NE", "INT"]:
            self.advance()
            if self.e():
                return True
            if self.rel_exp():
                return True
        return False            
    
    def e(self):
        if self.t():
            return True
        if self.e_prime():
            return True
        return False

    def e_prime(self):
        if self.current in ["ADD", "MIN"] or self.current == "ASS":
            self.advance()
            if self.t():
                return True
            if self.e_prime():
                return True
        return False

    def t(self):
        if self.f():
            return True
        if self.t_prime():
            return True
        return False

    def t_prime(self):
        if self.current in ["MUL", "DIV", "MOD"]:
            self.advance()
            if self.f():
                return True
            if self.t_prime():
                return True
        return False
    
    def f(self):
        if self.current == "ID":
            self.advance()
            self.f_init()
        elif self.current in ["INT", "FT", "STR", "CR"]:
            self.advance()
            return True
        elif self.current == "L_NOT":
            self.advance()
            if self.f():
                return True
        elif self.current == "CALLING":
            self.advance()
            self.func_call()
        raise SyntaxError("Syntax Error: Expected ID or literal")

    def f_init(self):
        if self.current == "LB":
            self.advance()
            self.exp()
            if self.current == "RB":
                self.advance()
                self.f_init()
        elif self.current == "ID":
            self.advance()
            self.f_init()
        elif self.current in ["INC", "DEC"]:
            self.advance()
        else:
            return True
        
    def f_init_tail(self):
        if self.current == "ID":
            self.advance()
            self.f_init()
        elif self.current == "LB":
            self.advance()
            self.exp()
            if self.current == "RB":
                self.advance()
                self.f_init()
        else:
            return True
        
    def func_call(self):
        if self.current == "ID":
            self.advance()
            if self.current == "LP":
                self.advance()
                self.param()
                if self.current == "RP":
                    self.advance()
                    return True
        raise SyntaxError("Syntax Error: Missing function name in function call")
        
    def param(self):
        self.exp()
        self.param2()

    def param2(self):   
        if self.current == "COM":
            self.advance()
            self.exp()
            self.param2()
        else:
            return True
        
def test_parser(file_path):
    with open(file_path, 'r') as file:
        tokens = file.read().split(',')
    
    try:
        parser = Parser(tokens)
        parser.start()
        print("Parsing successful!")
    except SyntaxError as e:
        print("Parsing failed:", e)

# Example usage:
test_parser("lexer.txt")
