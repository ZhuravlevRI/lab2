import os
import os.path
import stat
import time


def obhod(path):  # not checked
    try:
        dirlist = os.scandir(path)
        for elem in dirlist:
            stats = elem.stat()
            if path == '/': path = ''
            if stat.filemode(stats.st_mode)[0] == 'd':
                yield from obhod(path + '/' + elem.name)
            else:
                yield path + '/' + elem.name
    except Exception:
        print('ne rabotaet:', path)


def log(initial_path, message):  # works
    with open(f'{initial_path}/log/shell.log', 'r') as f:
        prev = f.read()
    with open(f'{initial_path}/log/shell.log', 'w') as f:
        f.write(prev + time.strftime("[%Y-%m-%d %H:%M:%S] ", time.gmtime()) + message + '\n')


def get_abs_path(abs_path, cur_path):
    if not os.path.isabs(cur_path):
        return os.path.abspath(abs_path + '/' + cur_path)
    else:
        return os.path.abspath(cur_path)
