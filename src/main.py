import functions
import commands
import os
import os.path
import stat
import shutil
import time
import tabulate


def run():
    os.chdir(os.path.expanduser('~'))
    path = os.path.abspath('.')
    message = ''
    while True:
        print(message)
        inp = input(f'{path} ').split()
        if inp[0] == 'ls':
            detailed = inp[1] == '-l'
            ls_path = inp[1 + int(detailed)]
            if not os.path.isabs(ls_path):
                ls_path = path + ls_path
            try:
                message = commands.ls(ls_path, detailed)
            except FileNotFoundError:
                message = 'ERROR: No such file or directory'
            except PermissionError:
                message = 'ERROR: Permission denied'
        if inp[0] == 'cd':
            cd_path = inp[1]
            if not os.path.isabs(cd_path):
                cd_path = path + cd_path
            try:
                message = commands.cd(cd_path)
            except FileNotFoundError:
                message = 'ERROR: No such file or directory'
            except PermissionError:
                message = 'ERROR: Permission denied'


if __name__ == '__main__':
    run()
