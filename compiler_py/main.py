from arit_tokenizer import Lexer
from wrt_log import TraceFile
import arit_parser
import sys
import argparse

if __name__ == '__main__':
    filename = ""
    argp = argparse.ArgumentParser(description='pycompiler.')
    argp.add_argument('filename', help='O nome do arquivo a ser compilado.')
    argp.add_argument('-o', '--output', help='o nome do arquivo de saida.')
    argp.add_argument('-d', '--debuglvl', help='nivel de debug.',required=False)
    args = argp.parse_args()
    debuglvl = args.debuglvl
    if len(sys.argv) < 3 :
        print(f'{sys.argv[0]} usage:')
        print(f'{sys.argv[0]} arq_de_entrada -o arq_de_saida')
    
    contents = ""
    with open(args.filename, 'r') as fp:
        contents = fp.read()
    
    if contents == "":
        exit(-1)

    
    lexer = Lexer(contents)
    lexer.generate_token_code()
    TraceFile.write_log(msg=str(lexer.token_code), fnc="__main__")
    parser = arit_parser.Parser(lexer.token_code, lexer)
 
    with open(args.output, 'w') as fo:
        contents = fo.write()
