#!/usr/bin/python3

# network
'''Advent of code (2025) day 11 network'''


from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError
from time import process_time
from collections import deque


app_name = 'network.py'


def parse_graph(file):
    graph = {}
    for line in file:
        node1, destinations = line.split(':')
        graph[node1] = destinations.split()
    return graph


def count_paths(graph, start, end):
    queue = deque()
    num_paths = 0
    queue.append(start)
    while queue:
        this_node = queue.popleft()
        if this_node == end:
            num_paths += 1
        else:
            destinations = graph[this_node]
            for destination in destinations:
                queue.append(destination)
    return num_paths


def count_paths_waypoints(graph, start, end, waypoints):
    queue = deque()
    num_paths = 0
    waypoint_list = tuple([False]*len(waypoints))
    queue.append((start, waypoint_list))
    while queue:
        this_node = queue.popleft()
        node_value = this_node[0]
        waypoint_list = this_node[1]
        if node_value == end:
            num_paths += 1
        else:
            destinations = graph[node_value]
            for destination in destinations:
                queue.append((destination, waypoint_list))
    return num_paths


def main(arguments):
    program_name = app_name
    command_line_documentation = f'{program_name} --help --verbose --part [1|2] --file [input file]'
    verbose = False
    input_file_name = ''
    parts = []

    try:
        opts, args = getopt(arguments, "hvp:f:", ("help", "verbose", "part=", "file="))
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

        if opt in ('-p', '--part'):
            for part in arg:
                parts.append(part)

    if input_file_name:
        with open(input_file_name, 'r') as input_file:
            if verbose:
                print(f'Opened {input_file_name} for {app_name}')
            graph = parse_graph(input_file)

    time_start = process_time()
    for part in parts:
        print(f'Processing part {part}')
        if part == '1':
            start = "you"
            end = "out"
            num_paths = count_paths(graph, start, end)
            print(f'there were {num_paths} routes from "{start}" to "{end}"')
        if part == '2':
            start = "you"
            end = "out"
            waypoints = ("fft", "dac")
            num_paths = count_paths_waypoints(graph, start, end, waypoints)
            print(f'there were {num_paths} routes from "{start}" to "{end}"')
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