
import time
from Grid import Grid
from PicoNeoPixelDriver import *

WAIT_MS = 0
ITERATION_INTERVAL_MS = 0
BUTTON_PIN_NUMBER = 14
OPERATE_WITH_BUTTON = True

button = Pin(BUTTON_PIN_NUMBER, Pin.IN, Pin.PULL_DOWN)

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

    print('initializing grid')
    old_grid.show()
    
    while True:
        if OPERATE_WITH_BUTTON and button.value():
            print('stopping')
            break

        new_grid = LedGrid()
        new_grid.grid = old_grid.iterate_grid()

        if old_grid.grid == new_grid.grid:
            print('game finished')
            break

        new_grid.show()
        old_grid = new_grid


def run():
    try:        
        while True:
            if OPERATE_WITH_BUTTON:
                while True:
                    if button.value():
                        time.sleep(0.2)
                        break

                print('starting')
                start_game()
                colorWipe((0, 0, 0))
                time.sleep(0.2)

    finally:
        colorWipe((0, 0, 0))

if __name__ == '__main__':
    run()
    