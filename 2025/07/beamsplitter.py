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
        self.place_beams('S')
        self.num_splits = 0
        return

    def place_beams(self, start_character):
        beams = set()
        time_line_tracker = {}
        first_row = self.manifold[0]
        start_location = first_row.find(start_character)
        while start_location != -1:
            beams.add((0,start_location))
            time_line_tracker[(0, start_location)] = 1
            start_location = first_row[start_location+1:].find(start_character)
        self.beams = beams
        self.time_line_tracker = time_line_tracker
        return
    
    def propogate_beam(self, row, col):
        new_beams = []
        if row+1 < len(self.manifold):
            if self.manifold[row+1][col] == '^':
                if col-1 >= 0:
                    new_beams.append((row+1, col-1))
                if col+1 < len(self.manifold[row+1]):
                    new_beams.append((row+1, col+1))
            else:
                new_beams.append((row+1, col))
        return new_beams
    
    def add_count_of_time_lines(self, count, location):
        if location in self.time_line_tracker:
            old_count = self.time_line_tracker[location]
            self.time_line_tracker[location] = old_count + count
        else:
            self.time_line_tracker[location] = count
        return

    def count_time_lines(self):
        count = 0
        row = len(self.manifold) - 1
        for col in range(len(self.manifold[row])):
            location = (row, col)
            if location in self.time_line_tracker:
                count += self.time_line_tracker[location]
        return count

    def move_beams_once(self):
        new_beams = set()
        for beam in self.beams:
            row = beam[0]
            col = beam[1]
            count_of_time_lines = self.time_line_tracker[beam]
            next_beams = self.propogate_beam(row, col)
            if len(next_beams) > 1:
                self.num_splits += 1
            for next_beam in next_beams:
                new_beams.add((next_beam[0], next_beam[1]))
                self.add_count_of_time_lines(count_of_time_lines, next_beam)
        self.beams = new_beams

        return
    

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
            time_start = process_time()
            if verbose:
                print(f'Opened {input_file_name} for {app_name}')
            manifold = Manifold(input_file)
            while manifold.beams:
                manifold.move_beams_once()

            for part in parts:
                print(f'Processing part {part}')
                if part == '1':
                    print(f'the beam was split {manifold.num_splits} times')
                if part == '2':
                    print(f'the beam traveled through {manifold.count_time_lines()} time lines')

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