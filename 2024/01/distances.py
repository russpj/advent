#!/usr/bin/python3

# distances
'''Advent of code Day 01'''


from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError


app_name = 'distances.py'


def main(arguments):
    program_name = app_name
    command_line_documentation = f'{program_name} --help --afile --bfile [input file]'
    input_file_name = ''
    section = 'a'

    try:
        opts, args = getopt(arguments, "hab:", ("help", "afile=", "bfile="))
    except GetoptError:
        print(f'Invalid Arguments: {command_line_documentation}')
        exit(2)

    for opt, arg in opts:	
        if opt in ('-h', '--help'):
            print(f'usage: {command_line_documentation}')
            exit(0)

        if opt in ('-a', '--afile'):
            input_file_name = arg
            section = 'a'

        if opt in ('-b', '--bfile'):
            input_file_name = arg
            section = 'b'

    if input_file_name:
        left_list = []
        right_list = []
        with open(input_file_name, 'r') as input_file:
            print(f'Opened {input_file_name} for {app_name} section {section}')
            for line in input_file:
                left, right = [int(x) for x in line.split()]
                left_list.append(left)
                right_list.append(right)
        left_list = sorted(left_list)
        right_list = sorted(right_list)

        if section == 'a':
            sum = 0
            for pair in zip(left_list, right_list):
                difference = abs(pair[0]-pair[1])
                sum += difference
            print(f'The total distances of the {len(left_list)} pairs is {sum}')

        if section == 'b':
            total_similarity = 0
            for element in left_list:
                similarity = element * right_list.count(element)
                total_similarity += similarity
            print(f'The total similarity of the two lists is {total_similarity}')

    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input(f'enter command line for {app_name}: ')
        argv.extend(command_line.split())
    main(argv[1:])