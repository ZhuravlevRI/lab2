import os
import os.path
import stat
import time


def obhod(path):
    try:
        dirlist = os.scandir(path)
        for elem in dirlist:
            stats = elem.stat()
            if path == '/': path = ''
            if stat.filemode(stats.st_mode)[0] == 'd':
                yield from obhod(path + '/' + elem.name)
            else:
                yield path + '/' + elem.name
    except PermissionError:
        pass    # ЗАПИСАТЬ В ЛОГ "ОТКАЗАНО В ДОСТУПЕ"!!!!!!!! ХОТЬ БЫ НЕ ЗАБЫТЬ


def log(message):
    with open(f'log/shell.log', 'w') as f:
        prev = f.read()
        f.write(prev + time.strftime("[%Y-%m-%d %H:%M:%S]", time.gmtime()) + message)
