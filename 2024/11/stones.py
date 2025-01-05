#!/usr/bin/python3

# stones
'''Advent of code 2024 day 11 - Stones'''


from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError
from time import process_time


app_name = 'stones.py'


class Memoizer:
    def __init__(self):
        self.cache = {}
        return
    
    def execute_blinks(self, blinks_left, stones):
        result = 0
        self.cache = {}
        for stone in stones:
            after_blinks = self.blink(blinks_left, stone)
            print('.', end='')
            result += after_blinks
        print()
        return result
    
    def blink(self, blinks_left, stone):
        if blinks_left == 0:
            return 1
        
        cache_key = (stone, blinks_left)
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        if stone == 0:
            return_value = self.blink(blinks_left-1, 1)
        else:
            stone_label = str(stone)
            length = len(stone_label)
            if length % 2 == 0:
                left_stone = int(stone_label[:length//2])
                right_stone = int(stone_label[length//2:])
                left_stones = self.blink(blinks_left-1, left_stone)
                right_stones = self.blink(blinks_left-1, right_stone)
                return_value = left_stones + right_stones
            else:
                return_value = self.blink(blinks_left-1, stone*2024)
        self.cache[cache_key] = return_value
        return return_value


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

    memo = Memoizer()
    if verbose:
        tests = [(0, 1), (1, 1), (45, 1), (125, 6), (17, 6)]
        for test in tests:
            print(f'{test[0]} becomes {memo.blink(test[1], test[0])}')
        more_tests = [((125, 17), 6)]
        for test in more_tests:
            print(f'{test[0]} becomes {memo.execute_blinks(test[1], test[0])}')

    stones = []
    scenarios = []

    if input_file_name:
        with open(input_file_name, 'r') as input_file:
            print(f'Opened {input_file_name} for {app_name}')
            line = input_file.readline()
            stones = [int(s) for s in line.split(' ')]            

    for section in sections:
        print(f'Processing section {section}')
        if 'a' in section:
            scenarios.append(25)
        if 'b' in section:
            scenarios.append(75)
    for scenario in scenarios:    
        print(f'Processing {stones} in {scenario} blinks')
        time_start = process_time()
        final_stones = memo.execute_blinks(scenario, stones)
        print(f'after {scenario} blinks, there were {final_stones} stones')
        time_end = process_time()
        print(f'Time taken: {time_end - time_start} seconds.')

    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input(f'enter command line for {app_name}: ')
        argv.extend(command_line.split())
    main(argv[1:])