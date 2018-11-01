import subprocess
from subprocess import PIPE, Popen, STDOUT
import sys, os
import editdistance
import numpy as np
from testcase import test

def exe_command(command_str, path):
    # execute a command and return stdout and stderr
    result = subprocess.run(command_str.split(' '), cwd = path, capture_output = True)
    stdout = result.stdout.decode()
    stderr = result.stderr.decode()
    return_code = result.returncode

    return stdout, stderr, return_code

def compile_file(fname, path):
    compile_str = f'g++ -Wall -o test {fname}'
    return exe_command(compile_str, path)

def exec_test_case(test_str, exec_path):
    proc = subprocess.Popen([exec_path], stdout = PIPE, stderr = PIPE, stdin = PIPE)
    try:
        outs, errs = proc.communicate(input = test_str.encode('ascii'), timeout = 1)
        return outs
    except subprocess.TimeoutExpired:
        proc.kill()
        return None

def main():
    if len(sys.argv) != 2:
        print('wrong number of arguments')
        exit(1)

    folder_path = sys.argv[1]
    dirs = [dir for dir in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, dir))]

    compiled_set = set()

    for dir in dirs:
        full_dir_path = os.path.join(folder_path, dir)

        print(f'checking: {dir}')

        cpp_list = [x for x in os.listdir(full_dir_path) if '.cpp' in x]

        if not os.path.isfile(os.path.join(full_dir_path, 'test')):
            stdout, stderr, code = compile_file(' '.join(cpp_list), full_dir_path)

            if code != 0 or len(stdout) != 0 or len(stderr) != 0:
                print('error on compiling!')
                print(stdout, stderr)
            else:
                print('compiled!')
                compiled_set.add(dir)
        else:
            compiled_set.add(dir)
            print('already compiled')

    print('-----check code similarity------')

    similarity = np.zeros((len(dirs), len(dirs)))
    for i in range(len(dirs) - 1):
        for j in range(i + 1, len(dirs)):
            i_dir = dirs[i]
            j_dir = dirs[j]
            i_full_path = os.path.join(folder_path, i_dir)
            j_full_path = os.path.join(folder_path, j_dir)

            cpp_list = [x for x in os.listdir(i_full_path) if '.cpp' in x]
            sum = 0
            for cpp in cpp_list:
                try:
                    i_file = open(os.path.join(i_full_path, cpp), 'r')
                    j_file = open(os.path.join(j_full_path, cpp), 'r')

                    i_content = i_file.read()
                    j_content = j_file.read()

                    sim = editdistance.eval(i_content, j_content)
                    sum = sum + sim

                    i_file.close()
                    j_file.close()
                except:
                    print('invalid file encoding found, not valid ascii charaters in: ')
                    sum = np.Inf
                    try:

                        i_file = open(os.path.join(i_full_path, cpp), 'r')
                        i_file.read()
                        i_file.close()
                    except:
                        print(f'invalid characters found in file {i_full_path}')

                    try:

                        j_file = open(os.path.join(j_full_path, cpp), 'r')
                        j_file.read()
                        j_file.close()
                    except:
                        print(f'invalid characters found in file {j_full_path}')
                    i_file.close()
                    j_file.close()

            similarity[i][j] = sum
            similarity[j][i] = sum

    for i in range(len(dirs)):
        similarity[i][i] = np.Inf
    print(similarity)

    print('-----done code similarity check------')
    print('-----similarity report-----')
    print('min is:')
    print(np.min(similarity))
    mix_arg = np.argmin(similarity)
    x, y = np.unravel_index(mix_arg, similarity.shape)
    print(f'index at: ({x}, {y})')
    print(f'student: {dirs[x]}, {dirs[y]}')
    print('second highest:')
    similarity[x][y] = np.Inf
    similarity[y][x] = np.Inf
    print(np.min(similarity))
    mix_arg = np.argmin(similarity)
    x, y = np.unravel_index(mix_arg, similarity.shape)
    print(f'index at: ({x}, {y})')
    print(f'student: {dirs[x]}, {dirs[y]}')
    print('-----end of similarity report-----')

    while True:
        username = input('enter username:')
        if not username in dirs:
            print('not a valid username!')
        else:
            if not username in compiled_set:
                print('there are compilation error!')

            exec_path = os.path.join(folder_path, username, 'test')

            if os.path.isfile(exec_path) and not test(exec_test_case, exec_path):
                # compiled testing
                print('--------start testing---------')
                code = subprocess.call(exec_path)
                if code != 0:
                    print('return code is wrong')

            full_path = os.path.join(folder_path, username)
            cpps = ' '.join([x for x in os.listdir(full_path) if '.cpp' in x or '.h' in x])
            print('--code block--')
            subprocess.call(f'ccat {cpps}', shell = True, cwd = full_path)
            print('--------------')
            input('press enter to continue')

if __name__ == '__main__':
    main()
