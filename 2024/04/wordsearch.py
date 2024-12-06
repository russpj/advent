#!/usr/bin/python3

# wordsearch
'''Advent of code Day 04 Word Search'''


from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError


app_name = 'wordsearch.py'

def across_strides(letter_grid):
    for stride in letter_grid:
        yield stride


def down_strides(letter_grid):
    num_rows = len(letter_grid)
    if num_rows == 0:
        return
    num_cols = len(letter_grid[0])
    for col in range(num_cols):
        yield ''.join([letter_grid[row][col] for row in range(num_rows)])


def word_search_strides(letter_grid):
    for stride in across_strides(letter_grid):
        yield stride
        yield stride[::-1]
    for stride in down_strides(letter_grid):
        yield stride
        yield stride[::-1]


def main(arguments):
    program_name = app_name
    command_line_documentation = f'{program_name} --help --section [a|b] --file [input file]'
    input_file_name = ''
    sections = []

    try:
        opts, args = getopt(arguments, "hs:f:", ("help", "section=", "file="))
    except GetoptError:
        print(f'Invalid Arguments: {command_line_documentation}')
        exit(2)

    for opt, arg in opts:	
        if opt in ('-h', '--help'):
            print(f'usage: {command_line_documentation}')
            exit(0)

        if opt in ('-f', '--file'):
            input_file_name = arg

        if opt in ('-s', '--section'):
            for section in arg:
                sections.append(section)

    if input_file_name:
        with open(input_file_name, 'r') as input_file:
            print(f'Opened {input_file_name} for {app_name}')
            letter_grid = []
            for line in input_file:
                letter_grid.append(line.strip())

    for section in sections:
        print(f'Processing section {section}')
        if section == 'a':
            for line in word_search_strides(letter_grid):
                print(line)

    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input(f'enter command line for {app_name}: ')
        argv.extend(command_line.split())
    main(argv[1:])