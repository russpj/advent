#!/usr/bin/python3

# rope
'''Advent of code Day 9'''


from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError


app_name = 'rope.py'


class Rope():
    def __init__(this):
        this.head_pos = (0,0)
        this.tail_pos = (0,0)

    def print(this):
        print(f'The head is at {this.head_pos}, and the tail at {this.tail_pos}')

    def move_head(this, direction, steps):
        if direction == 'R':
            print(f'Right {steps}')
            this.head_pos = (this.head_pos(0) + steps, this.head_pos(1))
        if direction == 'U':
            print(f'Up {steps}')
            this.head_pos = (this.head_pos(0), this.head_pos(1)+steps)
        if direction == 'L':
            print(f'Left {steps}')
            this.head_pos = (this.head_pos(0)-steps, this.head_pos(1))
        if direction == 'D':
            print(f'Right {steps}')
            this.head_pos = (this.head_pos(0), this.head_pos(1)-steps)


def main(arguments):
    program_name = app_name
    command_line_documentation = f'{program_name} --help --file [input file]'
    input_file_name = ''

    try:
        opts, args = getopt(arguments, "hf:", ("help", "file="))
    except GetoptError:
        print(f'Invalid Arguments: {command_line_documentation}')
        exit(2)

    for opt, arg in opts:	
        if opt in ('-h', '--help'):
            print(f'usage: {command_line_documentation}')
            exit(0)

        if opt in ('-f', '--file'):
            input_file_name = arg

    if input_file_name:
        with open(input_file_name, 'r') as input_file:
            print(f'Opened {input_file_name} for {app_name}')


    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input(f'enter command line for {app_name}: ')
        argv.extend(command_line.split())
    main(argv[1:])