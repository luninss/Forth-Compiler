import ply.lex as lex

literals = ['(', ')', '=', '.']
tokens = (
    'SINAL',
    'NUM',
    'ID',
    'PRINT'
)

t_SINAL = r'\+|-|\*|\/|%'

def t_eof(t):
    return None  # To stop parsing

def t_NUM(t):
    r'\d+'
    return t

def t_ID(t):
    r'[a-zA-Z]+'
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
