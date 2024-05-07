import ply.lex as lex

literals = ['(', ')', '=', '.', ';', "\""]
tokens = (
    'SINAL',
    'NUM',
    'ID',
    'PRINT',
    'EMIT',
    'STRING',
    'CHAR',
)

t_SINAL = r'\+|-|\*|\/|%'

def t_eof(t):
    return None 

def t_EMIT(t):
    r'emit' 
    return t

def t_CHAR(t):
    r'char'
    return t

def t_NUM(t):
    r'\d+'
    return t

def t_ID(t):
    r'[a-zA-Z]+'
    return t

def t_STRING(t):
    r'"([^"]*)"'  # Match a space followed by any character except "
    return t

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
