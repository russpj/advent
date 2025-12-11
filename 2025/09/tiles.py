#!/usr/bin/python3

# tiles
'''Advent of code (2025) 09 floor tiles'''


from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError
from time import process_time


app_name = 'tiles.py'


def parse_pair(line):
    pair = line.strip().split(',')
    return (int(pair[0]), int(pair[1]))


def area(tiles, first_tile, second_tile):
    first = tiles[first_tile]
    second = tiles[second_tile]
    area = (abs(first[0]-second[0])+1)*(abs(first[1]-second[1])+1)
    return area


def rectangle(tiles, first_tile, second_tile):
    first = tiles[first_tile]
    second = tiles[second_tile]
    ul = (min(first[0], second[0]), min(first[1], second[1]))
    lr = (max(first[0], second[0]), max(first[1], second[1]))
    area = (lr[0]-ul[0]+1)*(lr[1]-ul[1]+1)
    return ((ul, lr), area)


class Scan_lines:
    def __init__(self, path):
        self.path = path
        self.scan_lines = self.find_scan_lines()
        return
    
    def find_scan_lines(self):
        edges = []

        for path_index in range(len(self.path)):
            next_index = (path_index + 1)%len(self.path)
            first_corner = self.path[path_index]
            second_corner = self.path[next_index]
            if first_corner[1] == second_corner[1]:
                # this is a horizontal edge
                edges.append((first_corner[1],                             
                              (min(first_corner[0], second_corner[0]),                             
                               max(first_corner[0], second_corner[0]))))
        edges.sort()
        first_row = edges[0][0]
        last_row = edges[-1][0]

        scan_lines = {}
        current_row = first_row-1
        scan_lines[current_row] = []
        edge_index = 0

        while edge_index < len(edges):
            edge = edges[edge_index]
            edge_row = edge[0]
            for row in range(current_row, edge_row):            
                scan_lines[row] = scan_lines[current_row].copy()
            scan_line = scan_lines[current_row].copy()
            for col in range(edge[1][0], edge[1][1]+1):
                if col not in scan_line:
                    scan_line.append(col)
                else:
                    if self.should_remove_column(edge[1], scan_lines[current_row], col):
                        scan_line.remove(col)
            scan_line.sort()
            scan_lines[edge_row] = scan_line
            current_row = edge_row
            edge_index += 1
        return
    
    def should_remove_column(self, edge_columns, previous_scan_line, col):
        if col == edge_columns[0] and col-1 in previous_scan_line:
            return False
        if col == edge_columns[-1] and col+1 in previous_scan_line:
            return False
        return True
    
    
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
            red_tiles = [parse_pair(location) for location in input_file]

    time_start = process_time()
    for part in parts:
        print(f'Processing part {part}')
        if part == '1':
            areas = [area(red_tiles, first, second)
                       for first in range(len(red_tiles)) 
                       for second in range(first)]
            areas.sort(reverse=True)
            print(f'The largest area is {areas[0]}')

        if part == '2':
            rectangles = [rectangle(red_tiles, first, second)
                       for first in range(len(red_tiles)) 
                       for second in range(first)]
            rectangles.sort(key=lambda rectangle: -rectangle[1])
            scan_lines = Scan_lines(red_tiles)

            pass

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