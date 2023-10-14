KEYWORDS = {
    'BEGINP':   0x100,
    'FUNCTION': 0x101,
    'INT':      0x102,
    'FLOAT':    0x103,
    'IF':       0x104,
    'ELSE':     0x105,
    'WHILE':    0x106,
    'DO':       0x107,
    'OR':       0x108,
    'AND':      0x109,
    'NOT':      0x110,
    'MOD':      0x111,
    'DIV':      0x112,  
    'ADD':      0x113,
    'MUL':      0x114,
    'PARAM':    0x115,
    'ENDP':     0x116
}

def is_keyword(symbol):
    global KEYWORDS
    try:
        return KEYWORDS[symbol]
    except:
        return False

def which_keyword(value):
    for key, number in KEYWORDS.items():
        if value == number:
            return key
    return False
