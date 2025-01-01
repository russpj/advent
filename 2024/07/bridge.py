#!/usr/bin/python3

# bridge
'''Advent of code template'''


from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError


app_name = 'bridge.py'


class Evaluator:
    def __init__(self):
        self.operators = ['+', '*']

    def evaluate_operator(self, operator, left, right):
        if operator == '+':
            return left+right
        if operator == '*':
            return left*right
        return 0

    def possible_values(self, accumulator, operands):
        if len(operands) == 0:
            yield accumulator
        else:
            for operator in self.operators:
                result = self.evaluate_operator(operator, accumulator, operands[0])
                yield from self.possible_values(result, operands[1:])

    def can_equation_be_valid(self, equation):
        target = equation[0]
        operands = equation[1]
        for value in self.possible_values(operands[0], operands[1:]):
            if value == target:
                return True
        return False


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
            equations = []
            for line in input_file:
                target, operands = line.split(':')
                target = int(target)
                operands = operands.strip().split(' ')
                operands = [int(x) for x in operands]
                equations.append((target, operands))

    for section in sections:
        print(f'Processing section {section}')
        if 'a' in sections:
            sum_of_targets = 0
            evaluator = Evaluator()
            for equation in equations:
                if evaluator.can_equation_be_valid(equation):
                    sum_of_targets += equation[0]
            print(f'The sum of valid targets is {sum_of_targets}')

    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input(f'enter command line for {app_name}: ')
        argv.extend(command_line.split())
    main(argv[1:])