# DICTIONARY
KD = {
        # keywords
        "START": "ST",
        "END": "ED",
        "INT": "INT",
        "CHAR": "CR",
        "FLOAT": "FT",
        "DOUBLE": "DB",
        "IF": "IF",
        "FOR": "FOR",
        "BOOL": "BL",
        "STR": "STR",
        "STRUCT": "SCT",
        "CONST": "CT",
        "DO": "DO",
        "WHILE": "WH",
        "ELSE":"EL"
       
    }

OD = {
    
    # operators
        "=": "ASS",
        "+=": "ADD_ASS",
        "-=": "MINUS_ASS",
        "*=": "MULTI_ASS",
        "/=": "DIV_ASS",
        "%=": "MOD_ASS",
        "+": "ADD",
        "-": "MIN",
        "*": "MUL",
        "/": "DIV",
        "%": "MOD",
        "++": "INC",
        "--": "DEC",
        "!": "L_NOT",
        "||": "L_OR",
        "&&": "L_AND",
        "==": "E",
        "!=": "NE",
        ">": "GT",
        "<": "LT",
        ">=": "GOE",
        "<=": "LOE",
        
}

DD = {
    
    # delimiters
        ";": "SEMI",
        "(": "LP",
        ")": "RP",
        "[": "LB",
        "]": "RB",
        "{": "LC",
        "}": "RC",
        "//": "SC",
        "#": "MM",
        " ": "SP",
        "'": "SQ",
        '"': "DQT",
        ":": "COL",
        ",": "COM",
        "<<": "SM",
        ">>": "EM",
}

RD = {
    
         # reserved words
        "BREAK": "BK",
        "FALSE": "FA",
        "CONT": "CON",
        "ELSE": "EL",
        "TRUE": "TR",
}

# for syntax analyzer
TOKEN_OD = set(OD.values())
TOKEN_KD = set(OD.values())
TOKEN_DD = set(OD.values())
TOKEN_RD = set(OD.values())