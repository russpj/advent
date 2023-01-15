#!/usr/bin/python3

# rucksack
'''Advent of code day 3'''

from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError

app_name = 'rucksack'


def priority(item_type):
    if item_type >= 'a' and item_type <= 'z':
        return ord(item_type) - ord('a') + 1
    if item_type >= 'A'  and item_type <= 'Z':
        return ord(item_type) - ord('A') + 27
    return 100


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
            sum_priorities = 0
            for contents in input_file:
                contents = contents.strip()
                midpoint = len(contents)//2
                left = set(contents[:midpoint])
                right = set(contents[midpoint:])
                common_items = left.intersection(right)
                for item in common_items:
                    sum_priorities += priority(item)
            print(f'the total priorities is {sum_priorities}')

    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input(f'enter command line for {app_name}: ')
        argv.extend(command_line.split())
    main(argv[1:])