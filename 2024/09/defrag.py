#!/usr/bin/python3

# defrag
'''Advent of Code 2024 Day 9: Disk defragmenting'''


from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError
from time import process_time


app_name = 'defrag.py'


class Disk_Block:
    def __init__(self, size, free_space=False, id=None):
        self.size = size
        self.free_space = free_space
        if self.free_space:
            if not id is None:
                raise Exception('Disk_Block: free space does not have an id')
            self.id = id
        else:
            if self.size <= 0:
                raise Exception('Disk_Block: files must have a positive size')
            self.id = id
            if self.id is None:
                raise Exception('Disk_Block: files must have ids')
        return


class Defragger:
    def __init__(self):
       return

    def parse(self, compressed_directory):
        self.block_list = []
        self.sector_map = []
        reading_file = True
        file_id = 0
        for digit in compressed_directory:
            size = int(digit)
            if reading_file:
                block = Disk_Block(size, id=file_id)
                self.block_list.append(block)
                self.sector_map.extend([file_id]*size)
                file_id += 1
            else:
                if size > 0:
                    block = Disk_Block(size, free_space=True)
                    self.block_list.append(block)
                    self.sector_map.extend([-1]*size)
            reading_file = not reading_file                
        return

    def char_for_id(self, id):
        char_map = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        if id < 10:
            return str(id)
        else:
            index = (id-10) % len(char_map)
            return char_map[index:index+1]

    def print_disk_map(self):
        for sector in self.sector_map:
            if sector == -1:
                ch_output = '.'
            else:
                ch_output = self.char_for_id(sector)
            print(ch_output, end='')
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

    defrag = Defragger()

    if input_file_name:
        with open(input_file_name, 'r') as input_file:
            print(f'Opened {input_file_name} for {app_name}')
            compressed_data = input_file.readline()
            defrag.parse(compressed_data)
            if verbose:
                defrag.print_disk_map()

    time_start = process_time()
    for section in sections:
        print(f'Processing section {section}')
    time_end = process_time()
    print(f'Time taken: {time_end - time_start} seconds.')

    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input(f'enter command line for {app_name}: ')
        argv.extend(command_line.split())
    main(argv[1:])