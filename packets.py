#!/usr/bin/python3

# packets
'''Advent of code day 3'''

from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError

app_name = 'packets'


class marker_finder():
    def __init__(this):
        this.prefix = ''
        this.num_uniq = 0
        return

    def add_char(this, char):
        if char == '\n':
            return -1
        this.prefix += char
        for look_back in range(1, this.num_uniq+1):
            if look_back > len(this.prefix):
                this.num_uniq += 1
                return this.num_uniq
            if char == this.prefix[-(look_back+1)]:
                this.num_uniq = look_back
                return this.num_uniq
        this.num_uniq += 1
        return this.num_uniq


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
            for line in input_file:
                marker = marker_finder()
                for char in line:
                    num_unique = marker.add_char(char)
                    if num_unique == 14:
                        break
                if num_unique == -1:
                    print(f'No marker found in {marker.prefix}.')
                else:
                    print(f'Found the marker. Message starts at {len(marker.prefix)}. The prefix was {marker.prefix}.')

    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input(f'enter command line for {app_name}: ')
        argv.extend(command_line.split())
    main(argv[1:])