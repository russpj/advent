#!/usr/bin/python3

# guard
'''Advent of code day 06 - guard paths'''


from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError


app_name = 'guard.py'

class Lab:
    def __init__(self, place_obstacles):
        self.map = []
        self.step = {'v': (1, 0), '<': (0, -1), '^': (-1, 0), '>': (0, 1)}
        self.turn = {'v': '<', '<': '^', '^': '>', '>': 'v'}
        self.block = '#'
        self.visited = 'X'
        self.num_rows = 0
        self.num_cols = 0
        self.obstacles_placed = []
        self.place_obstacles = place_obstacles
        return
    
    def set_map(self, map):
        self.map = []
        self.num_rows = len(map)
        if self.num_rows:
            self.num_cols = len(map[0])
            for row in range(self.num_rows):
                map_row = []
                for col in range(self.num_cols):
                    map_row.append(map[row][col])
                self.map.append(map_row)

    def print_map(self):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                print(self.map[row][col], end='')
            print()
        print()

    def print_map_near_position(self, position):
        size = 3
        for row in range(position[0]-size, position[0]+size+1):
            if row >= 0 and row < self.num_rows:
                for col in range(position[1]-size, position[1]+size+1):
                    if col >= 0 and col < self.num_cols:
                        print(self.map[row][col], end='')
                print()
        print()
    
    def guard_positions(self):
        positions = []
        for row in range(len(self.map[0])):
            if row >= 0:
                for col in range(len(self.map[row])):
                    cell = self.map[row][col]
                    if cell in self.turn:
                        position = (row, col)
                        positions.append(position)
        return positions
    
    def count_visited_positions(self):
        count = 0
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if self.map[row][col] == self.visited:
                    count += 1
        return count
    
    def move_guard(self, position):
        row = position[0]
        col = position[1]
        guard = self.map[row][col]
        if guard in self.turn:
            self.map[row][col] = self.visited
            next_step = self.step[guard]
            next_row = row + next_step[0]
            next_col = col + next_step[1]
            if next_row < 0 or next_row >= self.num_cols:
                return
            if next_col < 0 or next_col >= self.num_cols:
                return
            if self.map[next_row][next_col] == self.block:
                self.map[row][col] = self.turn[guard]
            else:
                self.map[next_row][next_col] = guard


def main(arguments):
    program_name = app_name
    command_line_documentation = f'{program_name} --help --verbose --section [a|b] --file [input file]'
    input_file_name = ''
    sections = []
    verbose = False

    try:
        opts, args = getopt(arguments, "hvs:f:", ("help", "verbose", "section=", "file="))
    except GetoptError:
        print(f'Invalid Arguments: {command_line_documentation}')
        exit(2)

    for opt, arg in opts:	
        if opt in ('-h', '--help'):
            print(f'usage: {command_line_documentation}')
            exit(0)

        if opt in ('-f', '--file'):
            input_file_name = arg

        if opt in ('-s', '--section'):
            for section in arg:
                sections.append(section)

        if opt in ('-v', '--verbose'):
            verbose = True

    place_obstacles = 'b' in section
    lab = Lab(place_obstacles)

    if input_file_name:
        with open(input_file_name, 'r') as input_file:
            map = []
            print(f'Opened {input_file_name} for {app_name}')
            for line in input_file:
                map.append(line.strip())
        lab.set_map(map)
        if verbose:
            lab.print_map()

    go_again = True
    while go_again:
        guard_positions = lab.guard_positions()
        if len(guard_positions) <= 0:
            go_again = False
        else:
            for position in guard_positions:
                if verbose:
                    lab.print_map_near_position(position)
                lab.move_guard(position)
    if verbose:
        lab.print_map()
    if 'a' in sections:
        print(f'The guards visited {lab.count_visited_positions()} positions')

    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input(f'enter command line for {app_name}: ')
        argv.extend(command_line.split())
    main(argv[1:])