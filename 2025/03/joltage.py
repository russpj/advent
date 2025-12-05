#!/usr/bin/python3

# joltage
'''Advent of code (2025) joltage calculator'''


from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError
from time import process_time


app_name = 'joltage.py'


def maximize_joltage_two_pass(battery):
    max_joltage_first = 0
    first_cell = 0
    for cell in range(len(battery)-1):
        if int(battery[cell]) > max_joltage_first:
            first_cell = cell
            max_joltage_first = int(battery[first_cell])

    max_joltage_second = 0
    second_cell = first_cell+1
    for cell in range(first_cell+1, len(battery)):
        if int(battery[cell]) > max_joltage_second:
            second_cell = cell
            max_joltage_second = int(battery[second_cell])

    return max_joltage_first*10 + max_joltage_second



def maximize_joltage(battery, num_cells):
    picked_cells = list(range(num_cells))

    for next_cell in range(1, len(battery)):
        next_cell_value = battery[next_cell]
        for voltage_cell in range(num_cells):
            if next_cell+num_cells-voltage_cell <= len(battery):
                if next_cell_value > battery[picked_cells[voltage_cell]]:
                    picked_cells[voltage_cell] = next_cell
                    for increment in range(voltage_cell+1, num_cells):
                        picked_cells[increment] = picked_cells[increment-1]+1
                    break;

    joltage = 0
    for index in picked_cells:
        joltage *= 10
        joltage += int(battery[index])
    return joltage


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
    for section in sections:
        print(f'Processing section {section}')
        if section == 'a':
            total_joltage = 0
            if input_file_name:
                with open(input_file_name, 'r') as input_file:
                    print(f'Opened {input_file_name} for {app_name}')
                    for battery in input_file:
                        joltage = maximize_joltage(battery.strip(), 2)
                        total_joltage += joltage
                        if verbose:
                            other_joltage = maximize_joltage_two_pass(battery.strip())
                            if joltage != other_joltage:
                                print(f'{battery} gets {joltage} and {other_joltage}')
            print(f'the highest voltage we can get is {total_joltage}')

    time_end = process_time()
    print(f'Time taken: {time_end - time_start} seconds.')

    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input(f'enter command line for {app_name}: ')
        argv.extend(command_line.split())
    main(argv[1:])