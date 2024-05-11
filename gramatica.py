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
         | Def
    """
    p[0] = p[1]
    return p

def p_Def(p):
    """
    Def : ':' ID ARGUMENTOS Prog ';'
        | ':' ID Prog ';'
    """
    print('entrei')
    print(p[1])
    if len(p) == 6:
        parser.tab_func[p[2]] = p[4]
    else :
        parser.tab_func[p[2]] = p[3] 
    p[0] = ''
    return p



def p_Frase(p):
    """
    Frase : DUP
    """
    p[0] = 'dup 1\n'
    return p

def p_Frase1(p):
    """
    Frase : EMIT
    """
    p[0] = 'writechr\n'
    return p

def p_Frase2(p):
    """
    Frase : CHAR ID
          | CHAR NUM
          | CHAR STRING
          | CHAR STRINGPONTO
          | CHAR SINAL
    """
    p[0] = f'pushs ' + "\"" +  f'{p[2][0]}' + "\"" + '\nchrcode\n'
    return p

def p_Frase3(p):
    """
    Frase : Var
    """
    p[0] = p[1]
    return p

def p_Frase4(p):
    """
    Frase : Expressao
    """
    p[0] = p[1]
    return p

def p_Frase5(p):
    """
    Frase : SWAP
    """
    p[0] = 'swap\n'
    return p

def p_Frase6(p):
    """
    Frase : OVER
    """
    p[0] = 'pushsp\nload-1\n'
    return p

def p_Frase7(p):
    """
    Frase : DROP
    """
    p[0] = 'pop 1\n'
    return p

def p_Frase8(p):
    """
    Frase : CR
    """
    p[0] = 'writeln\n'
    return p

def p_Frase9(p):
    """
    Frase : SPACE
    """
    p[0] = 'pushs \" \"\nwrites\n'
    return p

def p_Frase10(p):
    """
    Frase : SPACES
    """
    p[0] = 'pusha space\ncall\n'
    parser.spaces_called = True
    return p

def p_Frase11(p):
    """
    Frase : ROT
    """
    numero = parser.next_addr
    parser.next_addr += 3
    p[0] = 'storeg ' + str(numero) + '\nstoreg ' + str(numero + 1) + '\nstoreg ' + str(numero + 2) + '\npushg ' + str(numero +1) + '\npushg ' + str(numero) + '\npushg ' + str(numero + 2) + '\n'
    return p

def p_Frase12(p):
    """
    Frase : NOT
    """
    p[0] = 'not\n'
    return p

def p_Frase13(p):
    """
    Frase : 2DUP
    """
    p[0] = 'pushsp\nload-1\npushsp\nload-1\n'
    return p

def p_Frase14(p):
    """
    Frase : KEY
    """
    p[0] = 'read\natoi\n'
    return p

def p_Expressao_Cond(p):
    """
    Expressao : IF Prog THEN
              | IF Prog ELSE Prog THEN
    """
    if len(p) == 4:
        p[0] = 'jz continue' + str(parser.next_if) + '\n' 
        p[0]+= p[2]
        p[0] += 'continue' +  str(parser.next_if) + ':\n'
        parser.next_if += 1
    elif len(p) == 6:
        p[0] = 'jz else' + str(parser.next_if) + '\n' 
        p[0]+=  p[2]
        p[0] += 'jump continue' +  str(parser.next_if) + '\n'
        p[0] += 'else' +  str(parser.next_if) + ':\n'
        p[0] += p[4]
        p[0] += 'continue' +  str(parser.next_if) + ':\n'
        parser.next_if += 1
    return p

def p_Expressao_Print(p):
    """
    Expressao : STRINGPONTO
    """
    if p[1][2] == ' ':
        palavra = p[1][3:]
        p[0] = 'pushs ' + "\"" +  palavra + '\nwrites\n'
    else :
        parser.exito = False
        p[0] = ''
    return p

def p_Expressao_Print2(p):
    """
    Expressao : '.'
    """
    p[0] = 'writei\npushs \" \"\nwrites\n'
    return p

def p_Expressao_sinal(p):
    """
    Expressao : SINAL 
    """
    if p[1] == '+':
        p[0] = 'ADD\n'
    elif p[1] == '-':
        p[0] = 'SUB\n'
    elif p[1] == '*':
        p[0] =  'MUL\n'
    elif p[1] == '/':
        p[0] =  'DIV\n'
    elif p[1] == '%':
        p[0] =  'MOD\n'
    elif p[1] == '<':
        p[0] =  'INFEQ\n'
    elif p[1] == '>':
        p[0] =  'SUP\n'
    elif p[1] == '=':
        p[0] =  'EQUAL\n'
    return p


def p_Expressao_atom(p):
    """
    Expressao : Numero
              | Numero ID '@'
              | Numero Palavra
    """
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        if p[2] in parser.tab_id.keys():
            p[0] = p[1] + 'pushg ' + str(parser.tab_id[p[2]]) + '\n' # push global do endereço da variavel que vai tirar ao dicionario
        else:
            print("Variavel nao declarada")
            print(p[2])
            p[0]=''
    elif len(p) == 3:
        p[0] = p[1] + p[2]
    return p

def p_Expressao_atom2(p):
    """
    Expressao : Palavra
    """
    p[0] = p[1]
    return p

def p_Var1(p):
    """
    Var : DEFVARIABLE ID
    """
    if p[2] not in parser.tab_id.keys():
        parser.tab_id[p[2]] = parser.next_addr
        parser.next_addr += 1
    p[0] = ''
    return p

def p_Var2(p):
    """
    Var : Numero ID '!' 
    """
    if p[2] in parser.tab_id.keys():
        p[0] = p[1] + 'storeg ' + str(parser.tab_id[p[2]]) + '\n' # pop global do endereço da variavel que vai tirar ao dicionario
    else:
        print("Variavel nao declarada")
        print(p[1])
        p[0]=''
    return p

def p_Var3(p):
    """
    Var : ID '?'
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
    Var : ID '@'
    """
    if p[1] in parser.tab_id.keys():
        p[0] = 'pushg ' + str(parser.tab_id[p[1]]) + '\n' # push global do endereço da variavel que vai tirar ao dicionario
    else:
        print("Variavel nao declarada")
        print(p[1])
        p[0]=''
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
        p[0] = ''
        # erro("Funcao nao declarada")
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
    print(codigo)  # escrever este codigo para um ficheiro em vez de imprimir

def debug_lexer(fonte):
    lex.input(fonte)
    while tok := lex.token():
       print(tok)

debug_lexer(fonte)
