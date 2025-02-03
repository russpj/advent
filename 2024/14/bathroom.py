#!/usr/bin/python3

# advent
'''Advent of code Day 14 - Bathroom guards'''


from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError
from time import process_time
from re import findall


app_name = 'bathroom.py'


class Robot:
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel
        return


def parse_robots(file):
    robots = []
    robot_exp = r'p=(-?\d*),(-?\d*) v=(-?\d*),(-?\d*)'    
    for line in file:
        matches = findall(robot_exp, line)
        if matches:
            pos = [int(val) for val in matches[0][0:2]]
            vel = [int(val) for val in matches[0][2:4]]
            robots.append(Robot(pos, vel))
    return robots


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
            robots = parse_robots(input_file)

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