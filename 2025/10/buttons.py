#!/usr/bin/python3

# buttons
'''Advent of code (2025) day 10, starting the machines'''


from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError
from time import process_time
from collections import deque
from functools import cache


app_name = 'buttons.py'


def parse_machine(line):
    button_rules = []
    segments = line.split()
    for segment in segments:
        if segment[0] == '[':
            # parse the target light configuration
            target_lights = segment[1:-1]
            num_lights = len(target_lights)
        if segment[0] == '(':
            # parse a button rule
            toggles = [int(x) for x in segment[1:-1].split(',')]
            rule = [0]*num_lights
            for toggle in toggles:
                rule[toggle] = 1
            button_rules.append(tuple(rule))
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


def apply_rule_lights(light_state, rule):
    lights = []
    for light_index in range(len(light_state)):
        if rule[light_index]:
            lights.append(toggle_light(light_state[light_index]))
        else:
            lights.append(light_state[light_index])
    return ''.join(lights)


def apply_rule_joltage(joltage_state, rule):
    joltages = [joltage for joltage in joltage_state]
    for joltage_index in range(len(joltage_state)):
        joltages[joltage_index] += rule[joltage_index]
    return tuple(joltages)


def click_buttons_lights(machine):
    target_lights = machine[0]
    button_rules = machine[1]
    initial_lights = '.'*len(target_lights)
    click_result = (0, initial_lights)
    click_results = deque()
    click_results.append(click_result)
    queued_targets = set()

    while click_results:
        previous_clicks, light_state = click_results.popleft()
        for rule in button_rules:
            click_result = apply_rule_lights(light_state, rule)
            if click_result == target_lights:
                return previous_clicks+1
            if not click_result in queued_targets:
                queued_targets.add(click_result)
                click_results.append((previous_clicks+1, click_result))
    return


def joltages_too_high(joltages, target_joltages):
    for joltage_index in range(len(joltages)):
        if joltages[joltage_index] > target_joltages[joltage_index]:
            return True
    return False


def click_buttons_joltages_old(machine, verbose):
    target_joltages = machine[2]
    button_rules = machine[1]
    initial_joltages = [0]*len(target_joltages)
    click_result = (0, initial_joltages)
    click_results = deque()
    click_results.append(click_result)
    queued_targets = set()
    if verbose:
        last_clicks = 0

    while click_results:
        previous_clicks, joltage_state = click_results.popleft()
        if verbose and previous_clicks > last_clicks:
            last_clicks = previous_clicks
            print(f'{last_clicks} clicks, {len(click_results)} queued states')
        for rule in button_rules:
            click_result = apply_rule_joltage(joltage_state, rule)
            if click_result == target_joltages:
                return previous_clicks+1
            if not click_result in queued_targets:
                if not joltages_too_high(click_result, target_joltages):
                    queued_targets.add(click_result)
                    click_results.append((previous_clicks+1, click_result))
                else:
                    pass
            else:
                pass
    return


def click_buttons_joltages(machine, verbose):
    rules = machine[1]
    target_joltages = machine[2]
    round = max(target_joltages)
    while round < 100:
        if satisfy(round, target_joltages, rules):
            return round
        round += 1
    return round


def next_digits(digits, sum_digits):
    digit_index = 0

    0, 0, 0, 3
    0, 0, 1, 2
    0, 0, 2, 1
    0, 0, 3, 0
    0, 1, 0, 2
    0, 1, 1, 1
    0, 1, 2, 0
    0, 2, 0, 1
    0, 2, 1, 0
    0, 3, 0, 0
    1, 0, 0, 2
    1, 0, 1, 1
    1, 0, 2, 0
    1, 1, 0, 1
    1, 1, 1, 0
    1, 2, 0, 0
    2, 0, 0, 1
    2, 0, 1, 0
    2, 1, 0, 0
    3, 0, 0, 0


    return False


def odometer(num_digits, range_digits):
    if num_digits == 1:
        return [range_digits]
    for trial in range(range_digits):
        for more_digits in odometer(num_digits-1, range_digits-trial):
            digits = [trial] + more_digits
            yield digits
    return


def reverse_rule(rule, joltages):
    reversal = [joltages[i] - rule[i] for i in range(len(rule))]
    return tuple(reversal)


def all_zero(numbers):
    return all([number==0 for number in numbers])


def any_negative(numbers):
    return any([number < 0 for number in numbers])

@cache
def satisfy(rounds_left, current_joltages, rules):
    if rounds_left == 0:
        return all_zero(current_joltages)
    if any_negative(current_joltages):
        return False
    for rule in rules:
        joltages = reverse_rule(rule, current_joltages)
        satisfied = satisfy(rounds_left-1, joltages, rules)
        if satisfied:
            return True
    return False


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
                button_clicks += click_buttons_lights(machine)
                if verbose:
                    print(f'{button_clicks} so far ...')
            print(f'It took {button_clicks} button clicks to light the lights correctly.')
        if part == '2':
            button_clicks = 0
            for machine in machines:
                button_clicks += click_buttons_joltages(machine, verbose)
                if verbose:
                    print(f'{button_clicks} so far ...')
            print(f'It took {button_clicks} button clicks to set the joltages correctly.')
        if part == '3':
            test_cases = ((3, 3), (6, 7), (6, 10), (5, 12), (4, 11))
            for test in test_cases:
                for answer in odometer(test[0], test[1]):
                    print(answer)
    time_end = process_time()
    print(f'Time taken: {time_end - time_start} seconds.')

    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input(f'enter command line for {app_name}: ')
        argv.extend(command_line.split())
    main(argv[1:])