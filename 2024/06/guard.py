#!/usr/bin/python3

# guard
'''Advent of code day 06 - guard paths'''


from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError
from time import process_time

app_name = 'guard.py'

class Lab:
    def __init__(self, place_obstacles):
        self.map = []
        self.visit_detail = {}
        self.step = {'v': (1, 0), '<': (0, -1), '^': (-1, 0), '>': (0, 1)}
        self.step_backward = {'v': (-1, 0), '<': (0, 1), '^': (1,0), '>': (0, -1)}
        self.turn = {'v': '<', '<': '^', '^': '>', '>': 'v'}
        self.block = '#'
        self.visited = 'X'
        self.num_rows = 0
        self.num_cols = 0
        self.obstacles_placed = []
        self.possible_obstacle_locations = []
        self.place_obstacles = place_obstacles
        self.uturn_locations = []
        self.verbose = False
        return
    
    def set_map(self, map):
        self.visit_detail = {}
        self.map = []
        self.num_rows = len(map)
        if self.num_rows:
            self.num_cols = len(map[0])
            for row in map:
                self.map.append([*row])

    def print_map(self):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if (row, col) in self.obstacles_placed:
                    print ('O', end='')
                else:
                    print(self.map[row][col], end='')
            print()
        print()

    def print_map_near_position(self, position):
        size = 3
        for row in range(position[0]-size, position[0]+size+1):
            if row >= 0 and row < self.num_rows:
                for col in range(position[1]-size, position[1]+size+1):
                    if col >= 0 and col < self.num_cols:
                        print(self.map[row][col], end='')
                print()
        print()
    
    def guard_position(self):
        for row in range(len(self.map[0])):
            if row >= 0:
                for col in range(len(self.map[row])):
                    cell = self.map[row][col]
                    if cell in self.turn:
                        position = (row, col)
                        return position
        return ()
    
    def count_visited_positions(self):
        count = 0
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if self.map[row][col] == self.visited:
                    count += 1
        return count
    
    def is_valid_position(self, position):
        row = position[0]
        col = position[1]
        if row < 0 or row >= self.num_rows:
            return False
        if col < 0 or col >= self.num_cols:
            return False
        return True
    
    def look_behind_for_obstacle_candidates(self, position, guard):
        previous_guard = list(self.turn.keys())[list(self.turn.values()).index(guard)]
        while True:
            look_position = self.next_position(position, previous_guard)
            if not self.is_valid_position(position):
                break
            row_look = look_position[0]
            col_look = look_position[1]
            looked_at = self.map[row_look][col_look]
            if looked_at  == self.block or looked_at == self.visited:
                pass
            self.possible_obstacle_locations.append((look_position, previous_guard))
            position = self.next_position(position, guard, self.step_backward)
        pass

    def next_position(self, position, guard, step=[]):
        if not step:
            step = self.step
        direction = step[guard]
        return (position[0]+direction[0], position[1]+direction[1])
    
    def mark_visited(self, position, guard):
        key = tuple(position)
        self.map[position[0]][position[1]] = self.visited
        if key in self.visit_detail:
            guards = self.visit_detail[key]
            if guard in guards:
                return True
            else:
                guards.append(guard)
        else:
            self.visit_detail[key] = [guard]
        return False

    def move_guard(self, position, check_for_loops = False):
        if self.verbose:
            self.print_map_near_position(position)
        row, col = position
        guard = self.map[row][col]
        if guard in self.turn:
            repeat = self.mark_visited(position, guard)
            if check_for_loops and repeat:
                return True

            next_position = self.next_position(position, guard)
            next_row, next_col = next_position

            if not self.is_valid_position(next_position):
                return False

            if self.map[next_row][next_col] == self.block:
                new_guard = self.turn[guard]
                self.map[row][col] = new_guard
                if self.place_obstacles:
                    self.look_behind_for_obstacle_candidates(position, guard)
                after_turn = self.next_position(position, new_guard)
                if not check_for_loops:
                    if self.map[after_turn[0]][after_turn[1]] != self.block:
                        self.uturn_locations.append(after_turn)
            else:
                if self.place_obstacles:
                    if (next_position, guard) in self.possible_obstacle_locations:
                        self.obstacles_placed.append(next_position)
                self.map[next_row][next_col] = guard
        return False

    def is_uturn_loop(self):
        guard_position = self.guard_position()
        while guard_position:
            if self.move_guard(guard_position, check_for_loops=True):
                return True
            guard_position = self.guard_position()
        return False
    
    def count_uturn_loops(self, map):
        uturn_loops_count = 0
        test_for_loops = Lab(place_obstacles=False)
        test_for_loops.verbose = self.verbose
        for position in self.uturn_locations:
            test_for_loops.set_map(map)
            test_for_loops.map[position[0]][position[1]] = test_for_loops.block
            if test_for_loops.is_uturn_loop():
                uturn_loops_count += 1
                print('+', end='')
            else:
                print('.', end='')
        print()
        return uturn_loops_count
    

def main(arguments):
    program_name = app_name
    command_line_documentation = f'{program_name} --help --verbose --section [a|b] --file [input file]'
    input_file_name = ''
    sections = []
    verbose = False

    try:
        opts, args = getopt(arguments, "hvs:f:", ("help", "verbose", "section=", "file="))
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

        if opt in ('-v', '--verbose'):
            verbose = True

    place_obstacles = 'b' in section
    lab = Lab(place_obstacles)
    lab.verbose = verbose

    if input_file_name:
        with open(input_file_name, 'r') as input_file:
            map = []
            print(f'Opened {input_file_name} for {app_name}')
            for line in input_file:
                map.append(line.strip())
        lab.set_map(map)
        if lab.verbose:
            lab.print_map()

    time_start = process_time()
    guard_position = lab.guard_position()
    lab.look_behind_for_obstacle_candidates(guard_position, lab.map[guard_position[0]][guard_position[1]])
    go_again = True
    while go_again:
        guard_position = lab.guard_position()
        if not guard_position:
            go_again = False
        else:
            lab.move_guard(guard_position)
    time_end = process_time()
    if lab.verbose:
        lab.print_map()
    if 'a' in sections:
        print(f'The guard visited {lab.count_visited_positions()} positions')
    if 'b' in sections:
        if lab.verbose:
            print(f'The look behind method found {len(lab.obstacles_placed)} locations to create loops')
            print(f'There are {len(lab.uturn_locations)} positions to check for u-turns')
        uturn_loops = lab.count_uturn_loops(map)    
        print(f'We found {len(lab.obstacles_placed)+uturn_loops} total locations to create loops')
    print(f'Time taken: {time_end - time_start} seconds.')

    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input(f'enter command line for {app_name}: ')
        argv.extend(command_line.split())
    main(argv[1:])