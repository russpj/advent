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


def is_valid_pamphlet(pages, rules):
    for index in range(len(pages)):
        test_page = pages[index]
        if test_page in rules:
            invalid_pages = rules[test_page]
            for invalid_page_index in range(index):
                if pages[invalid_page_index] in invalid_pages:
                    return False
    return True


def make_valid_pamphlet(pages, rules):
    made_changes = False
    for index in range(len(pages)):
        new_index = index
        test_page = pages[index]
        if test_page in rules:
            invalid_pages = rules[test_page]
            while new_index > 0:
                index_compare = new_index-1
                if pages[index_compare] in invalid_pages:
                    made_changes = True
                    pages[new_index], pages[index_compare] = pages[index_compare], pages[new_index]
                    new_index -= 1
                else:
                    return made_changes
    return made_changes


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
        if section == 'a' or section == 'b':
            sum_valid_middle_pages = 0
            count_valid = 0
            sum_invalid_middle_pages = 0
            count_invalid = 0
            for pamphlet in pamphlets:
                valid = not make_valid_pamphlet(pamphlet, rules)
                if valid:
                    count_valid += 1
                    middle_page = pamphlet[len(pamphlet)//2]
                    sum_valid_middle_pages += middle_page
            print(f'The sum of the middle pages of {count_valid} pamphlets was {sum_valid_middle_pages}')
    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input(f'enter command line for {app_name}: ')
        argv.extend(command_line.split())
    main(argv[1:])