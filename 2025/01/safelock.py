#!/usr/bin/python3

# advent
'''Advent of code (2025) 01 - Safe combination'''


from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError
from time import process_time


app_name = 'safelock.py'


class Dial:
    def __init__(self, pos, limit):
        self.pos = pos 
        self.limit = limit

    def move_dial(self, instruction):
        direction, amount = self.parse(instruction)
        if direction == 'L':
            amount = -amount
        self.pos += amount
        self.pos = self.pos%self.limit

    def move_dial_clicks(self, instruction, pos_click):
        pass_click = False
        direction, amount = self.parse(instruction)
        if direction == 'L':
            new_pos = (self.pos - amount)%self.limit
            if new_pos < self.pos:
                if new_pos <= pos_click < self.pos:
                    pass_click = True
            else:
                new_pos = self.pos - amount + self.limit
                if pos_click < self.pos or new_pos <= pos_click:
                    pass_click = True
        else:
            new_pos = (self.pos+amount)%self.limit
            if new_pos > self.pos:
                if self.pos < pos_click <= new_pos:
                    pass_click = True
            else:
                if self.pos < pos_click or pos_click <= new_pos:
                    pass_click = True
                        
        self.pos = new_pos
        return 1 if pass_click else 0

    def parse(self, instruction):
        direction = instruction[0]
        amount = int(instruction[1:])
        return (direction, amount)
    
    def count_positions(self, instructions, pos_land):
        count_pos = 0
        for instruction in instructions:
            self.move_dial(instruction)
            if self.pos == pos_land:
                count_pos +=1
        return count_pos
    
    def count_clicks(self, instructions, pos_pass):
        clicks_count = 0
        for instruction in instructions:
            pos_current = self.pos
            clicks_count += self.move_dial_clicks(instruction, pos_pass)
        return clicks_count
    

def test(dial, expected):
    if dial.pos != expected:
        print (f'Expected: {expected}, Actual: {dial.pos}')

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



    time_start = process_time()
    dial = Dial(50, 100)

    for section in sections:
        print(f'Processing section {section}')
        test_position = 0
        if section == 'a':
            if input_file_name:
                with open(input_file_name, 'r') as input_file:
                    print(f'Opened {input_file_name} for {app_name}')
                    count = dial.count_positions(input_file, test_position)
                    print(f'We found the {test_position} position {count} times')

        if section == 'b':
            if input_file_name:
                with open(input_file_name, 'r') as input_file:
                    print(f'Opened {input_file_name} for {app_name}')
                    count = dial.count_clicks(input_file, test_position)
                    print(f'We passed the {test_position} position {count} times')

    if verbose:
        print('Debugging output goes here')
        print('Running some tests')
        test(dial, 50)
        dial.move_dial("R10")
        test(dial, 60)
        dial.move_dial("L20")
        test(dial, 40)
        dial.move_dial("L50")
        test(dial, 90)
        dial.move_dial("R10")
        test(dial, 0)

    time_end = process_time()
    print(f'Time taken: {time_end - time_start} seconds.')

    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input(f'enter command line for {app_name}: ')
        argv.extend(command_line.split())
    main(argv[1:])