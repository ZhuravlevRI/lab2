import os
import os.path
import stat


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

