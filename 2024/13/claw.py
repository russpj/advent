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


def score(solution):
    return 3*solution[0] + solution[1]

def find_solutions(claw):
    solutions = []
    a = 0
    while True:
        b = (claw.goal[0] - a*claw.button_a[0])//claw.button_b[0]
        if b < 0:
            break
        if a*claw.button_a[0] + b*claw.button_b[0] == claw.goal[0]:
            if a*claw.button_a[1] + b*claw.button_b[1] == claw.goal[1]:
                solutions.append((score((a,b)), a, b))
        a += 1
    
    return sorted(solutions)


def adjust_claw_goals(claws, adjustment):
    new_claws = []
    for claw in claws:
        new_goal = (claw.goal[0]+adjustment, claw.goal[1]+adjustment)
        new_claws.append(Claw(claw.button_a, claw.button_b, new_goal))
    return new_claws


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
            original_claws = parse_claws(input_file)

    time_start = process_time()
    for section in sections:
        print(f'Processing section {section}')
        if section == 'a':
            claws = original_claws
        if section == 'b':
            claws = adjust_claw_goals(original_claws, 10000000000000)
        cost = 0
        prize_count = 0
        for claw in claws:
            if verbose:
                print('Finding solutions for:')
                claw.print()
            solutions = find_solutions(claw)
            if solutions:
                if verbose:
                    print(solutions)
                cost += solutions[0][0]
                prize_count += 1
            else:
                if verbose:
                    print('  No Solutions')
        print(f'The minimum cost to get {prize_count} prizes is {cost}.')

    time_end = process_time()
    print(f'Time taken: {time_end - time_start} seconds.')

    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input(f'enter command line for {app_name}: ')
        argv.extend(command_line.split())
    main(argv[1:])