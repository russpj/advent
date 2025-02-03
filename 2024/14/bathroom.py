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
        self.pos = list(pos)
        self.vel = list(vel)
        return
    

class Floor:
    def __init__(self, num_cols, num_rows, robots):
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.robots = robots
        return
    
    def print(self):
        robot_counts = {}
        for robot in self.robots:
            location = tuple(robot.pos)
            if location in robot_counts:
                robot_counts[location] += 1
            else:
                robot_counts[location] = 1
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if (col, row) in robot_counts:
                    print(robot_counts[(col, row)], end='')
                else:
                    print('.', end='')
            print()
        return
    
    def move_robots(self, moves):
        for robot in self.robots:
            pos = list(robot.pos)
            vel = robot.vel
            size = (self.num_cols, self.num_rows)
            for index in range(2):
                pos[index] += vel[index]*moves
                pos[index] = pos[index] % size[index]
            robot.pos = pos
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

    grid_size = {'test.txt': (11, 7), 'input.txt': (101, 103)}

    floor_size = grid_size[input_file_name]

    time_start = process_time()
    for section in sections:
        print(f'Processing section {section}')
        if section == 'a':
            floor = Floor(floor_size[0], floor_size[1], robots.copy())
            if verbose:
                floor.print()
            floor.move_robots(100)
            if verbose:
                print(f'After {100} moves:')
                floor.print()
    time_end = process_time()
    print(f'Time taken: {time_end - time_start} seconds.')

    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input(f'enter command line for {app_name}: ')
        argv.extend(command_line.split())
    main(argv[1:])