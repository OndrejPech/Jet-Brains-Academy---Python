from collections import namedtuple
import re
import os
import argparse
import ast

Error = namedtuple('Stylistic', 'code message')
S001 = Error('S001', 'Too long')
S002 = Error('S002', 'Indentation is not a multiple of four')
S003 = Error('S003', 'Unnecessary semicolon')
S004 = Error('S004', 'At least two spaces required before inline comments')
S005 = Error('S005', 'TODO found')
S006 = Error('S006', 'More than two blank lines used before this line')
S007 = Error('S007', "Too many spaces after 'XXX'")
S008 = Error('S008', "Class name 'XXX' should use CamelCase")
S009 = Error('S009', "Function name 'XXX' should use snake_case")
S010 = Error('S010', "Argument name 'XXX' should be snake_case")
S011 = Error('S011', "Default argument value is mutable")
S012 = Error('S012', "Variable 'XXX' should be snake_case")


def s001_check(line, num, path):
    """If length of line exceed 79 characters, print Error message"""
    if len(line) > 79:
        print(f'{path}: Line {num}: {S001.code} {S001.message}')


def s002_check(line, num, path):
    """If Indentation is not a multiple of four, print Error message"""
    match = re.match('(\s+)\w', line)
    if match:
        all_whitespaces = match.group(1)
        if len(all_whitespaces) % 4 != 0:
            print(f'{path}: Line {num}: {S002.code} {S002.message}')


def s003_check(line, num, path):
    """If unnecessary semicolon after a statement,print Error message """
    match_comment = re.search('#', line)
    if match_comment:
        line_without_comment = line[:match_comment.start()].strip()
        if len(line_without_comment) > 0 and line_without_comment[-1] == ';':
            print(f'{path}: Line {num}: {S003.code} {S003.message}')
    else:
        match = re.search(';\n', line)
        if match:
            print(f'{path}: Line {num}: {S003.code} {S003.message}')


def s004_check(line, num, path):
    """find comment and make sure they are at least two spaces before inline comment"""
    match = re.search('#', line)
    if match:
        index = match.start()
        if index != 0 and line[index-2:index] != '  ':
            print(f'{path}: Line {num}: {S004.code} {S004.message}')


def s005_check(line, num, path):
    """find TODO string in comment """
    match = re.search('#', line)
    if match:
        index = match.start()
        match2 = re.search('TODO', line[index:], re.IGNORECASE)
        if match2:
            print(f'{path}: Line {num}: {S005.code} {S005.message}')


def s006_check(line, num, path):
    """find more than two lines in row """
    global empty_rows
    if line == '\n':
        empty_rows += 1
    else:
        if empty_rows == 3:
            print(f'{path}: Line {num}: {S006.code} {S006.message}')
        empty_rows = 0


def s007_check(line, num, path):
    """print message if there is more than one space after consturction name"""
    match = re.match('(def|class)\s{2,}', line.strip())
    if match:
        constructor = match.group(1)
        message = S007.message.replace('XXX', constructor)
        print(f'{path}: Line {num}: {S007.code} {message}')


def s008_check(line, num, path):
    """print message if class name is not CamelCase"""
    match = re.match('class (.*?)[(:]', line.strip())
    if match:
        class_name = match.group(1).strip()

        if "_" in class_name or class_name[0].islower() or class_name == class_name.upper():
            message = S008.message.replace('XXX', class_name)
            print(f'{path}: Line {num}: {S008.code} {message}')


def s009_check(line, num, path):
    """print message if function name is not snake_case"""
    match = re.match('def (.+)\(', line.strip())
    if match:
        function_name = match.group(1).strip()
        if not is_snake_case(function_name):
            message = S009.message.replace('XXX', function_name)
            print(f'{path}: Line {num}: {S009.code} {message}')


def get_py_files(directory):
    """add all py files from directory"""
    py_files = []
    if os.path.isfile(directory):
        ending = os.path.splitext(directory)[-1]
        if ending == '.py':
            py_files.append(directory)

    if os.path.isdir(directory):
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    py_files.append(os.path.join(root, file))

    return sorted(py_files)


def is_snake_case(name: str) -> bool:
    """return True if name is snake_case else False"""
    return bool(re.match('^[\da-z_]+$', name))


def get_ast_errors(directory) -> dict:
    """
    return dictionary with all S010,S011, S012 Errors inside functions
    key : two item tuple (line number, variable/argument_name)
    value: namedtuple - Error
    """
    ast_errors = dict()
    with open(directory) as file:
        tree = ast.parse(file.read())
        nodes = ast.walk(tree)
        for node in nodes:
            if isinstance(node, ast.FunctionDef):  # check function
                for argument in node.args.args:  # check argument name
                    argument_name = argument.arg
                    if not is_snake_case(argument_name):
                        ast_errors[(node.lineno, argument_name)] = S010

                for item in node.args.defaults:  # check argument
                    if isinstance(item, (ast.List, ast.Set, ast.Dict)):  # immutable
                        ast_errors[(node.lineno, 'DEFAULT')] = S012

                for no in ast.walk(node):
                    if isinstance(no, ast.Name):
                        if isinstance(no.ctx, ast.Store):  # is variable
                            variable_name = no.id
                            if not is_snake_case(variable_name):
                                ast_errors[(no.lineno, variable_name)] = S011

    return ast_errors


# argparse
parser = argparse.ArgumentParser()
parser.add_argument('path')
args = parser.parse_args()
arg = args.path

files_to_check = get_py_files(arg)

for file_name in files_to_check:
    ast_error_in_file = get_ast_errors(file_name)  # file_name is opened once here
    with open(file_name) as python_file:  # and once here, can be done BETTER
        empty_rows = 0
        for i, row in enumerate(python_file, 1):
            s001_check(row, i, file_name)
            s002_check(row, i, file_name)
            s003_check(row, i, file_name)
            s004_check(row, i, file_name)
            s005_check(row, i, file_name)
            s006_check(row, i, file_name)
            s007_check(row, i, file_name)
            s008_check(row, i, file_name)
            s009_check(row, i, file_name)
            for k, v in ast_error_in_file.items():
                if k[0] == i:
                    message_to_print = v.message.replace('XXX', k[1])
                    print(f'{file_name}: Line {i}: {v.code} {message_to_print}')
