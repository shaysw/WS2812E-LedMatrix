GAME_OF_LIFE_FOLDER = 'GameOfLife'
WAIT_MS = 10
ITERATION_INTERVAL_MS = 100

import os

os.chdir(GAME_OF_LIFE_FOLDER)

import time
from Grid import Grid
from PicoNeoPixelDriver import *


class LedGrid(Grid):
    def __init__(self):
        super().__init__()

    def show(self):
        for row_index in range(len(self.grid)):
            for col_index in range(len(self.grid[row_index])):
                strip_cell = self.convert_array_cell_to_strip_cell(row_index, col_index)
                is_alive = self.grid[row_index][col_index]

                pixels_set(strip_cell, (0, 255, 0) if is_alive else (0, 0, 0))

        pixels_show()

    @staticmethod
    def convert_array_cell_to_strip_cell(row_index, col_index):
        if row_index % 2 == 0:
            return row_index * 16 + 15 - col_index
        else:
            return row_index * 16 + col_index


def start_game():
    old_grid = LedGrid()
    old_grid.initialize()

    old_grid.show()

    while True:
        new_grid = LedGrid()
        new_grid.grid = old_grid.iterate_grid()
        time.sleep(ITERATION_INTERVAL_MS / 1000)

        if old_grid.grid == new_grid.grid:
            print('game finished')
            break

        new_grid.show()
        old_grid = new_grid


def reset_game():
    colorWipe((0, 0, 0))
    start_game()


if __name__ == '__main__':
    try:
        while True:
            start_game()

    finally:
        colorWipe((0, 0, 0))
