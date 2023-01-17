#!/usr/bin/env python3
"""
Created on 21-10-2022
Author: Ruby van der Holst
Contact: rhcvdh@gmail.com

Last edited on 17-01-2023
by Ruby van der Holst

The purpose of this script is to convert a set of .seq files to a singular
.fasta file.
"""

import os
import sys
from datetime import datetime
import getopt


def get_arg():
    """
    The arguments are retrieved checked and returned. If the arguments are
    given in a wrong format or -h/--help is one of the arguments, the help is
    shown and the script terminates.

    :return arg_input_dir: Input directory (string)
    :return arg_prefix: Prefix of fasta file (string)
    :return arg_output_dir: Output directory (string)
    """
    argv = sys.argv
    arg_input_dir = '.'
    arg_prefix = 'new'
    arg_output_dir = '.'
    arg_help = '{0} -i <input directory> -p <prefix fasta file> -o <output directory>'.format(argv[0])

    try:
        opts, args = getopt.getopt(argv[1:], 'h:i:p:o:',
                                   ['help', 'input=', 'prefix=', 'output='])
    except getopt.GetoptError:
        print(arg_help)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(arg_help)
            sys.exit(2)
        elif opt in ('-i', '--input'):
            arg_input_dir = arg
        elif opt in ('-p', '--prefix'):
            arg_prefix = arg
        elif opt in ('-o', '--output'):
            arg_output_dir = arg
    return arg_input_dir, arg_prefix, arg_output_dir


def create_fasta(input_dir='.', output_prefix='new', output_dir='.'):
    """
    Iterates through files in input_dir. All files are checked if they have
    right requirements and if so are put into the fasta file.
    Requirements:
        - is a .seq file
        - is not empty
    A file (added.txt) is created which lists all used input files.
    A file (skipped.txt) is created which lists all unused files in the input
    directory.

    :param input_dir: Input directory (string)
    :param output_prefix: Prefix of output fasta file (string)
    :param output_dir: Output directory (string)
    """
    fasta_file = open(f'{output_dir}/{output_prefix}.fasta', 'w')
    added = []
    skipped = []

    for file_name in os.listdir(input_dir):
        file_path = os.path.join(input_dir, file_name)
        if file_name.endswith('.seq'):

            if os.stat(file_path).st_size == 0:
                print(f'"{file_name}" is empty. It will not be added to the '
                      f'new fasta file.')
                skipped.append(file_name)
            else:
                read_file = open(file_path, 'r', encoding="ISO-8859-1")
                sequence = read_file.readlines()[-1]
                read_file.close()

                mtime_float = os.path.getmtime(file_path)
                mtime_datetime = datetime.fromtimestamp(mtime_float).\
                    strftime("%d-%m-%y %H:%M:%S")
                base_file_name = os.path.basename(file_name)
                fasta_file.write(f'>{base_file_name}|{mtime_datetime}\n'
                                 f'{sequence}\n')
                added.append(file_name)
        else:
            skipped.append(file_name)

    fasta_file.close()

    list_to_file(added, f"{output_dir}/added.txt")
    list_to_file(skipped, f"{output_dir}/skipped.txt")

    print(f'"{output_prefix}.fasta" created successfully.')
    print('A list of the added files can be found in "added.txt".')
    print('A list of the skipped files can be found in "skipped.txt".')


def check_isdir(path, create=False):
    """
    This function checks if a directory exists. The user gets the option to
    create the directory if it does not exist.

    :param path: path of directory (string)
    :param create: boolean which indicates if a directory has to be created
    if it does not exist (boolean)
    :return: boolean which indicates if the user answered yes (True) or
    no (False).
    """
    if not os.path.isdir(path):
        print(f'Directory "{path}" does not exist.')
        if create:
            if "/" in path:
                if not check_isdir('/'.join(path.split('/')[:-1])):
                    return False
            if check_yes_no('Do you want to create this directory (yes/no): '):
                os.mkdir(path)
                print(f'Directory "{path}" is created.')
            else:
                sys.exit(1)
        return False
    else:
        return True


def windows_to_unix_path(windows_path):
    """
    A Windows type path is converted to a Unix type path.

    :param windows_path: a file/directory path using Windows format (string)
    :return unix_path: a file/directory path using Unix format (string)
    """
    unix_path = os.popen(f'wslpath "{windows_path}"').read().rstrip('\n')
    print(f"Windows path {windows_path} was converted to the unix path "
          f"{unix_path}")
    return unix_path


def check_yes_no(prompt):
    """
    A prompt is shown to user. The user can answer y, yes, n or no.
    The prompt will be shown again if the user does not give a valid answer.
    A boolean is returned which shows which answer the user has given.

    :param prompt: Text which is shown to the user on input (string)
    :return boolean: True (yes/y) or False (no/n)
    """
    while True:
        answer = input(prompt).lower()
        if answer in ['y', 'yes']:
            return True
        elif answer in ['n', 'no']:
            return False
        else:
            print('The answer must be one of the following: y, yes, n or no')


def list_to_file(item_list, file_path):
    """
    Iterates over a list of strings and puts each string in a new line in
    the given file.

    :param item_list: a list of strings to write into the file
    :param file_path: the path to the file
    """
    file = open(file_path, 'w')
    for item in item_list:
        file.write(item + '\n')
    file.close()


def main():
    input_dir, prefix, output_dir = get_arg()
    if '\\' in input_dir:
        input_dir = windows_to_unix_path(input_dir)
    if '\\' in output_dir:
        output_dir = windows_to_unix_path(output_dir)
    if not check_isdir(input_dir, create=False):
        sys.exit(1)
    check_isdir(output_dir, create=True)
    create_fasta(input_dir, prefix, output_dir)


if __name__ == '__main__':
    main()
