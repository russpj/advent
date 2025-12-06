#!/usr/bin/python3

# forklift
'''Advent of code (2025) 04 moving paper rolls by forklift'''


from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError
from time import process_time


app_name = 'forklift.py'


def count_rolls(floor, row_roll, col_roll):
    num_rolls = 0
    for row in range(row_roll-1, row_roll+2):
        for col in range(col_roll-1, col_roll+2):
            if row >= 0 and row < len(floor) and col >= 0 and col < len(floor[row_roll]):
                if not(row == row_roll and col == col_roll):
                    if floor[row][col] == '@':
                        num_rolls += 1
    return num_rolls


def find_movable_rolls(floor, threshold):
    moveable_rolls = set()
    for row in range(len(floor)):
        for col in range(len(floor[row])):
            if floor[row][col] == '@' and count_rolls(floor, row, col) < threshold:
                moveable_rolls.add((row, col))
    return moveable_rolls


def remove_rolls(floor, rolls):
    for roll in rolls:
        row, col = roll
        floor[row] = floor[row][:col] + 'x' + floor[row][col+1:]


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

    floor = []
    if input_file_name:
        with open(input_file_name, 'r') as input_file:
            print(f'Opened {input_file_name} for {app_name}')
            for row in input_file:
                floor.append(row.strip())

    time_start = process_time()
    for section in sections:
        print(f'Processing section {section}')
        if section == 'a':
            moveable_rolls = find_movable_rolls(floor, 4)
            print(f'{len(moveable_rolls)} rolls are moveable')

        if section == 'b':
            count_of_rolls = 0
            moveable_rolls = find_movable_rolls(floor, 4)
            while moveable_rolls:
                count_of_rolls += len(moveable_rolls)
                remove_rolls(floor, moveable_rolls)
                moveable_rolls = find_movable_rolls(floor, 4)
            print(f'{count_of_rolls} rolls are moveable over many turns')

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