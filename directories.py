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
        this.update_accumulated_size(size)
        return

    def update_accumulated_size(this, size):
        this.accumulated_size += size
        if this.parent:
            this.parent.update_accumulated_size(size)

    def dictionary_list(this):
        yield this
        for child in this.child_directories:
            yield from child.dictionary_list()



class Shell():
    def __init__(this, input_file):
        this.root_directory = Directory(None, '/')
        this.working_directory = this.root_directory
        this.input_file = input_file
        this.current_command = this.read_next_line()
        this.ls_command_template = re.compile(r'\$\s+ls')
        this.cd_command_template = re.compile(r'\$\s+cd\s+(.*)$')
        this.directory_listing = re.compile(r'dir\s+(\S+)')
        this.file_listing = re.compile(r'(\d+)\s+(\S+)')

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
            target_directory = command.group(1)
            print(f'Executing: cd {target_directory}')
            if target_directory == '/':
                this.working_directory = this.root_directory
            elif target_directory == '..':
                if this.working_directory.parent:
                    this.working_directory = this.working_directory.parent
            else:
                directory_found = False
                for directory in this.working_directory.child_directories:
                    if directory.name == target_directory:
                        this.working_directory = directory
                        directory_found = True
                if not directory_found:
                    print(f'Error: Could not find {target_directory} in {this.working_directory}')
            this.current_command = this.read_next_line()
            return

        command = re.match(this.ls_command_template, this.current_command)
        if command:
            print(f'Executing: ls')
            output_line = this.read_next_line()
            while (output_line and output_line[0] != '$'):
                output = re.match(this.file_listing, output_line)
                if output:
                    file_name = output.group(2)
                    file_size = int(output.group(1))
                    print(f'     File: {file_name} {file_size}')
                    this.working_directory.add_file(file_name, file_size)
                    output_line = this.read_next_line()
                    continue
                
                output = re.match(this.directory_listing, output_line)
                if output:
                    directory_name = output.group(1)
                    print(f'Directory: dir {directory_name}')
                    this.working_directory.add_directory(directory_name)
                    output_line = this.read_next_line()
                    continue

                print(f'Unrecognized output: {output_line}')
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
            file_system_capacity = 70000000
            update_required_free_space = 30000000
            space_available = file_system_capacity - shell.root_directory.accumulated_size
            new_space_required = update_required_free_space - space_available
            candidate_directory = None
            for directory in shell.root_directory.dictionary_list():
                print(f'finding directory {directory.name} with {directory.accumulated_size} in size')
                if directory.accumulated_size > new_space_required:
                    if not candidate_directory or directory.accumulated_size < candidate_directory.accumulated_size:
                        candidate_directory = directory
            print(f'{candidate_directory.accumulated_size} will be freed by deleting {candidate_directory.name}')
            print(f'There will be {space_available+candidate_directory.accumulated_size} bytes free on the filesystem.')

    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input(f'enter command line for {app_name}: ')
        argv.extend(command_line.split())
    main(argv[1:])