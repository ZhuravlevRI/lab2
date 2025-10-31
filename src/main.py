import os
import os.path
import shlex
import stat

import commands
import functions


def run():
    initial_path = os.path.abspath('..')
    os.chdir(os.path.expanduser('~'))
    path = os.path.abspath('.')
    error_message = ''
    output = ''
    while True:
        try:
            if error_message:
                print(error_message)
                functions.log(initial_path, error_message)
                error_message = ''
            if output:
                print(output)
                output = ''

            inp = shlex.split(input(f'{path} '))
            functions.log(initial_path, f'{path} ' + ' '.join(inp))

            if len(inp) == 0:
                pass
            if inp[0] == 'ls':
                inp.append('.')
                detailed = inp[1] == '-l'
                ls_path = functions.get_abs_path(path, inp[1 + int(detailed)])
                try:
                    output = commands.ls(ls_path, detailed)
                except FileNotFoundError:
                    error_message = 'ERROR: No such file or directory'
                except PermissionError:
                    error_message = 'ERROR: Permission denied'

            elif inp[0] == 'cd':
                try:
                    if inp[1] == '~':
                        cd_path = os.path.expanduser('~')
                    else:
                        cd_path = functions.get_abs_path(path, inp[1])
                    # print(cd_path)
                    commands.cd(cd_path)
                    path = cd_path
                except IndexError:
                    pass
                except FileNotFoundError:
                    error_message = 'ERROR: No such file or directory'
                except PermissionError:
                    error_message = 'ERROR: Permission denied'

            elif inp[0] == 'cat':
                try:
                    cat_path = functions.get_abs_path(path, inp[1])
                    if not stat.S_ISDIR(os.stat(cat_path).st_mode):
                        output = commands.cat(cat_path)
                    else:
                        error_message = 'ERROR: cat: operand should not be a directory'
                except IndexError:
                    error_message = 'ERROR: cat: missing operand'
                except FileNotFoundError:
                    error_message = 'ERROR: No such file or directory'
                except PermissionError:
                    error_message = 'ERROR: Permission denied'
                except UnicodeDecodeError:
                    error_message = 'ERROR: Failed to read file'

            elif inp[0] == 'cp':
                try:
                    recursion = inp[1] == '-r'
                    cp_src = functions.get_abs_path(path, inp[1 + int(recursion)])
                    cp_dst = functions.get_abs_path(path, inp[2 + int(recursion)])
                    commands.cp(cp_src, cp_dst, recursion)
                except IndexError:
                    error_message = 'ERROR: cp: missing operand'
                except FileNotFoundError:
                    error_message = 'ERROR: No such file or directory'
                except PermissionError:
                    error_message = 'ERROR: Permission denied'

            elif inp[0] == 'mv':
                try:
                    mv_src = functions.get_abs_path(path, inp[1])
                    mv_dst = functions.get_abs_path(path, inp[2])
                    commands.mv(mv_src, mv_dst)
                except IndexError:
                    error_message = 'ERROR: mv: missing operand'
                except FileNotFoundError:
                    error_message = 'ERROR: No such file or directory'
                except PermissionError:
                    error_message = 'ERROR: Permission denied'

            elif inp[0] == 'rm':
                try:
                    recursion = inp[1] == '-r'
                    rm_path = inp[1 + int(recursion)]
                    if rm_path == '..' and rm_path == '/':
                        error_message = f'ERROR: Cannot delete {rm_path}'
                    else:
                        rm_path = functions.get_abs_path(path, rm_path)
                        confirmation = input(f'Delete {rm_path}?\n[Y/n] ').strip() == 'Y' or 'y'
                        if confirmation:
                            commands.rm(rm_path, recursion)
                        else:
                            error_message = 'Operation cancelled'
                except IndexError:
                    error_message = 'ERROR: rm: missing operand'
                except FileNotFoundError:
                    error_message = 'ERROR: No such file or directory'
                except PermissionError:
                    error_message = 'ERROR: Permission denied'
            elif inp[0] == 'exit':
                return
            else:
                error_message = f'ERROR: No such command: {inp[0]}'

        except KeyboardInterrupt:
            return
        except Exception:
            error_message = 'ERROR: Unexpected exception'


if __name__ == '__main__':
    run()
