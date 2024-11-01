import sys
import ply.lex as plylex
import ply.yacc as plyyacc
from app.compiler.lex import *
from app.compiler.yacc import *

lexer = plylex.lex()
parser = plyyacc.yacc()

if __name__=='__main__':
    if len(sys.argv) == 0 or sys.argv[0] == "yacc":
        while True:
            s = input('query> ')
            if not s: break
            s = s.lower()
            result = parser.parse(s)

    elif sys.argv[0] == "lex":
        while(True):
            s = input("query> ")
            if not s:
                break
            s = s.lower() 
            lexer.input(s)
            print('=======Tokens=======')
            while True:
                tok = lexer.token()
                if not tok:
                    break
                print("\t", tok.value, "\t:\t", tok.type, sep="")
            print('====================')
            