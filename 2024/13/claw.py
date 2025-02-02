#!/usr/bin/python3

# claw
'''Advent of code Day 13 The Claw'''


from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError
from time import process_time
import re


app_name = 'claw.py'


class Claw:
    def __init__(self, button_a, button_b, goal):
        self.button_a = button_a
        self.button_b = button_b
        self.goal = goal
        return
    
    def print(self):
        print(f'Button A: X+{self.button_a[0]}, Y+{self.button_a[1]}')
        print(f'Button B: X+{self.button_b[0]}, Y+{self.button_b[1]}')
        print(f'Prize: X={self.goal[0]}, Y={self.goal[1]}')
        return
    

def parse_claws(file):
    claws = []
    button_test = r'Button ([A-B]): X\+(\d+), Y\+(\d+)'
    prize_test = r'Prize: X=(\d+), Y=(\d+)'
    for line in file:
        matches = re.findall(button_test, line)
        if matches:
            button = matches[0][0]
            x, y = [int(val) for val in matches[0][1:]]
            if button == 'A':
                button_a = (x, y)
            if button == 'B':
                button_b = (x, y)
        matches = re.findall(prize_test, line)
        if matches:
            goal = [int(val) for val in matches[0]]
            claws.append(Claw(button_a, button_b, goal))
    return claws


def find_solutions(claw):
    solutions = []
    return solutions


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
            claws = parse_claws(input_file)

    time_start = process_time()
    for section in sections:
        print(f'Processing section {section}')
        if section == 'a':
            for claw in claws:
                if verbose:
                    print('Finding solutions for:')
                    claw.print()
                solutions = find_solutions(claw)
                if verbose:
                    print(solutions)

    time_end = process_time()
    print(f'Time taken: {time_end - time_start} seconds.')

    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input(f'enter command line for {app_name}: ')
        argv.extend(command_line.split())
    main(argv[1:])