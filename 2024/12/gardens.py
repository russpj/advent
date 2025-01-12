#!/usr/bin/python3

# gardens
'''Advent of code 2024 day 12 gardens'''


from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError
from time import process_time


app_name = 'gardens.py'

class Garden:
    def __init__(self, vegetable):
        self.vegetable = vegetable
        self.positions = set()
        self.area = 0
        self.perimeter = 0
        self.sides = 0
        return
    
    def add_grid(self, position):
        self.positions.append(position)
        return


class Gardens:
    def __init__(self):
        self.gardens = []
        self.grid = []
        return
    
    def read_file(self, input_file):
        row = 0
        for line in input_file:
            grid_row = []
            for col, vegetable in enumerate(list(line.strip())):
                grid_row.append(vegetable)
            self.grid.append(grid_row)
            row += 1
        self.num_rows = len(self.grid)
        self.num_cols = len(self.grid[0])
        return
    
    def new_positions(self, position):
        row = position[0]
        col = position[1]
        yield (row-1, col) if row > 0 else ()
        yield (row+1, col) if row < self.num_rows-1 else ()
        yield (row, col-1) if col > 0 else ()
        yield (row, col+1) if col < self.num_cols-1 else ()

    def find_rest_of_garden(self, garden, position):
        if position not in garden.positions:
            garden.positions.add(position)
            self.placed_positions.add(position)
            garden.area += 1
            for new_position in self.new_positions(position):
                if new_position:
                    if self.grid[new_position[0]][new_position[1]] == garden.vegetable:
                        self.find_rest_of_garden(garden, new_position)
                    else:
                        garden.perimeter += 1
                else:
                    garden.perimeter += 1
        return        
    
    def find_gardens(self):
        self.placed_positions = set()
        self.gardens = []
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if ((row, col)) not in self.placed_positions:
                    garden = Garden(self.grid[row][col])
                    self.find_rest_of_garden(garden, ((row, col)))
                    self.gardens.append(garden)
                    
    
    def print_grid(self):
        for grid_row in self.grid:
            for vegetable in grid_row:
                print(vegetable, end='')
            print()
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

    gardens = Gardens()

    if input_file_name:
        with open(input_file_name, 'r') as input_file:
            print(f'Opened {input_file_name} for {app_name}')
            gardens.read_file(input_file)

    time_start = process_time()
    if verbose:
        gardens.print_grid()
    gardens.find_gardens()
    for section in sections:
        print(f'Processing section {section}')
        if 'a' in section:
            cost = 0
            for garden in gardens.gardens:
                cost += garden.area*garden.perimeter
            print (f'The total cost (by perimeter) is {cost}.')
        if 'b' in section:
            cost = 0
            for garden in gardens.gardens:
                cost += garden.area*garden.sides
            print (f'The total cost (by sides) is {cost}.')
    time_end = process_time()
    print(f'Time taken: {time_end - time_start} seconds.')

    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input(f'enter command line for {app_name}: ')
        argv.extend(command_line.split())
    main(argv[1:])