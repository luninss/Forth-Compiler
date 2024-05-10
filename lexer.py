import ply.lex as lex

literals = ['(', ')', '=', '.', ';', ':', "\"", '!', '?', '@']
tokens = (
    'SINAL',
    'NUM',
    'ID',
    #'PRINT',
    'EMIT',
    'STRING',
    'CHAR',
    'DEFVARIABLE',
    'DUP',
    'SWAP',
    'OVER',
    'DROP',
    'CR',
    'ARGUMENTOS',
    'SPACES',
    'SPACE',
    'ROT',
    '2DUP',
    'NOT',
    'STRINGPONTO',
    # 'LASTRESORT',
    'IF',
    'ELSE',
    'THEN',
    # 'DO',
)

# def t_DO(t):
#     r'DO'
#     return t

def t_SINAL(t):
    r'\+|\-|\*|\/|\<|\>|\=|MOD'
    return t

def t_IF(t):
    r'IF'
    return t

def t_ELSE(t):
    r'ELSE'
    return t

def t_THEN(t):
    r'THEN'
    return t

def t_NOT(t):
    r'NOT'
    return t

def t_2DUP(t):
    r'2DUP'
    return t

def t_ROT(t):
    r'ROT'
    return t

def t_SPACES(t):
    r'SPACES'
    return t

def t_SPACE(t):
    r'SPACE'
    return t

def t_ARGUMENTOS(t):
    r'\(.*\)'
    return t

def t_CR(t):
    r'CR'
    return t

def t_DROP(t):
    r'DROP'
    return t

def t_OVER(t):
    r'OVER'
    return t

def t_SWAP(t):  
    r'SWAP'
    return t

def t_DUP(t):
    r'DUP'
    return t

def t_eof(t):
    return None 

def t_EMIT(t):
    r'emit' 
    return t

def t_CHAR(t):
    r'char'
    return t

def t_DEFVARIABLE(t):
    r'VARIABLE'
    return t

def t_NUM(t):
    r'\d+'
    return t

def t_ID(t):
    r'[a-zA-Z]+'
    return t


def t_STRING(t):
    r'"([^"]*)"'
    return t


def t_STRINGPONTO(t):
    r'\."\s*([^"]+)"'
    return t

# def t_LASTRESORT(t): 
#     r'.'
#     return t

def t_error(t):
    print('Illegal character: ', t.value[0])
    t.lexer.skip(1)

t_ignore = ' \n\t'  

# Define precedence for math operators
precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
)

lexer = lex.lex()
