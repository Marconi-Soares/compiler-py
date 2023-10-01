# from main import dbglevel
from datetime import datetime

class TraceFile:
    debuglvl = 7 # details  
    def __init__(self,dbglvl = None) -> None:
        if dbglvl:
            TraceFile.debuglvl= dbglvl or 7

    def write_log(msg, fnc=""):
        # if dbglevel == -1:
            # return
        with open('compiler.log', 'a') as file:
            file.write(f'[{datetime.now()}]{fnc}: {msg}')
            file.write('\n')

