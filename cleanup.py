#!/usr/bin/python3

# cleanup
'''Advent of code day 3'''

from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError

app_name = 'cleanup'


def parse_assignments(line):
    assignments = []
    ranges = line.split(',')
    for range in ranges:
        left, right = range.split('-')
        assignments.append((int(left), int(right)))
    return assignments


def left_contains_right(left, right):
    contains = left[0] <= right[0] and left[1] >= right[1]
    return contains


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
            contains_count = 0
            for line in input_file:
                assignments = parse_assignments(line.strip())
                first = assignments[0]
                second = assignments[1]
                if left_contains_right(first, second) or left_contains_right(second, first):
                    contains_count += 1
            print(f'{contains_count} of the assigments had completely overlapping ranges.')
    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input(f'enter command line for {app_name}: ')
        argv.extend(command_line.split())
    main(argv[1:])