from wrt_log import write_log
from arit_tokenizer import Lexer
from arit_parser import Parser
import sys
import argparse

# dbglevel = -1
def exit_error(message):
    write_log(message,"main")
    print(f'{message} Aborting...')
    exit(-1)

if __name__ == '__main__':
    filename = ""
    argp = argparse.ArgumentParser(description='pycompiler.')
    argp.add_argument('filename', help='O nome do arquivo a ser compilado.')
    argp.add_argument('-o', '--output', help='o nome do arquivo de saida.')
    args = argp.parse_args()
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
    write_log(lexer.token_code, "__main__")
    parser = Parser(lexer.token_code, lexer)
