# for Python 3.7+


import argparse
import os
import hashlib


def choose_sorting_option():
    """user choose if he want Descending or Ascending sorting order"""

    options = ['Descending', 'Ascending']
    print('\nSize sorting options:')
    for i, op in enumerate(options, 1):
        print(f'{i}. {op}')

    print()
    while True:
        n_op = input('Enter a sorting option:\n')
        if n_op not in ('1', '2'):
            print('\nWrong option')
            continue
        else:
            return n_op


def file_sizes_dict(file_path, file_extension=None):
    """ create and return dictionary with size as key and list of path of that size as value
    if extension is specified, include only files with that extension"""
    sizes = {}
    if not file_extension:
        file_extension = ''
    for root, dirs, files in (os.walk(file_path)):
        for name in files:
            if name.endswith(file_extension):
                file_path = os.path.join(root, name)
                file_size = os.path.getsize(file_path)

                # add or update size dictionary values
                sizes.setdefault(file_size, []).append(file_path)

    return sizes


def get_file_format_from_user():
    """ ask user for file extension, return None if extension not specified """
    available_formats = ['gif', 'html', 'bin', 'rar', 'jpg', 'png', 'pdf', 'txt', 'mp3', 'py', 'csv']
    file_extension = input('Enter file format:')
    if len(file_extension) == 0:
        return None
    else:
        if file_extension not in available_formats:
            print('unknown file format')
            raise AssertionError
        else:
            return '.' + file_extension

def get_file_numbers(max_num):
    while True:
        user_input = input('\nEnter file numbers to delete\n')
        try:
            nums = set(map(lambda x: int(x), user_input.split()))
        except ValueError:
            print('Wrong format')
            continue
        else:
            # if user enter numbers of files,which not exist
            if len(nums) == 0 or not all(num in range(1, max_num + 1) for num in nums):
                print('Wrong format')
                continue
            else:
                return list(sorted(nums))




def yes_or_no(question):
    available_answers = ('yes', 'no')
    while True:
        print('\n'+question)
        answer = input()
        if answer not in available_answers:
            print('Wrong option')
            continue
        else:
            return True if answer == 'yes' else False


def print_duplicates(dictionary):
    for size, list_paths in dictionary.items():
        print()
        print(f'{size} bytes')
        for path in list_paths:
            print(path)


def print_duplicates_with_hash(dictionary):
    for f_size, hash_dic in dictionary.items():
        print(f'\n{f_size} bytes')
        for f_hash, files in hash_dic.items():
            print(f'Hash: {f_hash}')
            for num_file, file in files.items():
                print(f'{num_file}. {file}')


def get_hash_file(file):
    with open(file, 'rb') as f:
        bin_text = f.read()
        # get hash of file
        m = hashlib.md5()
        m.update(bin_text)
        return m.hexdigest()


def keep_duplicated_only(dictionary):
    """ return new dictionary with key ,values pairs
    where there is at least 2 items in values """
    return {k: v for k, v in dictionary.items() if len(v) > 1}


parser = argparse.ArgumentParser(description="print all files in this path")
parser.add_argument("user_path").required = False
args = parser.parse_args()

path = args.user_path


if not path:
    print('Directory is not specified')
    exit()

extension = get_file_format_from_user()
sized_files = file_sizes_dict(path, extension)
# keep only files, which has at least one another file of same size
# only_same_size_files = {size: files for size, files in sized_files.items() if len(files) > 1}
only_same_size_files = keep_duplicated_only(sized_files)

sort_mode = choose_sorting_option()
reverse_mode = {'1': True, '2': False}[sort_mode]

sorted_same_size_files = dict(sorted(only_same_size_files.items(), reverse=reverse_mode))  # for Python 3.7+
print_duplicates(sorted_same_size_files)

if not yes_or_no('Check for duplicates?'):  # user input
    exit()


max_file_num = 0

# create nested dict {size: {hash: :{ file_num : file}}}
main_dictionary = {}
for size, files in sorted_same_size_files.items():

    hash_dict = {}
    for file in files:
        file_hash = get_hash_file(file)
        # group the files of same hash
        hash_dict.setdefault(file_hash, []).append(file)

    hash_dict = keep_duplicated_only(hash_dict)

    # create nested dict {hash: {file_num: file}}
    numbered_hash_dict = {}
    for f_hash, files in hash_dict.items():

        # create nested dict {file_num: file}
        nums_file_dict = {}
        for file in files:
            max_file_num += 1
            nums_file_dict[max_file_num] = file

        numbered_hash_dict[f_hash] = nums_file_dict

    main_dictionary[size] = numbered_hash_dict

print_duplicates_with_hash(main_dictionary)

if not yes_or_no('Delete files?'):  # user input
    exit()

n_files_to_delete = get_file_numbers(max_file_num)

total_size_deleted = 0
# delete files in N
for size, file_hash in main_dictionary.items():
    for hash, file_dict in file_hash.items():
        for num, file in file_dict.items():
            if num in n_files_to_delete:
                os.remove(file)
                # print(f'{file} deleted')
                total_size_deleted += size

print(f'\nTotal freed up space: {total_size_deleted} bytes')
