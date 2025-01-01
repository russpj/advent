#!/usr/bin/python3

# antinodes
'''Advent of code template'''


from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError
from time import process_time
from string import ascii_letters, digits


app_name = 'antinodes.py'

class Stations:
    def __init__(self):
        self.locations = {}
        self.station_names = list(ascii_letters+digits)
        self.num_cols = 0
        self.num_rows = 0

    def read_file(self, file):
        row = 0
        for line in file:
            line = line.strip()
            for col in range(len(line)):
                station = line[col]
                if station in self.station_names:
                    self.add_station(station, row, col)
            self.num_cols = col
            row += 1
        self.num_rows = row
        return
    
    def unique_pairs(self, n):
        for first in range(n):
            for second in range(first+1, n):
                yield (first, second)
        return
    
    def station_pairs(self):
        for station in self.locations:
            locations = self.locations[station]
            for pair in self.unique_pairs(len(locations)):
                pair_locations = (locations[pair[0]], locations[pair[1]])
                yield (station, pair_locations)
    
    def print_station_pairs(self):
        for station_pair in self.station_pairs():
            print(f'{station_pair}')
        return
    
    def add_station(self, station, row, col):
        if station in self.locations:
            locations = self.locations[station]
            locations.append((row, col))
        else:
            self.locations[station] = [(row, col)]
        return
    
    def location_pair_difference(self, location_pair):
        return (location_pair[1][0] - location_pair[0][0], \
                location_pair[1][1] - location_pair[0][1])
    
    def location_pair_subtract(self, location_pair, delta):
        return (location_pair[0][0]-delta[0], \
                location_pair[0][1]-delta[1])
    
    def location_pair_add(self, location_pair, delta):
        return (location_pair[1][0]+delta[0], \
                location_pair[1][1]+delta[1])
    
    def is_in_map(self, location):
        row, col = location
        if row < 0 or row >= self.num_rows:
            return False
        if col < 0 or col >= self.num_cols:
            return False
        return True
    
    def find_antinodes(self):
        self.antinodes = []
        for station_pair in self.station_pairs():
            location_pair = station_pair[1]
            delta = self.location_pair_difference(location_pair)
            lower_antinode = self.location_pair_subtract(location_pair, delta)
            upper_antinode = self.location_pair_add(location_pair, delta)
            if self.is_in_map(lower_antinode):
                self.antinodes.append(lower_antinode)
            if self.is_in_map(upper_antinode):
                self.antinodes.append(upper_antinode)
        return
    
    def print_antinodes(self):
        print(f'Antinodes:')
        for antinode in sorted(self.antinodes):
            print(f'{antinode}')
        

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

    stations = Stations()
    if input_file_name:
        with open(input_file_name, 'r') as input_file:
            print(f'Opened {input_file_name} for {app_name}')
            stations.read_file(input_file)

    time_start = process_time()
    for section in sections:
        print(f'Processing section {section}')
        if verbose:
            stations.print_station_pairs()
        stations.find_antinodes()
        if verbose:
            stations.print_antinodes()
        print(f'There are {len(stations.antinodes)} antinodes in the map')
    time_end = process_time()
    print(f'Time taken: {time_end - time_start} seconds.')

    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input(f'enter command line for {app_name}: ')
        argv.extend(command_line.split())
    main(argv[1:])