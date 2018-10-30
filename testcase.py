from termcolor import colored
def test(exe_fct, exec_path):
    test_str = 'abc def ghi\njkl\nmno\nquit\n'
    concat_str = 'abc def ghijklmno'
    result = exe_fct(test_str, exec_path)
    if result is None:
        print(colored('test case timeout', 'red'))
    else:
        if concat_str in result.decode():
            print(colored('test case succeed', 'green'))
            return True
        else:
            print(colored('test case does not match', 'red'))
            print('-----------')
            print('------expecting--------')
            print(concat_str)
            print('------having-----------')
            print(result.decode())
            print('------end of test------')



    return False
