from wrt_log import TraceFile

def exit_error(message):
    TraceFile.write_log(msg=message)
    print(f'{message} Aborting...')
    exit(-1)
    return
