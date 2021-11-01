#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import itertools
import time
from rpi_ws281x import PixelStrip, Color
import argparse
from gpiozero import LED, Button
import RPi.GPIO as GPIO

# LED strip configuration:
from GameOfLifePython.Grid import Grid

LED_COUNT = 256  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 5  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53
WAIT_MS = 10
ITERATION_INTERVAL_MS = 100
OPERATE_WITH_BUTTON = False

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=WAIT_MS):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()
    # time.sleep(wait_ms / 1000.0)


def theaterChase(strip, color, wait_ms=WAIT_MS, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)


def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


def rainbow_cells(strip, cells, wait_ms=WAIT_MS, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    a = list(map(lambda cell: LedGrid.convert_array_cell_to_strip_cell(cell[0], cell[1]), cells))
    for j in range(256 * iterations):
        for i in a:
            strip.setPixelColor(i, wheel((i + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def rainbow(strip, wait_ms=WAIT_MS, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def rainbowCycle(strip, wait_ms=WAIT_MS, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel(
                (int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def theaterChaseRainbow(strip, wait_ms=WAIT_MS):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, wheel((i + j) % 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)


# Main program logic follows:
class LedGrid(Grid):
    def __init__(self, strip):
        super().__init__()
        self.strip = strip

    def show(self):
        for row_index in range(len(self.grid)):
            for col_index in range(len(self.grid[row_index])):
                strip_cell = self.convert_array_cell_to_strip_cell(row_index, col_index)
                is_alive = self.grid[row_index][col_index]

                self.strip.setPixelColor(strip_cell, Color(0, 255, 0) if is_alive else Color(0, 0, 0))

        self.strip.show()

    @staticmethod
    def convert_array_cell_to_strip_cell(row_index, col_index):
        if row_index % 2 == 0:
            return row_index * 16 + 15 - col_index
        else:
            return row_index * 16 + col_index

def start_game():
    time.sleep(0.5)

    old_grid = LedGrid(strip)
    old_grid.initialize()

    old_grid.show()

    while True:
        if OPERATE_WITH_BUTTON:
            if button.is_pressed:
                time.sleep(0.5)
                button.wait_for_press()
            
            if button.is_held:
                reset_game()
                break

        new_grid = LedGrid(strip)
        new_grid.grid = old_grid.iterate_grid()
        time.sleep(ITERATION_INTERVAL_MS / 1000)

        if old_grid.grid == new_grid.grid:
            print('game finished')
            break

        new_grid.show()

        old_grid = new_grid


def reset_game():
    colorWipe(strip, Color(0, 0, 0), 10)
    start_game()


if __name__ == '__main__':
    game_started = False

    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    if (OPERATE_WITH_BUTTON):
        button = Button(2, hold_time=2)
    
    try:
        while True:
            if (OPERATE_WITH_BUTTON):
                button.wait_for_press()
            start_game()
        
    finally:
        colorWipe(strip, Color(0, 0, 0), 10)
