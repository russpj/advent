#!/usr/bin/python3

# trails
'''Advent of code 2024 Day 10 - Trails'''


from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError
from time import process_time


app_name = 'trails.py'


class Trails:
    def __init__(self):
        return
    
    def read_file(self, input_file):
        self.grid = []
        for line in input_file:
            row = [int(digit) for digit in list(line.strip())]
            self.grid.append(row)
        self.num_rows = len(self.grid)
        self.num_cols = len(self.grid[0])
        return
    
    def trail_ends(self, location):
        row = location[0]
        col = location[1]
        height = self.grid[row][col]
        if height == 9:
            yield location
        else:
            if row-1 >= 0 and self.grid[row-1][col] == height+1:
                yield from self.trail_ends((row-1, col))
            if row+1 < self.num_rows and self.grid[row+1][col] == height+1:
                yield from self.trail_ends((row+1, col))
            if col-1 >= 0 and self.grid[row][col-1] == height+1:
                yield from self.trail_ends((row, col-1))
            if col+1 < self.num_cols and self.grid[row][col+1] == height+1:
                yield from self.trail_ends((row, col+1))
        return
    
    def find_trails(self):
        self.trails = {}
        for row_index in range(len(self.grid)):
            for col_index in range(len(self.grid[row_index])):
                if self.grid[row_index][col_index] == 0:
                    trail_head = (row_index, col_index)
                    trail_ends = []
                    for trail_end in self.trail_ends(trail_head):
                        if trail_end not in trail_ends:
                            trail_ends.append(trail_end)
                    self.trails[trail_head] = trail_ends
        return


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

    trails = Trails()

    if input_file_name:
        with open(input_file_name, 'r') as input_file:
            print(f'Opened {input_file_name} for {app_name}')
            trails.read_file(input_file)

    time_start = process_time()
    for section in sections:
        print(f'Processing section {section}')
        if 'a' in section:
            trails.find_trails()
            num_trails = 0
            for trail_head in trails.trails:
                num_trails += len(trails.trails[trail_head])
                if verbose:
                    print(f'{trail_head}: {trails.trails[trail_head]}')
            print(f'There were {num_trails} different routes')
    time_end = process_time()
    print(f'Time taken: {time_end - time_start} seconds.')

    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input(f'enter command line for {app_name}: ')
        argv.extend(command_line.split())
    main(argv[1:])