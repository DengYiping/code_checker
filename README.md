# code_checker
Help TAs to grade homework and find possible code plagirism in the grading process
## Requirements
This program requires you to have Python 3.7 and `ccat` for coloring the code
## Installation
 - `pip install -r requirements.txt`
## usage
 - If you don't want automatic test case, modify `testcase.py` to return `False` so that you can check it manually
 - `python check.py a1_p1_r3/` this command will start checking homework under the folder `a1_p1_r3` and try to compile all the source code. Once compiled, it will compare all the solutions and give you the code similarity matrxi. It will also give you the most similar 2 of all the solutions. 
 
Afterwards, you can enter a username to check the solution.
