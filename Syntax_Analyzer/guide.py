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
        if tokenList[i].type == "ST" and tokenList[i+1] == "SM":
            if tokenList[i].type == "ED" and tokenList[i+1].type == "EM":
                i += 2
                return True
        return False
    
    def body():
        multi_stm()
        
    def multi_stm():
        if tokenList[i].type == 'EOF':
            return False
        if single_stm():
            multi_stm()
            
    def single_stm():
        if tokenList[i].type == 'EOF':
            return False
        elif (tokenList[i].type == "DT" and tokenList[i+1].type != "DEFINE"):
            dec()
            single_stm()            
        elif tokenList[i].type == "ID":
            assign_st()
        elif tokenList[i].type == "CALL_FUNC":
            func_call()
            single_stm()
        elif tokenList[i].type in ["INC", "DEC"]:
            inc_dec_st()
        elif tokenList[i].type == "IF":
            if_else()
            single_stm()
        elif (tokenList[i].type in ['DT', 'VOID'] and tokenList[i+1].type == "DEF"):
            func_def()
            single_stm()
            
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
            
    def if_else():
        global i, tokenList
        if tokenList[i].type == "IF":
            i += 1
            if tokenList[i].type == "LP":
                i += 1
                exp()
                if tokenList[i].type == "RP":
                    i += 1
                    if tokenList[i].type == "LC":
                        i += 1
                        body()
                        if tokenList[i].type == "RC":
                            i += 1
                            
                        if_else_tail()
        syntaxError("Syntax Error: Missing 'IF' in 'if' statement")

    def if_else_tail():
        global i, tokenList
        if tokenList[i].type == "ELIF":
            i += 1
            if tokenList[i].type == "LP":
                i += 1
                exp()
                if tokenList[i].type == "RP":
                    i += 1
                    if tokenList[i].type == "LC":
                        i += 1
                        body()
                        if tokenList[i].type == "RC":
                            i += 1
                            if_else_tail()
                    else:
                        syntaxError(
                            "Syntax Error: Missing ':' after condition in 'check' statement")
                else:
                    syntaxError(
                        "Syntax Error: Missing ')' after condition in 'check' statement")
        elif tokenList[i].type == "ELSE":
            i += 1
            if tokenList[i].type == "LC":
                i += 1
                body()
                if tokenList[i].type == "RC":
                    i += 1
                if_else_tail()
            else:
                syntaxError("Syntax Error: Missing ':' after 'else'")
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
        if tokenList[i].type in ["ASS", "ADD_ASS", "MINUS_ASS", "MULTI_ASS", "DIV_ASS", "MOD_ASS"]:
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
    #     
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
        if and_op():
            return True
        if exp_or():
            return True
        return False

    def exp_or():
        global i, tokenList
        if tokenList[i].type == "OR":
            i += 1
            if and_op():
                return True
            if exp_or():
                return True
        return False
    
    def and_op():
        if rel_op():
            return True
        if a_prime():
            return True
        return False

    def a_prime():
        global i, tokenList
        if tokenList[i].type == "AND":
            i += 1
            if rel_op():
                return True
            if a_prime():
                return True
        return False

    def rel_op():
        if e():
            return True
        if rel_exp():
            return True
        return False

    def rel_exp():
        global i, tokenList
        if tokenList[i].type in ["L_OR", "L_AND", "E", "NE", "INT"]:
            i += 1
            if e():
                return True
            if rel_exp():
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
        if tokenList[i].type in ["ADD", "MIN"] or tokenList[i+1].type =="ASS":
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
        if tokenList[i].type in ["MUL", "DIV", "MOD"]:
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
        elif tokenList[i].type in ["INT", "FT", "STR", "CR"]:
            i+=1
            return True
        elif tokenList[i].type == "L_NOT":
            i += 1
            if f():
                return True
        elif tokenList[i].type == "CALLING":
            i += 1
            func_call()
        syntaxError("Syntax Error: Expected ID or literal")

    def f_init():
        global i, tokenList
        if tokenList[i].type == "LB":
            i += 1
            exp()
            if tokenList[i].type == "RB":
                i += 1
                f_init()
        elif tokenList[i].type == "ID":
            i += 1
            f_init()
        elif tokenList[i].type in ["INC", "DEC"]:
            i += 1
        else:
            return True
    def f_init_tail():
        global i, tokenList
        if tokenList[i].type == "ID":
            i += 1
            f_init()
        elif tokenList[i].type == "LB":
            i += 1
            exp()
            if tokenList[i].type == "RB":
                i += 1
                f_init()
        else:
            return True
        
    def func_call():
        global i, tokenList
        if tokenList[i].type == "ID":
            i += 1
            if tokenList[i].type == "LP":
                i += 1
                param()
                if tokenList[i].type == "RP":
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
    

    