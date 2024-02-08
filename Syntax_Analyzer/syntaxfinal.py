class Parser:
    
    def init(self, tokens):
        self.tokens = tokens
        self.index = -1
        self.advance()

    def advance(self):
        self.index += 1
        if self.index < len(self.tokens):
            self.current = self.tokens[self.index]
        else:
            self.current = None
        return self.current


    def structure():
        global i, tokenList
        if self.current == 'EOF':
            return True
        pass
        syntaxError("Syntax Error: Invalid start rule")
    
    def start():
        global i, tokenList
        if self.current == "ST" and tokenList[i+1] == "SM":
            if self.current == "ED" and tokenList[i+1].type == "EM":
                i += 2
                return True
        return False
    
        
    def body():
        multi_stm()
        
    def multi_stm():
        if self.current == 'EOF':
            return False
        if single_stm():
            multi_stm()
            
    def single_stm():
        if self.current == 'EOF':
            return False
        elif (self.current == "DT" and tokenList[i+1].type != "DEFINE"):
            dec()
            single_stm()            
        elif self.current == "ID":
            assign_st()
        elif self.current == "CALL_FUNC":
            func_call()
            single_stm()
        elif self.current in ["INC", "DEC"]:
            inc_dec_st()
        elif self.current == "IF":
            if_else()
            single_stm()
        elif (self.current in ['DT', 'VOID'] and tokenList[i+1].type == "DEF"):
            func_def()
            single_stm()
            
    def dec():
        global i, tokenList
        if self.current == "DT":
            self.advance()
            list_()
        else:
            syntaxError("Syntax Error")
    

    def list_():
        global i, tokenList
        if self.current == "SEMI":
            self.advance()
            
            dec()
        elif self.current == "COM":
            self.advance()
            if self.current == "ID":
                self.advance()
                list_()
        elif self.current in ['DIV', 'MIN', 'SUB', 'ADD','RELATION']:
            exp()
        else:
            syntaxError("Syntax Error")
            
    def inc_dec_st():
        if self.current in ["ID", "STR", "CR", "FT", "INT"]:
            self.advance()
            self.exp()
            self.inc_dec_op()
        else:
            raise SyntaxError("Syntax Error")
    
    def inc_dec_op():
        if self.current in ["INC", "DEC"]:
            self.advance()
        else:
            raise SyntaxError("Syntax Error")
    
    def exp():
        if self.and_op():
            return True
        if self.exp_or():
            return True
        return False
    
    def exp_or():
        if self.current() == "OR":
            self.advance()
            if self.and_op():
                return True
            if self.exp_or():
                return True
        return False
    
    def and_op():
        if rel_op():
            return True
        if a_prime():
            return True
        return False

    def a_prime():
        if self.current == "AND":
            self.advance()
            if self.rel_op():
                return True
            if self.a_prime():
                return True
        return False

    def rel_op():
        if self.e():
            return True
        if self.rel_exp():
            return True
        return False

    def rel_exp():
        if self.current in ["L_OR", "L_AND", "E", "NE", "INT"]:
            self.advance()
            if self.e():
                return True
            if self.rel_exp():
                return True
        return False            
    
    def e():
        if self.t():
            return True
        if self.e_prime():
            return True
        return False

    def e_prime():
        if self.current in ["ADD", "MIN"] or tokenList[i+1].type =="ASS":
            self.advance()
            if self.t():
                return True
            if self.e_prime():
                return True
        return False

    def t():
        if self.f():
            return True
        if self.t_prime():
            return True
        return False

    def t_prime():
        if self.current in ["MUL", "DIV", "MOD"]:
            self.advance()
            if self.f():
                return True
            if self.t_prime():
                return True
        return False
    
    def f():
        global i, tokenList
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

    def f_init():
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
        
    def f_init_tail():
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
        
    def func_call():
        if self.current == "ID":
            self.advance()
            if self.current == "LP":
                self.advance()
                self.param()
                if self.current == "RP":
                    self.advance()
                    return True
        raise SyntaxError(
            "Syntax Error: Missing function name in function call")
        
    def param():
        self.exp()
        self.param2()

    def param2():   
        if self.current == "COM":
            self.advance()
            self.exp()
            self.param2()
        else:
            return True
    
except LookupError:
    print("Tree Incomplete... Input Completely Parsed")
    

    
            