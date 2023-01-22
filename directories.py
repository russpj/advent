#!/usr/bin/python3

# directories
'''Advent of code day 7'''

from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError

app_name = 'directories.py'

class File():
    def __init__(this, name, size):
        this.name = name
        this.size = size
        return

class Directory():
    def __init__(this, parent, name):
        this.parent = parent
        this.name = name
        this.child_directories = []
        this.files = []
        this.accumulated_size = 0

    def add_directory(this, name):
        child = Directory(this, name)
        this.child_directories.append(child)

    def add_file(this, name, size):
        file = File(name, size)
        this.files.append(file)
        this.update_accumulate_size(size)
        return

    def update_accumulated_size(this, size):
        this.accumulate_size += size
        if this.parent:
            this.parent.update_accumulated_size(size)


class Shell():
    def __init__(this, input_file):
        this.root_directory = Directory('\'')
        this.workind_directory = this.root_directory
        this.input_file = input_file
        this.current_command = input_file.readline()



    


def main(arguments):
    program_name = app_name
    command_line_documentation = f'{program_name} --help --file [input file]'
    input_file_name = ''

    try:
        opts, args = getopt(arguments, "hf:", 
            ("help", "file="))
    except GetoptError:
        print(f'Invalid Arguments: {command_line_documentation}')
        exit(2)

    for opt, arg in opts:	
        if opt in ('-h', '--help'):
            print(f'usage: {command_line_documentation}')
            exit(0)

        if opt in ('-f', '--file'):
            input_file_name = arg

    if input_file_name:
        with open(input_file_name, 'r') as input_file:
            print(f'Opened {input_file_name} for {app_name}')

    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input(f'enter command line for {app_name}: ')
        argv.extend(command_line.split())
    main(argv[1:])