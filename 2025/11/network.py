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


def add_destination_score(scores, destination, incoming_score):
    if destination in scores:
        scores[destination] += incoming_score
    else:
        scores[destination] = incoming_score
    pass


def walk_paths(graph, start, end, verbose=False):
    queue = deque()
    num_paths = {}
    queue.append(start)
    num_paths[start] = 1
    visited = set()
    while queue:
        this_node = queue.popleft()
        if this_node in visited:
            if verbose:
                print(f'{this_node} has already been visited {num_paths[this_node]} times')
        else:
            visited.add(this_node)
            if this_node == end:
                if verbose:
                    print(f'the number of paths from {start} to {end} is now {num_paths[end]}')
            else:
                if this_node in graph:
                    destinations = graph[this_node]
                    for destination in destinations:
                        if destination in num_paths:
                            num_paths[destination] += num_paths[this_node]
                        else:
                            queue.append(destination)
                            num_paths[destination] = num_paths[this_node]
    if end in num_paths:
        count_paths = num_paths[end]
    else:
        count_paths = 0
    return (count_paths, visited)
    

def count_paths(graph, start, end, verbose=False):
    return walk_paths(graph, start, end, verbose)[0]


def count_paths_waypoints(graph, start, end, waypoints, verbose):
    num_paths = 1
    full_path = [start] + list(waypoints) + [end]
    segments = [(full_path[i], full_path[i+1]) for i in range(len(full_path)-1)]
    for segment in segments:
        num_paths_segment = count_paths(graph, segment[0], segment[1], verbose and False)
        if verbose:
            print(f'{num_paths_segment} paths from {segment[0]} to {segment[1]}')
        num_paths *= num_paths_segment
    return num_paths


def main(arguments):
    program_name = app_name
    command_line_documentation = f'{program_name} --help --verbose --part [1|2] --begin [begin] --end [end]  --file [input file]'
    verbose = False
    input_file_name = ''
    parts = []
    override_begin = ''
    override_end = ''

    try:
        opts, args = getopt(arguments, "hvp:b:e:f:", ("help", "verbose", "part=", "begin=", "end=", "file="))
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

        if opt in ('-b', '--begin'):
            override_begin = arg

        if opt in ('-e', '--end'):
            override_end = arg

    if input_file_name:
        with open(input_file_name, 'r') as input_file:
            if verbose:
                print(f'Opened {input_file_name} for {app_name}')
            graph = parse_graph(input_file)

    time_start = process_time()
    for part in parts:
        print(f'Processing part {part}')
        if part == '1':
            if override_begin:
                start = override_begin
            else:
                start = "you"
            if override_end:
                end = override_end
            else:
                end = "out"
            num_paths = count_paths(graph, start, end, verbose)
            print(f'there were {num_paths} routes from "{start}" to "{end}"')
        if part == '2':
            if override_begin:
                start = override_begin
            else:
                start = "svr"
            if override_end:
                end = override_end
            else:
                end = "out"
            waypoints = ("fft", "dac")
            num_paths = count_paths_waypoints(graph, start, end, waypoints, verbose)
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