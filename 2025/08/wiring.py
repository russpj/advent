#!/usr/bin/python3

# wiring
'''Advent of code (2025) 07 Junction Box Wiring'''


from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError
from time import process_time


app_name = 'wiring.py'


def distance_squared(boxes, first, second):
    first_box = boxes[first]
    second_box = boxes[second]
    ds = 0
    for coordinate in range(len(first_box)):
        ds += (first_box[coordinate]-second_box[coordinate])**2
    return ds


def main(arguments):
    program_name = app_name
    command_line_documentation = f'{program_name} --help --verbose --part [1|2] --file [input file]'
    verbose = False
    input_file_name = ''
    parts = []

    try:
        opts, args = getopt(arguments, "hvp:f:", ("help", "verbose", "part=", "file="))
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

        if opt in ('-p', '--part'):
            for part in arg:
                parts.append(part)

    num_trials = 0
    boxes = []
    if input_file_name:
        with open(input_file_name, 'r') as input_file:
            if verbose:
                print(f'Opened {input_file_name} for {app_name}')
            for line in input_file:
                if num_trials == 0:
                    num_trials = int(line)
                else:
                    x, y, z = line.split(',')
                    boxes.append((int(x), int(y), int(z)))

    time_start = process_time()
    for part in parts:
        print(f'Processing part {part}')
        if part == '1':
            pairs = [(x, y, distance_squared(boxes, x, y)) for x in range(len(boxes)) for y in range(x)]
            pairs.sort(key=lambda pair: pair[2])
            if verbose:
                for pair in pairs:
                    first = boxes[pair[0]]
                    second = boxes[pair[1]]
                    print(f'({first}, {second})')
    time_end = process_time()
    print(f'Time taken: {time_end - time_start} seconds.')

    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input(f'enter command line for {app_name}: ')
        argv.extend(command_line.split())
    main(argv[1:])