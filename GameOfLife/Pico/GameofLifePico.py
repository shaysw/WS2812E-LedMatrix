#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

from GameOfLife.Pico.Grid import Grid
from .PicoNeoPixelDriver import *

WAIT_MS = 10
ITERATION_INTERVAL_MS = 100

# Main program logic follows:
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

# def pause_game():
#     button.wait_for_press()


def start_game():
    time.sleep(0.5)

    old_grid = LedGrid()
    old_grid.initialize()

    old_grid.show()

    # button.when_pressed = pause_game
    # button.when_held = reset_game

    while True:
        # if button.is_pressed:
        #     time.sleep(0.5)
        #     button.wait_for_press()
        #
        # if button.is_held:
        #     reset_game()
        #     break

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
    game_started = False

    # Process arguments
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    # args = parser.parse_args()
    #
    # # Create NeoPixel object with appropriate configuration.
    # strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # # Intialize the library (must be called once before other functions).
    # strip.begin()

    # print('Press Ctrl-C to quit.')
    # if not args.clear:
    #     print('Use "-c" argument to clear LEDs on exit')

    # button = Button(2, hold_time=2)
    #
    try:
        while True:
            # button.wait_for_press()
            start_game()
        
    finally:
        colorWipe((0, 0, 0))
