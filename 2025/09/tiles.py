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


class Edges:
    def __init__(self, path):
        self.path = path
        self.scan_lines = self.find_edges()
        return
    
    def find_edges(self):
        horizontal_edges = []
        vertical_edges = []

        for path_index in range(len(self.path)):
            next_index = (path_index + 1)%len(self.path)
            first_end = self.path[path_index]
            second_end = self.path[next_index]
            if first_end[1] == second_end[1]:
                # this is a horizontal edge
                horizontal_edges.append((first_end[1],                             
                              (min(first_end[0], second_end[0]),                             
                               max(first_end[0], second_end[0]))))
            elif first_end[0] == second_end[0]:
                # this is a vertical edge
                vertical_edges.append((first_end[0],                             
                              (min(first_end[1], second_end[1]),                             
                               max(first_end[1], second_end[1]))))
                
        horizontal_edges.sort()
        vertical_edges.sort()
        self.horizontal_edges = horizontal_edges
        self.vertical_edges = vertical_edges
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
            if verbose:
                print(f'Found {len(rectangles)} rectangles')
            edges = Edges(red_tiles)
            if verbose:
                print(f'Found {len(edges.horizontal_edges)} horizontal edges ', end='')
                print(f'and {len(edges.vertical_edges)} vertical edges')
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