#!/usr/bin/python3

# calories
'''Advent of code day 1 part 1'''

from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError


def read_calories_for_elves(input_file):
    sum_of_calories = 0

    for line in input_file:
        line = line.strip()
        if len(line) == 0:
            if sum_of_calories == 0:
                # keep reading lines before 
                pass
            else:
                yield sum_of_calories
                sum_of_calories = 0
        else:
            calories = int(line)
            sum_of_calories += calories
    if sum_of_calories:
        yield sum_of_calories
    return


def bubble_up(numbers):
    for index in range(len(numbers)-1):
        if numbers[index] > numbers[index+1]:
            numbers[index], numbers[index+1] = numbers[index+1], numbers[index]
    return


def top_n(numbers, n):
    top_n_numbers = [0]*n
    for number in numbers:
        if number > top_n_numbers[0]:
            top_n_numbers[0] = number
            bubble_up(top_n_numbers)
    return top_n_numbers


def main(arguments):
    program_name = 'calories'
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
        max_calories = 0
        top_elves = 3
        with open(input_file_name, 'r') as input_file:
            top_3 = top_n(read_calories_for_elves(input_file), top_elves)

        print(f'the {top_elves} elves with the most nutrition had {sum(top_3)} calories.')


    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input('enter command line for calories: ')
        argv.extend(command_line.split())
    main(argv[1:])