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


def count_paths(graph, start, end, verbose=False):
    queue = deque()
    num_paths = {}
    queue.append(start)
    num_paths[start] = 1
    while queue:
        this_node = queue.popleft()
        if this_node in queue:
            if verbose:
                print(f'{this_node} has already been visited {num_paths[this_node]} times')
        elif this_node == end:
            if verbose:
                print(f'the number of paths from {start} to {end} is now {num_paths[end]}')
        else:
            if this_node in graph:
                destinations = graph[this_node]
                for destination in destinations:
                    queue.append(destination)
                    add_destination_score(num_paths, destination, num_paths[this_node])
    return num_paths[end]


def add_index(true_index, waypoint_list):
    new_list = []
    for index in range(len(waypoint_list)):
        new_list.append(index == true_index or waypoint_list[index])
    return tuple(new_list)


def count_paths_waypoints(graph, start, end, waypoints, verbose):
    queue = deque()
    num_paths = 0
    previous_nodes = tuple()
    if verbose:
        last_printed_length = 0
    queue.append((start, previous_nodes))
    while queue:
        this_node = queue.popleft()
        node_value = this_node[0]
        previous_nodes = this_node[1]
        if verbose:
            if len(previous_nodes) > last_printed_length:
                last_printed_length = len(previous_nodes)
                print(f'The queue is {len(queue)} nodes long', end='')
                print(f'. This node has a history {len(previous_nodes)} nodes long')
        if node_value == end:
            if all([waypoint in previous_nodes
                    for waypoint in waypoints]):
                num_paths += 1
                if verbose:
                    print(f'the number of paths is up to {num_paths}, ', end='')
            if verbose:
                print(f'the queue is {len(queue)} nodes long')
        else:
            if node_value in previous_nodes:
                if verbose:
                    print(f'found a loop {previous_nodes}: {node_value}')
            else:
                new_nodes = list(previous_nodes)
                new_nodes.append(node_value)
                previous_nodes = tuple(new_nodes)
                destinations = graph[node_value]
                for destination in destinations:
                    queue.append((destination, previous_nodes))
    return num_paths


def sorted_destinations(destinations):
    return sorted(destinations)


def flatten_graph(graph):
    flattened_graph = []
    for item in graph.items():
        key = item[0]
        destinations = tuple(sorted_destinations(item[1]))
        flattened_graph.append((key, destinations))
    return flattened_graph


def simplify_graph(graph, additional_node, verbose):
    if verbose:
        all_destinations = graph.values()
        num_edges = sum([len(destinations) for destinations in all_destinations])
        print(f'the input graph has {len(graph)} nodes and {num_edges} edges')

    reserved_nodes = ['you', 'out', 'svr', 'fft', 'dac']
    if additional_node and not additional_node in reserved_nodes:
        reserved_nodes.append(additional_node)

    new_graph = {}
    for entry in flatten_graph(graph):
        new_graph[entry[0]] = entry[1]

    
    return new_graph


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
            graph = simplify_graph(parse_graph(input_file), override_begin, verbose)

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