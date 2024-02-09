from configparser import ParsingError

class Parser:
     
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.token_index = -1
        self.line_number = 1  # Initialize line number
        self.advance()

    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
            print(f"Line {self.line_number}: Token:", self.current_token)
            if self.current_token == "NEWLINE":
                self.line_number += 1  # Increment line number for each newline token
        else:
            self.current_token = None
            
    def consume(self, token_type):
        if self.current_token == token_type:
            self.advance()
        else:
            raise ParsingError(f"Line {self.line_number}: Expected token '{token_type}', got '{self.current_token}' instead.")
    def analyze(self):
        try:
            self.body()
            return True
        except ParsingError as e:
            print("ParsingError:", e)
            return False
    
    def start():
        
        pass
    
    def body(self):
        self.principles()
        self.statement()
        self.declaration_list()
      
    def declaration_list(self):
        while self.current_token is not None and self.current_token != 'EOF':
            self.declaration()
   
    def declaration(self):
        self.dt()
        self.declarator_list()
        self.consume('SEMI')
    
    def dt(self):
        if self.current_token in ['INT', 'FT', 'CR', 'STR', 'DB', 'BL',"TAB"]:
            self.advance()
        else:
            raise ParsingError(f"Expected data type token, got '{self.current_token}' instead.")
    
    def declarator_list(self):
        self.init_declarator()
        while self.current_token == "COM":
            self.consume("COM")
            self.init_declarator()
            
    def init_declarator(self):
        self.declarator()
        if self.current_token == "ASS":
            self.consume("ASS")
            self.initializer()
        
    def declarator(self):
        self.identifier()
        
    def identifier(self):
        if self.current_token == "ID":
            self.advance()
        else:
            raise ParsingError(f"Expected identifier token, got '{self.current_token}' instead.")
        
    def initializer(self):
        self.ass_expr()
        
    def statement(self):
        self.compound_stm()
        self.exp_stm()
        self.selection_stm()
        self.iteration_stm()  
    
    def exp_stm(self):
        self.expression()
        if self.current_token == "SEMI":
            self.consume("SEMI")
        
    def compound_stm(self):
        if self.current_token == "LC":
            self.consume("LC")
            self.stm_list()
            if self.current_token == "RC":  # {DOR };
                self.consume("RC")
                    
    def stm_list(self):
        self.statement()
        if self.current_token is not None and self.current_token != 'RC':
            self.stm_list()
    
    def selection_stm(self):
        self._if()   
        self.if_else()
        
    def _if(self):
        if self.current_token == "IF":
            self.consume("IF")
            if self.current_token == "LP":
                self.consume("LP")
                self.expression()
                if self.current_token == "RP":
                    self.consume("RP")
                    self.statement()
                    self.if_else()

    def if_else(self):  
        self._if()   
        if self.current_token == "EL":
            self.consume("EL")
            self.statement()
                                                
    def iteration_stm(self):
        self._for()
        self._while()
        self._do()
        
    def _for(self):
        if self.current_token == "FOR":
            self.consume("FOR")
            if self.current_token == "LP":
                self.consume("LP")
                self.for_init()
                if self.current_token == "SEMI":
                    self.consume("SEMI")
                    self.for_condition()
                    if self.current_token == "SEMI":
                        self.consume("SEMI")
                        self.for_update()
                        if self.current_token == "RP":
                            self.consume("RP")
                            self.statement()
                            if self.current_token == "SEMI":
                                self.consume("SEMI")
    def _while(self):                 
        if self.current_token == "WH":
            self.consume("WH")
            if self.current_token == "LP":
                self.consume("LP")
                self.expression()
                if self.current_token == "RP":
                    self.consume("RP")
                    self.statement()
                    if self.current_token == "SEMI":
                        self.consume("SEMI")
                    
    def _do(self):    
        if self.current_token == "DO":
            self.consume("DO")
            self.statement()
            if self.current_token == "WH":
                self.consume("WH")
                if self.current_token == "LP":
                    self.consume("LP")
                    self.expression()
                    if self.current_token == "RP":
                        self.consume("RP")
                        if self.current_token == "SEMI":
                            self.consume("SEMI")
    def statement(self):
        self.compound_stm()
        self.exp_stm()
        self.selection_stm()
        self.iteration_stm()  
                          
    def for_init(self):
        self.exp_stm()
        self.declaration()
               
    def for_condition(self):
        self.expression()
        return True
    
    def expression(self):
        self.ass_expr()
        while self.current_token == "COM":
            self.consume('COM')
            self.ass_expr()
            
    def for_update(self):
        self.exp_stm()
        return True

    def ass_expr(self):
        self.cond_exp()
        if self.current_token == "ASS":
            self.consume('ASS')
            self.ass_expr()
               
    def cond_exp(self):
        self.logic_or()
    
    def logic_or(self):
        self.logic_and()
        if self.current_token == "L_OR":
            self.consume('L_OR')
            self.logic_and()
            
    def logic_and(self):
        self.equal_exp()
        if self.current_token == "L_AN":
            self.consume('L_AN')
            self.equal_exp()
    
    def equal_exp(self):
        self.rel_exp()
        while self.current_token in ["E", "NE"]:
            if self.current_token == "E":
                self.consume("E")
                self.rel_exp()
            elif self.current_token == "NE":
                self.consume("NE")
                self.rel_exp()
           
    def rel_exp(self):
        self.add_exp()
        while self.current_token in ["GT", "LT", "GOE", "LOE"]:
            if self.current_token == "GT":
                self.consume("GT")
                self.add_exp()
            elif self.current_token == "LT":
                self.consume("LT")
                self.add_exp()
            elif self.current_token == "GOE":
                self.consume("GOE")
                self.add_exp()
            elif self.current_token == "LOE":
                self.consume("LOE")
                self.add_exp()
               
    def add_exp(self):
        self.mul_exp()
        while  self.current_token in ["ADD", "MIN"]:
            if self.current_token == "ADD":
                self.consume("ADD")
                self.mul_exp()
            elif self.current_token == "MIN":
                self.consume("MIN")
                self.mul_exp()
    
    def mul_exp(self):
        self.unary()
        while self.current_token in ["MOD", "DIV", "MUL"]:
            if self.current_token == "MOD":
                self.consume("MOD")
                self.unary()
            elif self.current_token == "DIV":
                self.consume("DIV")
                self.unary()
            elif self.current_token == "MUL":
                self.consume("MUL")
                self.unary()
    
    def unary(self):
        self.postfix()
        while self.current_token in ["ADD", "MIN", "L_NOT"]:
            if self.current_token == "ADD":
                self.consume("ADD")
                self.postfix()
            elif self.current_token == "MIN":
                self.consume("MIN")
                self.postfix()
            elif self.current_token == "L_NOT":
                self.consume("L_NOT")
                self.postfix()
    
    def postfix(self):
        self.primary()
        while self.current_token in ["INC", "DEC"]:
            if self.current_token == "INC":
                self.consume("INC")
                self.identifier()
            elif self.current_token == "DEC":
                self.consume("DEC")
                self.identifier()
    
    
    def primary(self): # primary 
        if  self.current_token == "ID":
            self.consume("ID")
        elif self.current_token in ["IL", "SL", "FL", "DL", "CL", "TR", "FA"]:
            self.advance()
        elif self.current_token == "LP":
            self.consume("LP")
            self.expression()
            if self.current_token == "RP":
                self.consume("RP")
        elif self.current_token == "DP":
            self.consume("DP")
            self.output
        elif self.current_token == "GET":
            self.consume("GET")
            self.input()

    def output(self): # display of printf in C
       if self.current_token == "DP":
           self.consume("DP")
           if self.current_token == "LP":
               self.consume("LP")
               if self.current_token == "PH":
                   self.consume("PH")
                   if self.current_token == "SL":
                       self.consume("SL")
                       if self.current_token == "RP":
                           if self.current_token == "SEMI":
                               self.consume("SEMI")

    def input(self): # get of scanf in C
        if self.current_token == "GET":
            self.consume("GET")
            if self.current_token == "LP":
                self.consume("LP")
                if self.current_token == "PH":
                    self.consume("PH")
                    if self.current_token == "RP":
                        self.consume("RP")
                        if self.current_token == "SEMI":
                            self.consume("SEMI")
    def principles(self):
        self.table_gen()
        self.unit_con()
        self.div_mod()
        
    def table_gen(self): # table 
        self.create_tab()
        self.set_val()
        self.disp()
        self.free()
        
    def create_tab(self): # iniialize table
        if self.current_token == "TAB": 
            self.consume("TAB")
            if self.current_token == "ID":
                self.consume("ID")
                if self.current_token == "ASS":
                    self.consume("ASS")
                    if self.current_token == "CRETAB":
                        self.consume("CRETAB")
                        if self.current_token == "LP":
                            self.consume("LP")
                            if self.current_token == "IL":
                                self.consume("IL")
                                if self.current_token == "COM":
                                    self.consume("COM")
                                    if self.current_token == "IL":
                                        self.consume("IL")
                                        if self.current_token == "RP":
                                            self.consume("RP")
                                            if self.current_token == "SEMI":
                                                self.consume("SEMI")
                                    
    def set_val(self): # set cell value
        while self.current_token == "SETCELVAL":
            if self.current_token == "SETCELVAL":
                self.consume("SETCELVAL")
                if self.current_token == "LP":
                    self.consume("LP")
                    if self.current_token == "PH":
                        self.consume("PH")
                        if self.current_token == "ID":
                            self.consume("ID")
                            if self.current_token == "COM":
                                self.consume("COM")
                                if self.current_token == "IL":
                                    self.consume("IL")
                                    if self.current_token == "COM":
                                        self.consume("COM")
                                        if self.current_token == "IL":
                                            self.consume("IL")
                                            if self.current_token == "COM":
                                                self.consume("COM")
                                                if self.current_token == "SL":
                                                    self.consume("SL")
                                                    if self.current_token == "RP":
                                                        self.consume("RP")
                                                        if self.current_token == "SEMI":
                                                            self.consume("SEMI")
                          
    
    def disp(self): 
        if self.current_token == "DISTAB":
            self.consume("DISTAB")
            if self.current_token == "LP":
                self.consume("LP")
                if self.current_token == "PH":
                    self.consume("PH")
                    if self.current_token == "ID":
                        self.consume("ID")
                        if self.current_token == "RP":
                            self.consume("RP")
                            if self.current_token == "SEMI":
                                self.consume("SEMI")
                            else:
                                raise SyntaxError("Missing ';' after ID")
                        else:
                            raise SyntaxError("Missing ')' after ID")
                    else:
                        raise SyntaxError("Missing identifier after '('")
                else:
                    raise SyntaxError("Missing placeholder after '('")
            else:
                raise SyntaxError("Missing '(' after DISTAB")
        else:
            raise SyntaxError("Missing 'DISTAB' keyword")
        
    
    def free(self): # free table
        if self.current_token == "FRETAB":
            self.consume("FRETAB")
            if self.current_token == "LP":
                self.consume("LP")
                if self.current_token == "PH":
                    self.consume("PH")
                    if self.current_token == "ID":
                        self.consume("ID")
                        if self.current_token == "RP":
                            self.consume("RP")
                            if self.current_token == "SEMI":
                                self.consume("SEMI")
                            else:
                                raise SyntaxError("Missing ';' after ID")
                        else:
                            raise SyntaxError("Missing ')' after ID")
                    else:
                        raise SyntaxError("Missing identifier after '('")
                else:
                    raise SyntaxError("Missing placeholder after '('")
            else:
                raise SyntaxError("Missing '(' after FRETAB")
        else:
            raise SyntaxError("Missing 'FRETAB' keyword")
        
    
    def div_mod(self): # division modulo
        self.div_stm()
        self.div_call()
        self.div_disp()
    
    def div_stm(self):
        if self.current_token == "INT":
            self.consume("INT")
            if self.current_token == "ID":
                self.consume("ID")
                if self.current_token == "LB":
                    self.consume("LB")
                    if self.current_token == "IL":
                        self.consume("IL")
                        if self.current_token == "RB":
                            self.consume("RB")
                            if self.current_token == "ASS":
                                self.consume("ASS")
                                if self.current_token == "QR":
                                    self.consume
                                if self.current_token == "SEMI":
                                    self.consume("SEMI")
                                    self.div_disp()
    
    def div_call(self):
        if self.current_token == "QR":
            self.consume("QR")
            if self.current_token == "LP":
                self.consume("LP")
                if self.current_token == "IL":
                    self.consume("IL")
                    if self.current_token == "COM":
                        self.consume("COM")
                        if self.current_token == "IL":
                            self.consume("IL")
                            if self.current_token == "RP":
                                self.consume("RP")
                         
    def div_disp(self):
        if self.current_token == "DP":
            self.consume("DP")
            if self.current_token == "LP":
                self.consume("LP")
                if self.current_token == "ID":
                    self.consume("ID")
                    if self.current_token == "LB":
                        self.consume("LB")
                        if self.current_token == "IL":
                            self.consume("IL")
                            if self.current_token == "RB":
                                self.consume("RB")
                                if self.current_token == "COM":
                                    self.consume("COM")
                                    if self.current_token == "ID":
                                        self.consume("ID")
                                        if self.current_token == "LB":
                                            self.consume("LB")
                                            if self.current_token == "IL":
                                                self.consume("IL")
                                                if self.current_token == "RB":
                                                    self.consume("RB")
                                                    if self.current_token == "RP":
                                                        self.consume("RP")
                                                     
    def unit_con(self):
        self.unit_state()
        self.unit_disp()
        self.arg()
    
    def unit_state(self):
        if self.current_token in ["INT", "FT", "DB"]:
            self.advance()
            if self.current_token == "ID":
                self.consume("ID")
                if self.current_token == "ASS":
                    self.consume("ASS")                      
                    if self.current_token == "UC":
                        self.consume("UC")
                        if self.current_token == "LP":
                            self.consume("LP")
                            if self.current_token == "IL":
                                self.consume("IL")
                                if self.current_token =="COM":
                                    self.consume("COM")
                                    if self.current_token == "SL":
                                        self.consume("SL")
                                        if self.current_token =="COM":
                                            self.consume("COM")
                                            if self.current_token == "SL":
                                                self.consume("SL")
                                                if self.current_token =="RP":
                                                    self.consume("RP")
                                                    if self.current_token =="SEMI":
                                                        self.consume("SEMI")
                                                                   
    def unit_disp(self):
        if self.current_token == "DP":
            self.consume("DP")
            if self.current_token == "LP":
                self.consume("LP")
                self.arg()
                if self.current_token == "RP":
                    self.consume("RP")
                    if self.current_token == "SEMI":
                        self.consume("SEMI")
                    else:
                        print("Error: '")
                else:
                    print("Error: Expected RP")
            else:
                print("Error: Expected LP")
        else:
            print("Error: Expected DP")

                    
    def arg(self):
        if self.current_token == "PH":
            self.consume("PH")
            if self.current_token == "SL":
                self.consume("SL")
        elif self.current_token == "ID":
                self.consume("ID")

def read_tokens_from_file(filename):
    with open(filename, 'r') as file:
        content = file.read().strip()
        tokens = [token.strip() for token in content.split(',')]
    return tokens


# Example usage
filename = "lexer.txt"  # Replace with your file name
tokens = read_tokens_from_file(filename)
try:
    parser = Parser(tokens)
    parser.analyze()  # Call the method to start
except ParsingError as e:
    print("Parsing Error:", e)
