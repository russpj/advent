#!/usr/bin/python3

# calories
'''Advent of code day 1 part 1'''

from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError


def main(arguments):
    program_name = 'calories'
    command_line_documentation = f'{program_name} --help --file [input file]'
    input_file = ''

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
            input_file=arg

    if input_file:
        'process input'

    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input('enter command line for calories: ')
        argv.extend(command_line.split())
    main(argv[1:])