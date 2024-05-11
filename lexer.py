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
    'KEY',
    # 'DO',
)

# def t_DO(t):
#     r'DO'
#     return t

def t_KEY(t):
    r'[Kk][Ee][Yy]'
    return t

def t_SINAL(t):
    r'\+|\-|\*|\/|\<|\>|\=|\%'
    return t

def t_IF(t):
    r'[Ii][Ff]'
    return t

def t_ELSE(t):
    r'[Ee][Ll][Ss][Ee]'
    return t

def t_THEN(t):
    r'[Tt][Hh][Ee][Nn]'
    return t

def t_NOT(t):
    r'[Nn][Oo][Tt]'
    return t

def t_2DUP(t):
    r'2[Dd][Uu][Pp]'
    return t

def t_ROT(t):
    r'[Rr][Oo][Tt]'
    return t

def t_SPACES(t):
    r'[Ss][Pp][Aa][Cc][Ee][Ss]'
    return t

def t_SPACE(t):
    r'[Ss][Pp][Aa][Cc][Ee]'
    return t

def t_ARGUMENTOS(t):
    r'\(.*\)'
    return t

def t_CR(t):
    r'[Cc][Rr]'
    return t

def t_DROP(t):
    r'[Dd][Rr][Oo][Pp]'
    return t

def t_OVER(t):
    r'[Oo][Vv][Ee][Rr]'
    return t

def t_SWAP(t):  
    r'[Ss][Ww][Aa][Pp]'
    return t

def t_DUP(t):
    r'[Dd][Uu][Pp]'
    return t

def t_eof(t):
    return None 

def t_EMIT(t):
    r'[Ee][Mm][Ii][Tt]' 
    return t

def t_CHAR(t):
    r'[Cc][Hh][Aa][Rr]'
    return t

def t_DEFVARIABLE(t):
    r'[Vv][Aa][Rr][Ii][Aa][Bb][Ll][Ee]'
    return t

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    return t


def t_NUM(t):
    r'\d+'
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
