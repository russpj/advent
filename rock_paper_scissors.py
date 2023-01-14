#!/usr/bin/python3

# rock_paper_scissors
'''Advent of code day 2'''

from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError

game_score = {
    'A': {'X': 3, 'Y': 6, 'Z': 0},
    'B': {'X': 0, 'Y': 3, 'Z': 6},
    'C': {'X': 6, 'Y': 0, 'Z': 3}
}

game_choice = {
    'A': {'X': 'Z', 'Y': 'X', 'Z': 'Y'},
    'B': {'X': 'X', 'Y': 'Y', 'Z': 'Z'},
    'C': {'X': 'Y', 'Y': 'Z', 'Z': 'X'}
}

choice_score = {
    'X': 1,
    'Y': 2,
    'Z': 3
}


def main(arguments):
    program_name = 'rock_paper_scissors'
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
            total_score = 0            
            for game in input_file:
                opponent, choice = game.strip().split(' ')
                me = game_choice[opponent][choice]
                score = game_score[opponent][me] + choice_score[me]
                total_score += score
            print(f'The total score in the rock paper scissors match was {total_score}.')

    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input('enter command line for rock_paper_scissors: ')
        argv.extend(command_line.split())
    main(argv[1:])