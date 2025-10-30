import os
import os.path
import stat
import time

import tabulate


def ls(path=None, detailed=False):
    dirlist = os.scandir(path)
    if not detailed:
        output = ''
        for elem in dirlist:
            name = elem.name
            if ' ' in name:
                output += "'" + name + "' "
            else:
                output += name + ' '

    else:
        output = []
        for elem in dirlist:
            name = elem.name
            stats = elem.stat()
            mode = stats.st_mode
            size = stats.st_size  # if not stat.S_ISDIR(mode) else ''
            mod_time = time.gmtime(stats.st_mtime)
            output.append(tuple([stat.filemode(mode), size, time.strftime("%d/%m/%Y %H:%M:%S", mod_time), name]))
        output = tabulate.tabulate(output)

    return output


def cd(path='~'):
    os.chdir(path)


def cat(path):
    with open(path) as file:
        return file.read()


print(ls('/', 1))
