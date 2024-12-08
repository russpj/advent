#!/usr/bin/python3

# guard
'''Advent of code day 06 - guard paths'''


from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError


app_name = 'guard.py'

class Lab:
    def __init__(self):
        self.map = []
        self.step = {'v': (1, 0), '<': (0, -1), '^': (-1, 0), '>': (0, 1)}
        self.turn = {'v': '<', '<': '^', '^': '>', '>': 'v'}
        self.block = '#'
        self.visited = 'X'
        return
    
    def guard_positions(self):
        positions = []
        for row in range(len(self.map[0])):
            if row > 0:
                for col in range(len(self.map[row])):
                    cell = self.map[row][col]
                    if cell in self.turn:
                        position = (row, col)
                        positions.append(position)
        return positions


def main(arguments):
    program_name = app_name
    command_line_documentation = f'{program_name} --help --verbose --section [a|b] --file [input file]'
    input_file_name = ''
    sections = []
    verbose = False

    try:
        opts, args = getopt(arguments, "hvs:f:", ("help", "verbose", "section=", "file="))
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

        if opt in ('-v', '--verbose'):
            verbose = True

    lab = Lab()

    if input_file_name:
        with open(input_file_name, 'r') as input_file:
            print(f'Opened {input_file_name} for {app_name}')
            for line in input_file:
                lab.map.append(line.strip())
        if verbose:
            for row in lab.map:
                print(row)


    for section in sections:
        print(f'Processing section {section}')
        if section == 'a':
            guard_positions = lab.guard_positions()
            for position in guard_positions:
                print(f"There's a guard at {position}")

    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input(f'enter command line for {app_name}: ')
        argv.extend(command_line.split())
    main(argv[1:])