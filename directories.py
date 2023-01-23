#!/usr/bin/python3

# directories
'''Advent of code day 7'''

from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError
import re


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
        this.root_directory = Directory(None, '/')
        this.workind_directory = this.root_directory
        this.input_file = input_file
        this.current_command = this.read_next_line()
        this.ls_command_template = re.compile(r'\$ ls')
        this.cd_command_template = re.compile(r'\$ cd (.*)$')

    def has_command(this):
        return this.current_command != None and len(this.current_command) > 0

    def read_next_line(this):
        next_line = this.input_file.readline()
        if next_line:
            next_line = next_line.strip()
        if len(next_line) == 0:
            next_line = None
        return next_line

    def execute_command(this):
        if not this.has_command():
            print(f'Executing: No command')
            return

        command = re.match(this.cd_command_template, this.current_command)
        if command:
            print(f'Executing: cd {command.group(1)}')
            this.current_command = this.read_next_line()
            return

        command = re.match(this.ls_command_template, this.current_command)
        if command:
            print(f'Executing: ls')
            output_line = this.read_next_line()
            while (output_line and output_line[0] != '$'):
                print(f'   Output: {output_line}')
                output_line = this.read_next_line()
            this.current_command = output_line
            return

        print(f'Unrecognized command: {this.current_command}')
        this.current_command = this.read_next_line()
        return


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
            shell = Shell(input_file)
            while shell.has_command():
                shell.execute_command()

    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input(f'enter command line for {app_name}: ')
        argv.extend(command_line.split())
    main(argv[1:])