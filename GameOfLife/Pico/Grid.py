from random import random

HEIGHT = 16
WIDTH = 16
THRESHOLD = 0.33


class Grid:
    def __str__(self):
        number_of_live_neighbours = ''

        for row in range(len(self.grid)):
            number_of_live_neighbours += ' '.join(
                '1' if self.grid[row][col] else '0' for col in range(len(self.grid[row])))
            number_of_live_neighbours += '\n'

        return number_of_live_neighbours

    def __init__(self,
                 height=HEIGHT,
                 width=WIDTH,
                 threshold=THRESHOLD,
                 live_slot_min_live_neighbours_to_keep_alive=2,
                 live_slot_max_live_neighbours_to_keep_alive=3,
                 dead_slot_min_live_neighbours_to_bring_to_life=3,
                 dead_slot_max_live_neighbours_to_bring_to_life=3):
        self.threshold = threshold
        self.height = height
        self.width = width
        self.live_slot_min_live_neighbours_to_keep_alive = live_slot_min_live_neighbours_to_keep_alive
        self.live_slot_max_live_neighbours_to_keep_alive = live_slot_max_live_neighbours_to_keep_alive
        self.dead_slot_min_live_neighbours_to_bring_to_life = dead_slot_min_live_neighbours_to_bring_to_life
        self.dead_slot_max_live_neighbours_to_bring_to_life = dead_slot_max_live_neighbours_to_bring_to_life

        self.grid = []
        for _ in range(self.height):
            self.grid.append([False] * self.width)

    def initialize(self):
        for row in range(self.height):
            self.grid[row] = [random() < self.threshold for _ in range(self.width)]

            # self.grid.append([random() < self.threshold for _ in range(self.width)])

    def get_neighbour(self, row, col):
        try:
            neighbour_value = self.grid[row][col]
        except:
            neighbour_value = False

        return neighbour_value

    def get_number_of_live_neighbours(self, row, col):
        number_of_live_neighbours = 0

        if self.get_neighbour(row - 1, col - 1):
            number_of_live_neighbours += 1

        if self.get_neighbour(row - 1, col):
            number_of_live_neighbours += 1

        if self.get_neighbour(row - 1, col + 1):
            number_of_live_neighbours += 1

        if self.get_neighbour(row, col - 1):
            number_of_live_neighbours += 1

        if self.get_neighbour(row, col + 1):
            number_of_live_neighbours += 1

        if self.get_neighbour(row + 1, col - 1):
            number_of_live_neighbours += 1

        if self.get_neighbour(row + 1, col):
            number_of_live_neighbours += 1

        if self.get_neighbour(row + 1, col + 1):
            number_of_live_neighbours += 1

        return number_of_live_neighbours

    def iterate_cell(self, row, col):
        live_neighbours = self.get_number_of_live_neighbours(row, col)
        is_cell_alive = self.grid[row][col]

        if is_cell_alive:
            if self.live_slot_min_live_neighbours_to_keep_alive <= live_neighbours <= self.live_slot_max_live_neighbours_to_keep_alive:
                return True

            return False

        if self.dead_slot_min_live_neighbours_to_bring_to_life <= live_neighbours <= self.dead_slot_max_live_neighbours_to_bring_to_life:
            return True
        return False

    def iterate_grid(self):
        new_grid = []

        for _ in range(self.height):
            new_grid.append([False] * self.width)

        for row in range(self.height):
            for col in range(self.width):
                new_grid[row][col] = self.iterate_cell(row, col)

        return new_grid