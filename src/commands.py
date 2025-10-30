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
            stats = os.stat(elem)
            mode = stats.st_mode
            size = ''
            mod_time = time.gmtime(0)
            if not stat.S_ISDIR(mode):
                size = stats.st_size
                mod_time = time.gmtime()
            output.append(tuple([mode, size, time.strftime("%d/%m/%Y %H:%M:%S", mod_time), name]))
        output = tabulate.tabulate(output)

    return output


print(ls('/', detailed=True))
