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

    def read_file(self, file):
        row = 0
        for line in file:
            line = line.strip()
            for col in range(len(line)):
                station = line[col]
                if station in self.station_names:
                    self.add_station(station, row, col)
            row += 1
        return
    
    def unique_pairs(self, n):
        for first in range(n):
            for second in range(first+1, n):
                yield (first, second)
        return
    
    def print_station_pairs(self):
        for station in self.locations:
            print(f'Station {station}: ', end='')
            locations = self.locations[station]
            for pair in self.unique_pairs(len(locations)):
                print(f'({locations[pair[0]]},{locations[pair[1]]})  ', end = '')
            print()

    def add_station(self, station, row, col):
        if station in self.locations:
            locations = self.locations[station]
            locations.append((row, col))
        else:
            self.locations[station] = [(row, col)]
        return
        

def main(arguments):
    program_name = app_name
    command_line_documentation = f'{program_name} --help --section [a|b] --file [input file]'
    input_file_name = ''
    sections = []

    try:
        opts, args = getopt(arguments, "hs:f:", ("help", "section=", "file="))
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

    stations = Stations()
    if input_file_name:
        with open(input_file_name, 'r') as input_file:
            print(f'Opened {input_file_name} for {app_name}')
            stations.read_file(input_file)

    time_start = process_time()
    for section in sections:
        print(f'Processing section {section}')
        stations.print_station_pairs()
    time_end = process_time()
    print(f'Time taken: {time_end - time_start} seconds.')

    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input(f'enter command line for {app_name}: ')
        argv.extend(command_line.split())
    main(argv[1:])