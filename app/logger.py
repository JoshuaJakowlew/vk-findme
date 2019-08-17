
_log = ''

def log(text):
    print(text)
    global _log
    _log += '{}\n'.format(text)

def flush():
    with open('log.txt', 'wb') as log_file:
        log_file.write(_log.encode('utf-8'))