#!/usr/bin/python3

# arithmetic
'''Advent of code (2025) 06 cephalopod arithmetic'''


from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError
from time import process_time


app_name = 'arithmetic.py'


def read_problems(file):
    lines = []
    for line in file:
        lines.append(line.split())

    problems = []
    for problem_index in range(len(lines[0])):
        problem = []
        for line in lines:
            problem.append(line[problem_index])
        problems.append(problem)
    return problems


def main(arguments):
    program_name = app_name
    command_line_documentation = f'{program_name} --help --verbose --section [a|b] --file [input file]'
    verbose = False
    input_file_name = ''
    sections = []

    try:
        opts, args = getopt(arguments, "hvs:f:", ("help", "verbose", "section=", "file="))
    except GetoptError:
        print(f'Invalid Arguments: {command_line_documentation}')
        exit(2)

    for opt, arg in opts:	
        if opt in ('-h', '--help'):
            print(f'usage: {command_line_documentation}')
            exit(0)

        if opt in ('-v', '--verbose'):
            verbose = True

        if opt in ('-f', '--file'):
            input_file_name = arg

        if opt in ('-s', '--section'):
            for section in arg:
                sections.append(section)

    problems = []

    if input_file_name:
        with open(input_file_name, 'r') as input_file:
            if verbose:
                print(f'Opened {input_file_name} for {app_name}')
            problems = read_problems(input_file)

    time_start = process_time()
    for section in sections:
        print(f'Processing section {section}')
    if verbose:
        print('Debugging output goes here')
    time_end = process_time()
    print(f'Time taken: {time_end - time_start} seconds.')

    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input(f'enter command line for {app_name}: ')
        argv.extend(command_line.split())
    main(argv[1:])