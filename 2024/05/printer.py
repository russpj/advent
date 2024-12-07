#!/usr/bin/python3

# printer
'''Advent of code day 05'''


from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError


app_name = 'printer.py'


def process_rule(line, rules):
    rule_parts = line.split('|')
    if len(rule_parts) == 2:
        below = int(rule_parts[0])
        above = int(rule_parts[1])
        if below in rules:
            current_above_list = rules[below]
            current_above_list.append(above)
            rules[below] = current_above_list
        else:
            rules[below] = [above]
        return True
    return False


def is_valid_pamphlet(line, rules):
    return False, 0


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

    rules = {}
    pamphlets = []

    if input_file_name:
        with open(input_file_name, 'r') as input_file:
            print(f'Opened {input_file_name} for {app_name}')
            for line in input_file:
                if not process_rule(line, rules):
                    pages = [int(n) for n in line.strip().split(',') if len(n) > 0]
                    if len(pages) > 0:
                        pamphlets.append(pages)
        print(f'Found {len(rules)} rules and {len(pamphlets)} pamphlets')

    for section in sections:
        print(f'Processing section {section}')
        if section == 'a':
            sum_middle_pages = 0
            count_valid = 0
            for pamphlet in pamphlets:
                valid, page_list = is_valid_pamphlet(pamphlet, rules)
                if valid:
                    count_valid += 1
                    middle_page = page_list[len(page_list)//2]
                    sum_middle_pages += middle_page
            print(f'The sum of the middle pages of {count_valid} pamphlets was {sum_middle_pages}')
    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input(f'enter command line for {app_name}: ')
        argv.extend(command_line.split())
    main(argv[1:])