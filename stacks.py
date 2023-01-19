#!/usr/bin/python3

# stacks
'''Advent of code day 3'''

from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError
import re

app_name = 'stacks'

class stack():
    def __init__(this, name=''):
        this.crates = []
        this.name = name
        return


class move():
    def __init__(this, number, source, destination):
        this.number = number
        this.source = source
        this.destination = destination
        return


def create_stacks(lines):
    stacks = []
    stack_width = 4
    name_line = lines[-1]
    num_stacks = (len(name_line)+stack_width-1)//stack_width
    for stack_num in range(num_stacks):
        name = int(name_line[stack_num*stack_width:(stack_num+1)*stack_width])
        stacks.append(stack(name))
    
    for line in list(reversed(lines))[1:]:
        for stack_num in range(num_stacks):
            candidate = line[stack_num*stack_width:(stack_num+1)*stack_width]
            left_bracket = candidate.find('[')
            right_bracket = candidate.find(']')
            if left_bracket >= 0 and right_bracket >= 0:
                crate_name = candidate[left_bracket+1: right_bracket]
                stacks[stack_num].crates.append(crate_name)
    return stacks


def render_names(stacks):
    line = ''
    for stack in stacks:
        label = f' {stack.name: <3}'
        line += label
    return line

def render_crates(stacks, level):
    line = ''
    is_output = False
    for stack in stacks:
        if level < len(stack.crates):
            label = f'[{stack.crates[level]}] '
            line += label
            is_output = True
        else:
            line += '    '
    if not is_output:
        line = ''
    return line
     

def render_stacks(stacks):
    output = []
    output.append(render_names(stacks))
    crate_level = 0
    while True:
        crate_line = render_crates(stacks, crate_level)
        if not crate_line:
            break
        output.append(crate_line)
        crate_level += 1
    return reversed(output)


def main(arguments):
    program_name = app_name
    command_line_documentation = f'{program_name} --help --file [input file]'
    input_file_name = ''

    try:
        opts, args = getopt(arguments, "hf:", 
            ("help", "file="))
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
            reading_stacks = True
            stacks_definition = []
            move_instructions = []
            instruction_expression = re.compile(r'move (\d) from (\d) to (\d)')
            for line in input_file:
                if reading_stacks:
                    line = line.rstrip('\n')
                    if len(line) == 0:
                        reading_stacks = False
                    else:
                        stacks_definition.append(line)
                else:
                    matched = instruction_expression.match(line)
                    instruction = move(matched.group(1), matched.group(2), matched.group(3))
                    move_instructions.append(instruction)
            stacks = create_stacks(stacks_definition)
            picture = render_stacks(stacks)
            for line in picture:
                print(line)

            print(f'Opened {input_file_name} for input')
    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input(f'enter command line for {app_name}: ')
        argv.extend(command_line.split())
    main(argv[1:])