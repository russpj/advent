#!/usr/bin/python3

# ingredients
'''Advent of code (2025) 05 - testing ingredients'''


from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError
from time import process_time
from operator import itemgetter


app_name = 'ingredients.py'


def in_range(item, ranges):
    for range in ranges:
        if item > range[0] and item <= range[1]:
            return True
    return False


def merge_ranges(ranges):
    ranges.sort()
    current_range_index = 0
    while current_range_index < len(ranges)-1:
        current_range = ranges[current_range_index]
        next_range = ranges[current_range_index+1]
        if current_range[1] < next_range[0]:
            current_range_index += 1
        else:
            if current_range[1] <= next_range[1]:
                ranges[current_range_index] = list((current_range[0], next_range[1]))
            ranges.pop(current_range_index+1)
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

    fresh_ranges = []
    ingredients_to_test = []

    if input_file_name:
        with open(input_file_name, 'r') as input_file:
            print(f'Opened {input_file_name} for {app_name}')
            reading_ranges = True
            for line in input_file:
                line = line.strip()
                if reading_ranges:
                    if line:
                        first, last = line.split('-')
                        fresh_ranges.append((int(first), int(last)))
                    else:
                        reading_ranges = False
                else:
                    ingredients_to_test.append(int(line))

    time_start = process_time()
    for section in sections:
        print(f'Processing section {section}')
        if section == 'a':
            count_of_fresh_ingredients = 0
            for ingredient in ingredients_to_test:
                if in_range(ingredient, fresh_ranges):
                    count_of_fresh_ingredients += 1
            print(f'{count_of_fresh_ingredients} of the ingredients were fresh')
        
        if section == 'b':
            merge_ranges(fresh_ranges)
            count_of_fresh_ids = 0
            for range in fresh_ranges:
                count_of_fresh_ids += (range[1]-range[0] + 1)
            print(f'there are {count_of_fresh_ids} possible fresh ingredients')
            
    if verbose:
        print('Debugging output goes here')
    time_end = process_time()
    print(f'Time taken: {time_end - time_start} seconds.')

    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input(f'enter command line for {app_name}: ')
        argv.extend(command_line.split())
    main(argv[1:])