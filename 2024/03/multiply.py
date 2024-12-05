#!/usr/bin/python3

# multiply
'''Advent of code 2024 03'''


from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError
import re

app_name = 'multiply.py'

def evaluate(function):
    if function[0:3] == 'mul':
        arguments = function[4:-1]
        left, right = arguments.split(',')
        return int(left)*int(right)


class Processor:
    def __init__(this):
        this.enabled = True
        this.accumulator = 0

    def execute(this, function):
        if function[0:3] == 'mul':
            arguments = function[4:-1]
            left, right = arguments.split(',')
            if this.enabled:
                this.accumulator += int(left)*int(right)
        if function[0:2] == 'do':
            this.enabled = True
        if function[0:5] == "don't":
            this.enabled = False


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
            for section in arg:
                sections.append(section)

    if input_file_name:
        with open(input_file_name, 'r') as input_file:
            print(f'Opened {input_file_name} for {app_name}')
            commands = []
            for line in input_file:
                commands.append(line)

    for section in sections:
        print(f'Processing section {section}')
        if section == 'a':
            sum = 0
            test = r'mul\(\d{1,3},\d{1,3}\)'
            for command in commands:
                matches = re.findall(test, command)
                for function in matches:
                    sum += evaluate(function)
            print(f'The sum of all of the multiplications in {len(commands)} commands is {sum}')

        if section == 'b':
            proc = Processor()
            mul_test = r'mul\(\d{1,3},\d{1,3}\)'
            do_test = r'do\(\)'
            dont_test = r"don\'t\(\)"
            test = f'{mul_test}|{do_test}|{dont_test}'
            for command in commands:
                matches = re.findall(test, command)
                for function in matches:
                    proc.execute(function)
            print(f'Enabled multiplies added up to {proc.accumulator}')
    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input(f'enter command line for {app_name}: ')
        argv.extend(command_line.split())
    main(argv[1:])