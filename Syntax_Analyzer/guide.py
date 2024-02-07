i = 0
tokenList = []
errorAt = 0
synError = ""

def syntaxAnalyzer(tokens):
    global i, tokenList, errorAt, synError
    i = 0
    errorAt = 0
    tokenList = tokens
    result = structure()
    if tokenList[i].type == 'EOF':
        print("Your code is syntactically correct")
        return 
    
    if (not result):
        synError += "\nTOKEN UNEXPECTED:\n\tValue:\t" + tokenList[errorAt].value + "\n\tType:\t" + tokenList[errorAt].type + \
            "\n\tFile:\t\'.\\input.txt\' [@ " + str(
                tokenList[errorAt].line) + "]\n\tToken:\t" + str(errorAt) + "\n\n\n"
        print("\nTOKEN UNEXPECTED:\n\tValue:\t" + tokenList[errorAt].value + "\n\tType:\t" + tokenList[errorAt].type +
              "\n\tFile:\t\'.\\input.txt\' [@ line " + str(tokenList[errorAt].line) + "]\n\tToken:\t" + str(errorAt))
    return synError, result

def syntaxError(message='default'):
    global i, tokenList, errorAt
    if (i > errorAt):
        errorAt = i
    return False

try:

    def structure():
        global i, tokenList
        if tokenList[i].type == 'EOF':
            return True
        pass
        syntaxError("Syntax Error: Invalid start rule")
    
    def start():
        global i, tokenList
        if tokenList[i].type == "ST" and tokenList[i+1] == "<<":
            if tokenList[i].type == "END" and tokenList[i+1].type == ">>":
                i += 2
                return True
        else:
            False
    
    def body():
        MST()
        
    def MST():
        if tokenList[i].type == 'EOF':
            return False
        if SST():
            MST()
            
    def SST():
        if tokenList[i].type == 'EOF':
            return False
        elif (tokenList[i].type == "DT" and tokenList[i+1].type != "DEFINE"):
            dec()
            SST()            
        elif tokenList[i].type == "ID":
            assign_st()
        elif tokenList[i].type == "CALL_FUNC":
            func_call()
            SST()
        elif tokenList[i].type == "INC_DEC":
            inc_dec_st()
        elif tokenList[i].type == "WHEN":
            when_otherwise()
            SST()
        elif (tokenList[i].type in ['DT', 'VOID'] and tokenList[i+1].type == "DEF"):
            func_def()
            SST()
            
    def dec():
        global i, tokenList
        if tokenList[i].type == "DT":
            i += 1
            list_()
        else:
            syntaxError("Syntax Error")
    

    def list_():
        global i, tokenList
        if tokenList[i].type == "SEMI":
            i += 1
            
            dec()
        elif tokenList[i].type == "COM":
            i += 1
            if tokenList[i].type == "ID":
                i += 1
                list_()
        elif tokenList[i].type in ['DIV', 'MIN', 'SUB', 'ADD','RELATION']:
            exp()
        else:
            syntaxError("Syntax Error")
            
    def when_otherwise():
        global i, tokenList
        if tokenList[i].type == "WHEN":
            i += 1
            if tokenList[i].type == "O_PARAM":
                i += 1
                exp()
                if tokenList[i].type == "C_PARAM":
                    i += 1
                    if tokenList[i].type == "O_BRACE":
                        i += 1
                        body()
                        if tokenList[i].type == "C_BRACE":
                            i += 1
                            
                        if_else_tail()
        syntaxError("Syntax Error: Missing 'WHEN' in 'when' statement")

    def if_else_tail():
        global i, tokenList
        if tokenList[i].type == "CHECK":
            i += 1
            if tokenList[i].type == "O_PARAM":
                i += 1
                exp()
                if tokenList[i].type == "C_PARAM":
                    i += 1
                    if tokenList[i].type == "O_BRACE":
                        i += 1
                        body()
                        if tokenList[i].type == "C_BRACE":
                            i += 1
                            if_else_tail()
                    else:
                        syntaxError(
                            "Syntax Error: Missing ':' after condition in 'check' statement")
                else:
                    syntaxError(
                        "Syntax Error: Missing ')' after condition in 'check' statement")
        elif tokenList[i].type == "OTHERWISE":
            i += 1
            if tokenList[i].type == "O_BRACE":
                i += 1
                body()
                if tokenList[i].type == "C_BRACE":
                    i += 1
                if_else_tail()
            else:
                syntaxError("Syntax Error: Missing ':' after 'otherwise'")
        else:
            return True # Epsilon case
                
    def for_loop():
        global i, tokenList
        if tokenList[i].type == "FOR":
            i += 1
            if tokenList[i].type == "LP":
                i += 1
                for_loop_init()
                if tokenList[i].type == "SEMI":
                    i += 1
                    cond()
                    if tokenList[i].type == "SEMI":
                        i += 1
                        update()
                    if tokenList[i].type == "RP":
                        i += 1
                        if tokenList[i].type == "LB":
                            i += 1
                            body()
                            if tokenList[i].type == "RB":
                                i += 1
                                return True
                            else:
                                syntaxError("Syntax Error: Missing '}'")
                        else:
                            syntaxError("Syntax Error: Missing '{'")
                    else:
                        syntaxError("Syntax Error: Missing ')'")
                else:
                    syntaxError("Syntax Error: Missing ';'")
            else:
                syntaxError("Syntax Error: Missing ';' after condition")
        else:
            syntaxError("Syntax Error: Missing '('")
    # else:
    #     syntaxError("Syntax Error: Missing 'ITERATE'")
    
    def for_loop_init():
        global i, tokenList
        if tokenList[i].type == "DT":
            i += 1
            if tokenList[i].type == "ID":
                i += 1
                if tokenList[i].type == "ASS":
                    i += 1
                    if tokenList[i].type in ['ID', 'INT', 'FT', 'STR', 'CR']:
                        i+=1
                        return True
        else:
            syntaxError("Syntax Error")
    
    def cond():
        global i, tokenList

        if tokenList[i].type in ["ID", "INT", "FT", "STR","CR","L_NOT"]: 
        
            exp()
            
        else:
            return True # Epsilon case
        
    def update():
        global i, tokenList
        if tokenList[i].type == "ID":
            i += 1
            if tokenList[i].type in ["INC", "DEC"]:
                i += 1
                return True
        else:
            return True # Epsilon case
        
    def assign_st():
        global i, tokenList
        if tokenList[i].type == "ID":
            i += 1
            assignop()
            exp()
        else:
            syntaxError("Syntax Error: Missing ID in assignment statement")

    def assignop():
        global i, tokenList
        if tokenList[i].type in ["ASSIGN", "COMBO_ASSIGN"]:
            i += 1
        else:
            syntaxError("Syntax Error: Invalid assignment operator")
            
    def param():
        exp()
        param2()

    def param2():
        global i, tokenList
        if tokenList[i].type == "COM":
            i += 1
            exp()
            param2()
        else:
            return True # Epsilon case
    
    def func_def():
        global i, tokenList
        if (tokenList[i].type == "DT" or tokenList[i].type == "VD"):
            i+=1
            if tokenList[i].type == "DEF":
                i += 1
                if tokenList[i].type == "ID":
                    i += 1
                    if tokenList[i].type == "LP":
                        i += 1
                        args()
                        if tokenList[i].type == "RP":
                            i += 1
                            if tokenList[i].type == "LB":
                                i += 1
                                #body()
                                if tokenList[i].type == "RB":
                                    i += 1
                                    return True
                                
        syntaxError("Syntax Error: Missing 'DEFINE' keyword in function definition")
    
    def args():
        global i, tokenList
        if tokenList[i].type == "DT":
            i += 1
            if tokenList[i].type == "ID":
                i += 1
                n_args()
                
                syntaxError("Syntax Error: Missing data type in function arguments")
    
    def n_args():
        global i, tokenList
        if tokenList[i].type == "SEPARATOR":
            i += 1
            if tokenList[i].type == "DT":
                i += 1
                if tokenList[i].type == "ID":
                    i += 1
                    n_args()
            syntaxError("Syntax Error: Missing data type in function arguments")
        else:
            return True # Epsilon case
        syntaxError("Syntax Error: Missing data type in function arguments")
        
    def assign_st():
        global i, tokenList
        if tokenList[i].type == "ID":
            i += 1
            if tokenList[i].type == "ASS":
                i += 1
                exp()
        syntaxError("Syntax Error: Missing variable name in assignment statement")

    def inc_dec_st():
        global i, tokenList
        if tokenList[i].type in ["ID", "STR", "CR", "FT", "INT"]:
            i += 1
            exp()
            inc_dec_op()
        else:
            syntaxError("Syntax Error: Missing identifier or value for increment/decrement statement")

    def inc_dec_op():
        global i, tokenList
        if tokenList[i].type in ["INC", "DEC"]:
            i += 1
        else:
            syntaxError("Syntax Error: Invalid increment/decrement operator")
   
    def exp():
        if a():
            return True
        if exp_prime():
            return True
        return False

    def exp_prime():
        global i, tokenList
        if tokenList[i].type == "OR":
            i += 1
            if a():
                return True
            if exp_prime():
                return True
        return False
    
    def a():
        if r():
            return True
        if a_prime():
            return True
        return False

    def a_prime():
        global i, tokenList
        if tokenList[i].type == "AND":
            i += 1
            if r():
                return True
            if a_prime():
                return True
        return False

    def r():
        if e():
            return True
        if r_prime():
            return True
        return False

    def r_prime():
        global i, tokenList
        if tokenList[i].type == "RELATION":
            i += 1
            if e():
                return True
            if r_prime():
                return True
        return False            
    
    def e():
        if t():
            return True
        if e_prime():
            return True
        return False

    def e_prime():
        global i, tokenList
        if tokenList[i].type == "PM" or tokenList[i+1].type =="ASSIGN":
            i += 1
            if t():
                return True
            if e_prime():
                return True
        return False

    def t():
        if f():
            return True
        if t_prime():
            return True
        return False

    def t_prime():
        global i, tokenList
        if tokenList[i].type == "M_D_M":
            i += 1
            if f():
                return True
            if t_prime():
                return True
        return False
    
    def f():
        global i, tokenList
        if tokenList[i].type == "ID":
            i += 1
            f_init()
        elif tokenList[i].type in ["INT", "FLT", "STR", "CHAR"]:
            i+=1
            return True
        elif tokenList[i].type == "NOT":
            i += 1
            if f():
                return True
        elif tokenList[i].type == "CALLING":
            i += 1
            func_call()
        syntaxError("Syntax Error: Expected ID or literal")

    def f_init():
        global i, tokenList
        if tokenList[i].type == "O_BRACK":
            i += 1
            exp()
            if tokenList[i].type == "C_BRACK":
                i += 1
                f_init()
        elif tokenList[i].type == "ID":
            i += 1
            f_init()
        elif tokenList[i].type == "INC_DEC":
            i += 1
        else:
            return True
    def f_init_tail():
        global i, tokenList
        if tokenList[i].type == "ID":
            i += 1
            f_init()
        elif tokenList[i].type == "O_BRACK":
            i += 1
            exp()
            if tokenList[i].type == "C_BRACK":
                i += 1
                f_init()
        else:
            return True
        
    def func_call():
        global i, tokenList
        if tokenList[i].type == "ID":
            i += 1
            if tokenList[i].type == "O_PARAM":
                i += 1
                param()
                if tokenList[i].type == "C_PARAM":
                    i += 1
                    return True
        syntaxError(
            "Syntax Error: Missing function name in function call")
        
    def param():
        exp()
        param2()

    def param2():   
        global i, tokenList
        if tokenList[i].type == "COM":
            i += 1
            exp()
            param2()
        else:
            return True
    
except LookupError:
    print("Tree Incomplete... Input Completely Parsed")

