import ply.yacc as yacc
import ply.lex  as lex

import sys

from lexer import tokens


def p_Inicio(p):
    """
    Inicio : Prog
    """
    p[0]  = 'pushn ' + str(parser.next_addr) + '\n'
    p[0] += 'start\n'
    p[0] += p[1]
    p[0] += 'stop\n'
    return p


def p_Prog(p):
    """
    Prog : Prog Frase
    """
    p[0] = p[1] + p[2]
    return p

def p_Prog2(p):
    """
    Prog : Frase
    """
    p[0] = p[1]
    return p

def p_Frase(p):
    """
    Frase : Expressao PRINT
    """
    p[0] = p[1] + 'writei\n'
    return p

def p_Frase2(p):
    """
    Frase : Expressao
    """
    p[0] = p[1]
    return p

def p_Expressao_Print(p):
    """
    Expressao : Expressao '.'
    """
    p[0] = p[1] + 'writei\n'
    return p

def p_Expressao_soma(p):
    """
    Expressao : Expressao Expressao SINAL 
    """
    # Directly use the numbers on the stack for addition
    if p[3] == '+':
        p[0] = p[1] + p[2] + 'ADDd\n'
    elif p[3] == '-':
        p[0] = p[1] + p[2] + 'SUB\n'
    elif p[3] == '*':
        p[0] = p[1] + p[2] + 'MUL\n'
    elif p[3] == '/':
        p[0] = p[1] + p[2] + 'DIV\n'
    elif p[3] == '%':
        p[0] = p[1] + p[2] + 'MOD\n'
    return p


def p_Expressao_atom(p):
    """
    Expressao : atom
    """
    p[0] = p[1]
    return p


def p_atom_num(p):
    """
    atom : NUM
    """
    p[0] = 'pushi ' + str(p[1]) + '\n'
    return p

def p_atom_id(p):
    """
    atom : ID
    """
    if p[1] in parser.tab_id.keys():
        p[0] = 'pushg ' + str(parser.tab_id[p[1]]) + '\n'
    else:
        print("Variavel nao declarada")


def p_error(p):
    print('-----/-----')
    print('erro: ')
    print(p)
    print("Erro Sintático! Reescreva a frase")
    print('-----/-----')
    parser.exito = False


parser = yacc.yacc()
parser.exito = True
parser.tab_id = {}
parser.next_addr = 0

fonte = ""
for linha in sys.stdin:
    fonte += linha

codigo = parser.parse(fonte)


if parser.exito:
    print("Parsing terminou com sucesso")
    print(codigo)  # escrever este codigo para um ficheiro em vez de imprimir

def debug_lexer(fonte):
    lex.input(fonte)

    #while tok := lex.token():
    #    print(tok)

debug_lexer(fonte)
