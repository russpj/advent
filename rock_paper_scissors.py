#!/usr/bin/python3

# rock_paper_scissors
'''Advent of code day 2'''

from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError


def main(arguments):
    program_name = 'rock_paper_scissors'
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
            print(f'The input file was {input_file_name}')

    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input('enter command line for rock_paper_scissors: ')
        argv.extend(command_line.split())
    main(argv[1:])