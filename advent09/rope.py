#!/usr/bin/python3

# rope
'''Advent of code Day 9'''


from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError


app_name = 'rope.py'


class Rope():
    def __init__(this):
        this.knots = []
        this.knots.append((0,0))
        this.knots.append((0,0))
        this.tail_positions = set()

    def print(this):
        head = this.knots[0]
        tail = this.knots[1]
        this.tail_positions.add(tail)
        print(f'The head is at {head}, and the tail at {tail}')
        print(f'The tail has been in {len(this.tail_positions)} positions.')

    def move_head(this, direction, steps):
        if direction == 'R':
            print(f'Right {steps}')
        if direction == 'U':
            print(f'Up {steps}')
        if direction == 'L':
            print(f'Left {steps}')
        if direction == 'D':
            print(f'Right {steps}')
        for step in range(steps):
            this.move_head_one_step(direction)
            this.move_tails()
            this.print()

    def move_head_one_step(this, direction):
        head = this.knots[0]
        if direction == 'R':
            print(f'Right')
            head = (head[0], head[1]+1)
        if direction == 'U':
            print(f'Up')
            head = (head[0]+1, head[1])
        if direction == 'L':
            print(f'Left')
            head = (head[0], head[1]-1)
        if direction == 'D':
            print(f'Right')
            head = (head[0]-1, head[1])
        this.knots[0] = head

    def move_tails(this):
        for tail_index in range(1, len(this.knots)):
            head_index = tail_index-1
            head_row, head_col = this.knots[head_index]
            tail_row, tail_col = this.knots[tail_index]
            if abs(head_row-tail_row) <= 1 and abs(head_col-tail_col) <= 1:
                return
            if head_row == tail_row:
                if head_col < tail_col:
                    this.knots[tail_index] = (tail_row, tail_col-1)
                else:
                    this.knots[tail_index] = (tail_row, tail_col+1)
            elif head_col == tail_col:
                if head_row < tail_row:
                    this.knots[tail_index] = (tail_row-1, tail_col)
                else:
                    this.knots[tail_index] = (tail_row+1, tail_col)
            elif head_row < tail_row:
                if head_col < tail_col:
                    this.knots[tail_index] = (tail_row-1, tail_col-1)
                else:
                    this.knots[tail_index] = (tail_row-1, tail_col+1)
            elif head_row > tail_row:
                if head_col < tail_col:
                    this.knots[tail_index] = (tail_row+1, tail_col-1)
                else:
                    this.knots[tail_index] = (tail_row+1, tail_col+1)


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
            rope = Rope()
            rope.print()
            for command in input_file:
                direction, steps = command.strip().split()
                rope.move_head(direction, int(steps))

    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input(f'enter command line for {app_name}: ')
        argv.extend(command_line.split())
    main(argv[1:])