from termcolor import colored
def test(exe_fct, exec_path):
    test_str = '4\n1\n2\n3\n4\n'
    result = exe_fct(test_str, exec_path)
    if result is None:
        print(colored('test case timeout', 'red'))
    else:
        decoded = result.decode()
        if '-1' in decoded and '-2' in decoded and '-3' in decoded and '0' in decoded:
            print(colored('test case succeed', 'green'))
            return True
        else:
            print(colored('test case does not match', 'red'))
            print('-----------')
            print('------having-----------')
            print(decoded)
            print('------end of test------')

    return False
