import ply.yacc as yacc
import ply.lex  as lex

import sys

from lexer import tokens
import sys


def p_Inicio(p):
    """
    Inicio : Prog
    """
    p[0]  = 'pushn ' + str(parser.next_addr) + '\n'
    p[0] += 'start\n'
    p[0] += p[1]
    p[0] += 'stop\n'
    if parser.spaces_called:
        p[0] += 'space:\n   pushfp\n   load -1\n   pusha print\n   call\n   pushi 1\n   sub\n   dup 1\n   storel -1\n   not\n   jz space\n   return\n\nprint:\n   pushs \" \"\n   writes\n   RETURN'
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
    Frase : Def
    """
    p[0] = p[1]
    return p    

def p_Frase1(p):
    """
    Frase : Expressao
    """
    p[0] = p[1]
    return p


def p_Def(p):
    """
    Def :  ':' ID Prog ';'
    """
    parser.tab_func[p[2]] = p[3] 
    p[0] = ''
    return p

def p_Def2(p):
    """
    Def : ':' ID ARGUMENTOS Prog ';'
    """
    parser.tab_func[p[2]] = p[4]
    p[0] = ''
    return p


def p_Expressao_Cond(p):
    """
    Expressao : IF Prog THEN
    """
    p[0] = 'jz continue' + str(parser.next_if) + '\n' 
    p[0]+= p[2]
    p[0] += 'continue' +  str(parser.next_if) + ':\n'
    parser.next_if += 1
    return p

def p_Expressao_Cond2(p):
    """
    Expressao : IF Prog ELSE Prog THEN
    """
    p[0] = 'jz else' + str(parser.next_if) + '\n' 
    p[0]+=  p[2]
    p[0] += 'jump continue' +  str(parser.next_if) + '\n'
    p[0] += 'else' +  str(parser.next_if) + ':\n'
    p[0] += p[4]
    p[0] += 'continue' +  str(parser.next_if) + ':\n'
    parser.next_if += 1
    return p

def p_Expressao_Var(p):
    """
    Expressao : Var
    """
    p[0] = p[1]
    return p

def p_Expressao_Palavra(p):
    """
    Expressao : Palavra
    """
    p[0] = p[1]
    return p

def p_Expressao_Numero(p):
    """
    Expressao : Numero
    """
    p[0] = p[1]
    return p

def p_Expressao_Sinal(p):
    """
    Expressao : Sinal
    """
    p[0] = p[1]
    return p

def p_Expressao_OpStack(p):
    """
    Expressao : OPSTACK
    """
    p[0] = p[1]
    return p

def p_Expressao_Print(p):
    """
    Expressao : Print
    """
    p[0] = p[1]
    return p

def p_Sinal(p):
    """
    Sinal : '+'
    """
    p[0] = 'ADD\n'
    return p

def p_Sinal2(p):
    """
    Sinal : '-'
    """
    p[0] = 'SUB\n'
    return p

def p_Sinal3(p):
    """
    Sinal : '*'
    """
    p[0] = 'MUL\n'
    return p

def p_Sinal4(p):
    """
    Sinal : '/'
    """
    p[0] = 'DIV\n'
    return p

def p_Sinal5(p):
    """
    Sinal : '%'
    """
    p[0] = 'MOD\n'
    return p

def p_Sinal6(p):
    """
    Sinal : '<'
    """
    p[0] = 'INFEQ\n'
    return p

def p_Sinal7(p):
    """
    Sinal : '>'
    """
    p[0] = 'SUP\n'
    return p

def p_Sinal8(p):
    """
    Sinal : '='
    """
    p[0] = 'EQUAL\n'
    return p

def p_Print(p):
    """
    Print : STRINGPONTO
    """
    if p[1][2] == ' ':
        palavra = p[1][3:]
        p[0] = 'pushs ' + "\"" +  palavra + '\nwrites\n'
    else :
        parser.exito = False
        p[0] = ''
    return p

def p_Print1(p):
    """
    Print : '.'
    """
    p[0] = 'writei\npushs \" \"\nwrites\n'
    return p

def p_Print2(p):
    """
    Print : EMIT
    """
    p[0] = 'writechr\n'
    return p

def p_Print3(p):
    """
    Print : CHAR 
    """
    p[0] = f'pushs ' + "\"" +  p[1] + "\"" + '\nchrcode\n'
    return p

def p_Var1(p):
    """
    Var : DEF_VARIABLE
    """
    if p[1] not in parser.tab_id.keys():
        parser.tab_id[p[1]] = parser.next_addr
        parser.next_addr += 1
    p[0] = ''
    return p

def p_Var2(p):
    """
    Var : GIVE_VALUE_VARIABLE
    """
    if p[1].split()[1] in parser.tab_id.keys():
        p[0] = 'pushi ' + p[1].split()[0] + '\nstoreg ' + str(parser.tab_id[p[1].split()[1]]) + '\n'
    else:
        print("Variavel '" + p[1].split()[1] + "' nao declarada")
        p[0]=''
    return p

def p_Var3(p):
    """
    Var : PRINT_VARIABLE
    """
    if p[1] in parser.tab_id.keys():
        p[0] = 'pushg ' + str(parser.tab_id[p[1]]) + '\nwritei\n' # push global do endereço da variavel que vai tirar ao dicionario
    else:
        print("Variavel nao declarada")
        print(p[1])
        p[0]=''
    return p

def p_Var4(p):
    """
    Var : VARIABLE
    """
    if p[1] in parser.tab_id.keys():
        p[0] = 'pushg ' + str(parser.tab_id[p[1]]) + '\n' # push global do endereço da variavel que vai tirar ao dicionario
    else:
        print("Variavel nao declarada")
        print(p[1])
        p[0]=''
    return p


def p_OpStack(p):
    """
    OPSTACK : SWAP
    """
    p[0] = 'swap\n'
    return p

def p_OpStack1(p):
    """
    OPSTACK : OVER
    """
    p[0] = 'pushsp\nload-1\n'
    return p

def p_OpStack2(p):
    """
    OPSTACK : DROP
    """
    p[0] = 'pop 1\n'
    return p

def p_OpStack3(p):
    """
    OPSTACK : CR
    """
    p[0] = 'writeln\n'
    return p

def p_OpStack4(p):
    """
    OPSTACK : SPACE
    """
    p[0] = 'pushs \" \"\nwrites\n'
    return p

def p_OpStack5(p):
    """
    OPSTACK : SPACES
    """
    p[0] = 'pusha space\ncall\n'
    parser.spaces_called = True
    return p

def p_OpStack6(p):
    """
    OPSTACK : ROT
    """
    p[0] = 'storeg ' + str(parser.next_addr) + '\nswap\npushg ' + str(parser.next_addr) + '\nswap\n'
    parser.next_addr += 1
    return p

def p_OpStack7(p):
    """
    OPSTACK : NOT
    """
    p[0] = 'not\n'
    return p

def p_OpStack8(p):
    """
    OPSTACK : 2DUP
    """
    p[0] = 'pushsp\nload-1\npushsp\nload-1\n'
    return p

def p_OpStack9(p):
    """
    OPSTACK : KEY
    """
    p[0] = 'read\natoi\n'
    return p

def p_OpStack10(p):
    """
    OPSTACK : DUP
    """
    p[0] = 'dup 1\n'
    return p

def p_Numero(p):
    """
    Numero : NUM
    """
    p[0] = 'pushi ' + str(p[1]) + '\n'
    return p

def p_Palavra(p):
    """
    Palavra : ID
    """
    if p[1] in parser.tab_func.keys():
        p[0] = parser.tab_func[p[1]]
    else:
        print("Funcao nao declarada: " + p[1])
        p[0] = ''
    return p


def p_error(p):
    print('-----/-----')
    print('erro: ')
    print(p)
    print("Erro Sintático! Reescreva a frase")
    print('-----/-----')
    parser.exito = False

def erro(p):
    print('-----/-----')
    print('Erro: ')
    print(p)
    print('-----/-----')
    sys.exit(1)

parser = yacc.yacc()
parser.exito = True
parser.tab_id = {}
parser.tab_func = {}
parser.spaces_called= False
parser.next_addr = 0
parser.tab_ifs = {}
parser.next_if = 0

fonte = ""
for linha in sys.stdin:
    fonte += linha

codigo = parser.parse(fonte)


if parser.exito:
    print("\nParsing terminou com sucesso")
    print("codigo gerado:\n")
    print(codigo)  

def debug_lexer(fonte):
    lex.input(fonte)
    # while tok := lex.token():
    #    print(tok)

debug_lexer(fonte)
