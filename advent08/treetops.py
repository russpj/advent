#!/usr/bin/python3

# treetops.py
'''Advent of code Day 8'''

from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError


app_name = 'treetops.py'


def read_grid(input_file):
    grid = []
    for line in input_file:
        numbers = line.strip()
        row = []
        for index in range(len(numbers)):
            row.append(int(numbers[index]))
        grid.append(row)
    return grid


def find_visible_trees(grid):
    visible_trees = set()
    for row in range(len(grid)):
        highest_tree = -1
        for col in range(len(grid[row])):
            if grid[row][col] > highest_tree:
                visible_trees.add((row, col))
                highest_tree = grid[row][col]
        highest_tree = -1
        for col in range(len(grid[row])-1, -1, -1):
            if grid[row][col] > highest_tree:
                visible_trees.add((row, col))
                highest_tree = grid[row][col]
    for col in range(len(grid[0])):
        highest_tree = -1
        for row in range(len(grid)):
            if grid[row][col] > highest_tree:
                visible_trees.add((row, col))
                highest_tree = grid[row][col]
        highest_tree = -1
        for row in range(len(grid)-1, -1, -1):
            if grid[row][col] > highest_tree:
                visible_trees.add((row, col))
                highest_tree = grid[row][col]
    return visible_trees


def next_tree(grid, row, col, direction):
    if direction == 'left':
        if col == 0:
            return None
        else:
            return (row, col-1)
    if direction == 'right':
        if col == len(grid[row]) - 1:
            return None
        else:
            return (row, col + 1)
    if direction == 'up':
        if row == 0:
            return None
        else:
            return (row-1, col)
    if direction == 'down':
        if row == len(grid) - 1:
            return None
        else:
            return (row+1, col)


def view_score(grid, row, col, direction):
    this_tree_height = grid[row][col]
    view_length = 0
    look_ahead = next_tree(grid, row, col, direction)
    while look_ahead:
        view_length += 1
        row = look_ahead[0]
        col = look_ahead[1]
        if grid[row][col] >= this_tree_height:
            break
        look_ahead = next_tree(grid, row, col, direction)
    return view_length


def calculate_view_score(grid, row, col):
    return (view_score(grid, row, col, 'left') * 
            view_score(grid, row, col, 'right') * 
            view_score(grid, row, col, 'up') * 
            view_score(grid, row, col, 'down'))


def calculate_view_scores(grid):
    view_scores = []
    for row in range(len(grid)):
        row_scores = []
        for col in range(len(grid[row])):
            row_scores.append(calculate_view_score(grid, row, col))
        view_scores.append(row_scores)
    return view_scores


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
            print(f'Opened {input_file_name} for {app_name}')
            tree_grid = read_grid(input_file)
            visible_trees = find_visible_trees(tree_grid)
            print(f'The forest grid has {len(visible_trees)} visible trees')

            view_scores = calculate_view_scores(tree_grid)
            max_view_score = 0
            for row in view_scores:
                row_max = max(row)
                max_view_score = max((max_view_score, row_max))
            print(f'The best view has a score of {max_view_score}')


    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input(f'enter command line for {app_name}: ')
        argv.extend(command_line.split())
    main(argv[1:])