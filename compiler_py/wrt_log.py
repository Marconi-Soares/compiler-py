from datetime import datetime


def write_log(msg, fnc=""):
    with open('compiler.log', 'a') as file:
        file.write(f'[{datetime.now()}]{fnc}: {msg}')
        file.write('\n')

