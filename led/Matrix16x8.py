# Copyright (c) 2017 Adafruit Industries
# Author: Carter Nelson
# Modified from Matrix8x16 by Joe Parrish
# (https://github.com/adafruit/Adafruit_Python_LED_Backpack/blob/master/Adafruit_LED_Backpack/Matrix8x16.py)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
from . import HT16K33

class Matrix16X8(HT16K33.HT16K33):
    """Single color 8x16 matrix LED backpack display."""

    def __init__(self, **kwargs):
        """Initialize display.  All arguments will be passed to the HT16K33 class
        initializer, including optional I2C address and bus number parameters.
        """
        super(Matrix16x8, self).__init__(**kwargs)

    def set_pixel(self, x, y, value):
        """Set pixel at position x, y to the given value.  X and Y should be values
        of 0 to 7 and 0 to 15, resp.  Value should be 0 for off and non-zero for on.
        """
        if x < 0 or x > 15 or y < 0 or y > 7:
            # Ignore out of bounds pixels.
            return
        """ Remap the LEDS to make the Bottom-Left corner be (0, 0) and move up and right
            See LED_mapping.xlsx
        """
        led = ((15 - x) * 8 + (7 - y) - 64) % 128
        self.set_led(led, value)

    def set_column(self, x, value):
        """Since the HT16K33 is internally organized as one register per 8 LEDs
        provide a method to quickly set an entire register.
        Will set a column to have $value number of lit LEDs
        """
        self.set_register(self, x, value)
