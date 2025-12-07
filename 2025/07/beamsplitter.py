#!/usr/bin/python3

#  beamsplitter
'''Advent of code (2025) 07 tackyon beam splitter'''


from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError
from time import process_time


app_name = 'beamsplitter.py'


class Manifold:
    def __init__(self, input_file):
        manifold = []
        for row in input_file:
            manifold.append(row.strip('\n'))
        self.manifold = manifold
        self.beams = self.place_beams_at_start('S')
        self.num_splits = 0
        return

    def place_beams_at_start(self, start_character):
        beams = set()
        first_row = self.manifold[0]
        start_location = first_row.find(start_character)
        while start_location != -1:
            beams.add((0,start_location))
            start_location = first_row[start_location+1:].find(start_character)
        return beams

    def move_beams_once():
        pass
    

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

    if input_file_name:
        with open(input_file_name, 'r') as input_file:
            if verbose:
                print(f'Opened {input_file_name} for {app_name}')

            time_start = process_time()
            for part in parts:
                print(f'Processing part {part}')
                if part == '1':
                    manifold = Manifold(input_file)

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