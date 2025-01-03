#!/usr/bin/python3

# defrag
'''Advent of Code 2024 Day 9: Disk defragmenting'''


from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError
from time import process_time


app_name = 'defrag.py'


class Disk_Block:
    def __init__(self, sector_index, size):
        self.sector_index = sector_index
        self.size = size
        return
    
    def sort_key(self):
        return self.sector_index
    

class File_Block(Disk_Block):
    def __init__(self, sector_index, size, file_id):
        super().__init__(sector_index, size)
        self.file_id = file_id
        return
    

class Free_Block(Disk_Block):
    pass


class Defragger:
    def __init__(self):
       return

    def parse(self, compressed_directory):
        self.free_block_list = []
        self.file_block_list = []
        self.sector_map = []
        reading_file = True
        file_id = 0
        for digit in compressed_directory:
            size = int(digit)
            sector_index = len(self.sector_map)
            if reading_file:
                block = File_Block(sector_index, size, file_id)
                self.file_block_list.append(block)
                self.sector_map.extend([file_id]*size)
                file_id += 1
            else:
                if size > 0:
                    block = Free_Block(sector_index, size)
                    self.free_block_list.append(block)
                    self.sector_map.extend([-1]*size)
            reading_file = not reading_file                
        return
    
    def next_free_space_index(self, start_index):
        return self.sector_map[start_index:].index(-1) + start_index
    
    def previous_file_index(self, end_index):
        while self.sector_map[end_index] == -1:
            end_index -= 1
        return end_index

    def compact_free_space(self):
        free_space_index = self.next_free_space_index(0)
        file_index = self.previous_file_index(len(self.sector_map)-1)
        while file_index > free_space_index:
            self.sector_map[file_index], self.sector_map[free_space_index] = \
            self.sector_map[free_space_index], self.sector_map[file_index]
            
            free_space_index = self.next_free_space_index(free_space_index)
            file_index = self.previous_file_index(file_index)
        return
    
    def split_free_block(self, block_index, new_first_size):
        block = self.free_block_list[block_index]
        if new_first_size < block.size:
            new_block = Free_Block(block.sector_index+new_first_size, \
                                   block.size-new_first_size)
            block.size = new_first_size
            self.free_block_list.insert(block_index+1, new_block)
        return
    
    def find_free_block(self, size):
        for free_index in range(len(self.free_block_list)):
            if self.free_block_list[free_index].size >= size:
                self.split_free_block(free_index, size)
                free_block = self.free_block_list.pop(free_index)
                return free_block
        return None
    
    def defrag_blocks(self, verbose=False):
        for file_id in range(len(self.file_block_list)-1,-1,-1):
            file_block = self.file_block_list[file_id]
            free_block = self.find_free_block(file_block.size)
            if free_block and free_block.sector_index < file_block.sector_index:
                new_free_block = Free_Block(file_block.sector_index, file_block.size)
                file_block.sector_index = free_block.sector_index
                self.free_block_list.append(new_free_block)
        self.file_block_list.sort(key=Disk_Block.sort_key)
        self.free_block_list.sort(key=Disk_Block.sort_key)
        return

    def char_for_id(self, id):
        char_map = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        if id < 10:
            return str(id)
        else:
            index = (id-10) % len(char_map)
            return char_map[index:index+1]

    def print_sector_map(self):
        for sector in self.sector_map:
            if sector == -1:
                ch_output = '.'
            else:
                ch_output = self.char_for_id(sector)
            print(ch_output, end='')
        print()
        return
    
    def print_block_list(self):
        file_index = 0
        free_index = 0
        while file_index < len(self.file_block_list) or \
            free_index < len(self.free_block_list):
            if file_index >= len(self.file_block_list):
                print_file_block = False
            elif free_index >= len(self.free_block_list):
                print_file_block = True
            else:
                print_file_block = \
                    self.file_block_list[file_index].sector_index < \
                    self.free_block_list[free_index].sector_index
            if print_file_block:
                block = self.file_block_list[file_index]
                print_ch = self.char_for_id(block.file_id)
                print_len = block.size
                file_index += 1
            else:
                block = self.free_block_list[free_index]
                print_ch = '.'
                print_len = block.size
                free_index += 1
            print(print_ch*print_len, end='')

        # for block in self.block_list:
        #     if block.free_space:
        #         print_ch = '.'
        #     else:
        #         print_ch = self.char_for_id(block.id)
        #     print(print_ch*block.size, end='')
        print()
        return
    
    def checksum(self):
        check_sum = 0
        for sector_index in range(len(self.sector_map)):
            file_id = self.sector_map[sector_index]
            if file_id != -1:
                sector_value = sector_index*file_id
                check_sum += sector_value
        return check_sum

    def checksum_block_list(self):
        check_sum = 0
        for block in self.file_block_list:
            for sector_index in range(block.sector_index, block.sector_index+block.size):
                value = sector_index*block.file_id
                check_sum += value
        return check_sum


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
                defrag.print_sector_map()

    time_start = process_time()
    for section in sections:
        print(f'Processing section {section}')
        if section == 'a':
            print(f'The original filesystem checksome is {defrag.checksum()}')
            defrag.compact_free_space()
            if verbose:
                defrag.print_sector_map()
            print(f'The compacted filesystem checksome is {defrag.checksum()}')
        if section == 'b':
            if verbose:
                defrag.print_block_list()
            print(f'The original filesystem checksome is {defrag.checksum_block_list()}')
            defrag.defrag_blocks()
            if verbose:
                defrag.print_block_list()
            print(f'The compacted filesystem checksome is {defrag.checksum_block_list()}')
    time_end = process_time()
    print(f'Time taken: {time_end - time_start} seconds.')

    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input(f'enter command line for {app_name}: ')
        argv.extend(command_line.split())
    main(argv[1:])