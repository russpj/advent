#!/usr/bin/python3

# advent
'''Advent of code (2025) 01 - Safe combination'''


from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError
from time import process_time


app_name = 'safelock.py'


class Dial:
    def __init__(self, pos, limit):
        self.pos = pos 
        self.limit = limit

    def move_dial(self, instruction):
        direction, amount = self.parse(instruction)
        if direction == 'L':
            amount = -amount
        self.pos += amount
        self.pos = self.pos%self.limit

    def parse(self, instruction):
        return ("R", 0)


def test(dial, expected):
    if dial.pos != expected:
        print (f'Expected: {expected}, Actual: {dial.pos}')

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

    if input_file_name:
        with open(input_file_name, 'r') as input_file:
            print(f'Opened {input_file_name} for {app_name}')

    time_start = process_time()
    dial = Dial(50, 100)

    for section in sections:
        print(f'Processing section {section}')
    if verbose:
        print('Debugging output goes here')
        print('Running some tests')
        test(dial, 50)
        dial.move_dial("R10")
        test(dial, 60)
        dial.move_dial("L20")
        test(dial, 40)
        dial.move_dial("L50")
        test(dial, 90)
        dial.move_dial("R10")
        test(dial, 0)

    time_end = process_time()
    print(f'Time taken: {time_end - time_start} seconds.')

    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input(f'enter command line for {app_name}: ')
        argv.extend(command_line.split())
    main(argv[1:])