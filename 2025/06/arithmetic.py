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


def parse_column(lines, col):
    '''The column could be blank, could have a number, or could have a number and an operator'''
    number = 0
    operator = ''
    for ch in [lines[line][col] for line in range(len(lines))]:
        if ch.isdigit():
            number *= 10
            number += int(ch)
        elif ch == '+' or ch == '*':
            operator = ch
    return (number, operator)


def read_cephalopod_problem(lines, col):
    problem = []
    operator = ''
    while col >= 0:
        number, operator = parse_column(lines, col)
        col -= 1
        if number > 0:
            problem.append(str(number))
            if operator:
                problem.append(operator)
                return (problem, col)
    return ()



def read_cephalopod_problems(file):
    lines = []
    for line in file:
        lines.append(line.strip('\n'))

    problems = []
    col = len(lines[0])-1
    while (col >= 0):
        problem, col = read_cephalopod_problem(lines, col)
        if problem:
            problems.append(problem)

    return problems


def solve_problem(problem):
    arguments = problem[:-1]
    operator = problem[-1]
    if operator == '+':
        total = 0
        for argument in arguments:
            total += int(argument)
        return total
    if operator == '*':
        product = 1
        for argument in arguments:
            product *= int(argument)
        return product
    return 0


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

    time_start = process_time()
    for section in sections:
        print(f'Processing section {section}')
        if section == 'a':
            problems = []
            if input_file_name:
                with open(input_file_name, 'r') as input_file:
                    if verbose:
                        print(f'Opened {input_file_name} for {app_name}')
                    problems = read_problems(input_file)
            grand_total = 0
            for problem in problems:
                grand_total += solve_problem(problem)
            print(f'the grand total is {grand_total}')

        if section == 'b':
            problems = []
            if input_file_name:
                with open(input_file_name, 'r') as input_file:
                    if verbose:
                        print(f'Opened {input_file_name} for {app_name}')
                    problems = read_cephalopod_problems(input_file)
            grand_total = 0
            for problem in problems:
                grand_total += solve_problem(problem)
            print(f'the grand total is {grand_total}')

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