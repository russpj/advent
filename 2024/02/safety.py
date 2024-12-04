#!/usr/bin/python3

# safety
'''Advent of code Puzzle 02'''


from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError


app_name = 'safety.py'

def adjacent_difference(sequence):
    first = sequence[0::]
    second = sequence[1::]
    pairs = zip(first, second)
    diffs = []
    for pair in pairs:
        diffs.append(pair[1] - pair[0])
    return diffs


def is_within(values, min_value, max_value): # [min_value, max_value)
    for value in values:
        if value < min_value:
            return False
        if value >= max_value:
            return False
    return True


def main(arguments):
    program_name = app_name
    command_line_documentation = f'{program_name} --help --section [a|b] --file [input file]'
    input_file_name = ''
    sections = []

    try:
        opts, args = getopt(arguments, "hs:f:", ("help", "section=", "file="))
    except GetoptError:
        print(f'Invalid Arguments: {command_line_documentation}')
        exit(2)

    for opt, arg in opts:	
        if opt in ('-h', '--help'):
            print(f'usage: {command_line_documentation}')
            exit(0)

        if opt in ('-f', '--file'):
            input_file_name = arg

        if opt in ('-s', '--section'):
            sections.append(arg)

    reports = []
    if input_file_name:
        with open(input_file_name, 'r') as input_file:
            print(f'Opened {input_file_name} for {app_name}')
            for line in input_file:
                report = [int(x) for x in line.split()]
                reports.append(report)

    for section in sections:
        print(f'Processing {len(reports)} reports in section {section}')
        if section == 'a':
            count_safe = 0
            for report in reports:
                level_diffs = adjacent_difference(report)
                safe = is_within(level_diffs, 1, 4) or is_within(level_diffs, -3, 0)
                if safe:
                    count_safe += 1
            print(f'There were {count_safe} safe reports')

    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input(f'enter command line for {app_name}: ')
        argv.extend(command_line.split())
    main(argv[1:])