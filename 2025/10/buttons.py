#!/usr/bin/python3

# buttons
'''Advent of code (2025) day 10, starting the machines'''


from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError
from time import process_time
from collections import deque


app_name = 'buttons.py'


def parse_machine(line):
    button_rules = []
    segments = line.split()
    for segment in segments:
        if segment[0] == '[':
            # parse the target light configuration
            target_lights = segment[1:-1]
        if segment[0] == '(':
            # parse a button rule
            rule = [int(x) for x in segment[1:-1].split(',')]
            button_rules.append(rule)
        if segment[0] == '{':
            # parse joltage requirement 
            joltages = [int(x) for x in segment[1:-1].split(',')]
    return (target_lights, tuple(button_rules), tuple(joltages)) 


def toggle_light(light):
    if light == '.':
        return '#'
    if light == '#':
        return '.'
    return light


def apply_rule(light_state, rule):
    lights = []
    for light_index in range(len(light_state)):
        if light_index in rule:
            lights.append(toggle_light(light_state[light_index]))
        else:
            lights.append(light_state[light_index])
    return ''.join(lights)


def click_buttons(machine):
    target_lights = machine[0]
    button_rules = machine[1]
    initial_lights = '.'*len(target_lights)
    click_result = (0, initial_lights)
    click_results = deque()
    click_results.append(click_result)

    while deque:
        previous_clicks, light_state = click_results.popleft()
        for rule in button_rules:
            click_result = apply_rule(light_state, rule)
            if click_result == target_lights:
                return previous_clicks+1
            click_results.append((previous_clicks+1, click_result))
    return click_result[0]


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

    machines = []

    if input_file_name:
        with open(input_file_name, 'r') as input_file:
            if verbose:
                print(f'Opened {input_file_name} for {app_name}')
            for line in input_file:
                machines.append(parse_machine(line))

    time_start = process_time()
    for part in parts:
        print(f'Processing part {part}')
        if part == '1':
            button_clicks = 0
            for machine in machines:
                button_clicks += click_buttons(machine)
                if verbose:
                    print(f'{button_clicks} so far ...')
            print(f'It took {button_clicks} button clicks to light the lights correctly.')
    time_end = process_time()
    print(f'Time taken: {time_end - time_start} seconds.')

    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input(f'enter command line for {app_name}: ')
        argv.extend(command_line.split())
    main(argv[1:])