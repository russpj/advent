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


def create_rectangle(tiles, first_tile, second_tile):
    first = tiles[first_tile]
    second = tiles[second_tile]
    ul = (min(first[0], second[0]), min(first[1], second[1]))
    lr = (max(first[0], second[0]), max(first[1], second[1]))
    area = (lr[0]-ul[0]+1)*(lr[1]-ul[1]+1)
    return ((ul, lr), area)


def find_edge(edges, target):
    first = 0
    last = len(edges)
    while first < last:
        mid = first + (last-first)//2
        value = edges[mid][0]
        if value == target:
            return mid
        elif value < target:
            first = mid+1
        else:
            last = mid
    return first


def does_edge_intersect_range(edge, first, last):
    if edge[1][1] <= first or edge[1][0] >= last:
        return False
    else:
        return True
    

def does_any_edge_intersect_range(edges, edge_candidates, range):
    edge_index = find_edge(edges, edge_candidates[0])
    if edge_index < len(edges):
        edge = edges[edge_index]
        while edge[0] <= edge_candidates[1]:
            if does_edge_intersect_range(edge, range[0], range[1]):
                return True
            edge_index += 1
            if edge_index < len(edges):
                edge = edges[edge_index]
            else:
                break
    return False


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
    
    def find_vertical_edge(self, column):
        '''Find first vertical edge at or to the right of the given column'''
        index = find_edge(self.vertical_edges, column)
        return index
    
    def find_horizontal_edge(self, row):
        '''Find first horizontal edge at or below the given row'''
        index = find_edge(self.horizontal_edges, row)
        return index
    
    def contains(self, rectangle): 
        # Check for intersecting edges.
        # If an edge intersects the interior of the rectangle,
        # it can't be contained.
        upper_left = rectangle[0][0]
        lower_right = rectangle[0][1]
        left_edge = upper_left[0]
        right_edge = lower_right[0]
        upper_edge = upper_left[1]
        lower_edge = lower_right[1]
        left_interior = left_edge+1
        right_interior = right_edge-1
        upper_interior = upper_edge+1
        lower_interior = lower_edge-1
        if does_any_edge_intersect_range(self.vertical_edges, 
                                         (left_interior, right_interior),
                                         (upper_edge, lower_edge)):
            return False
        if does_any_edge_intersect_range(self.horizontal_edges,
                                         (upper_interior, lower_interior),
                                         (left_edge, right_edge)):
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
            rectangles = [create_rectangle(red_tiles, first, second)
                       for first in range(len(red_tiles)) 
                       for second in range(first)]
            rectangles.sort(key=lambda rectangle: -rectangle[1])
            if verbose:
                print(f'Found {len(rectangles)} rectangles')
            edges = Edges(red_tiles)
            if verbose:
                print(f'Found {len(edges.horizontal_edges)} horizontal edges ', end='')
                print(f'and {len(edges.vertical_edges)} vertical edges')
                for edge in [[0]] + edges.horizontal_edges + [[100000]]:
                    test_col = edge[0]
                    col_index = edges.find_horizontal_edge(test_col)
                    if (col_index >= len(edges.horizontal_edges) or 
                        edges.horizontal_edges[col_index][0] != test_col):
                        print(f'Looking for {test_col}, found ', end='')
                        if col_index >= 0 and col_index < len(edges.horizontal_edges):
                            print(f'{edges.horizontal_edges[col_index][0]}')
                        else:
                            print(f'the end of the line')
            for rectangle in rectangles:
                if edges.contains(rectangle):
                    print(f'found a rectangle with area {rectangle[1]}', end='')
                    print(' that is contained in the region')
                    break
                else:
                    if verbose:
                        print(f'a rectangle with area {rectangle[1]}', end='')
                        print(f' was not contained')

    time_end = process_time()
    print(f'Time taken: {time_end - time_start} seconds.')

    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input(f'enter command line for {app_name}: ')
        argv.extend(command_line.split())
    main(argv[1:])