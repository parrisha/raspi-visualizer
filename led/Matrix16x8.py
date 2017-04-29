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

class Matrix16x8(HT16K33.HT16K33):
    """Single color 8x16 matrix LED backpack display."""

    #Initialize display.  All arguments will be passed to the HT16K33 class
    # initializer, including optional I2C address and bus number parameters.
    def __init__(self, **kwargs):
        super(Matrix16x8, self).__init__(**kwargs)

    #Set pixel at position x, y to the given value (0 for off, 1 for on)
    def set_pixel(self, x, y, value):
        if x < 0 or x > 15 or y < 0 or y > 7:
            # Ignore out of bounds pixels.
            return
        
        #Remap the rows and columns when passing into HT16K33
        #to make the Bottom-Left corner of LED Array be (0, 0) and increase up and right
        #    See LED_mapping.xlsx
        led = ((15 - x) * 8 + (7 - y) - 64) % 128
        self.set_led(led, value)

    # JParrish 4/29/2017
    # Write an entire register in the HT16K33, which would normally light up a row
    #  But with the LED Arrays wired "backwards" (column drivers connected to LED row pins)
    #  Setting a row register is equivalent to lighting up a column
    def set_column(self, x, height):
        #Remap the column ID when passing into HT16K33 to make leftmost column 0 and increase to the right
        #We also want to light "up" from the end of the column, so generate Height number of 1's and then invert
        value = 256 - (2 ** (8 - height))
        self.set_row_reg((7 - x) % 16, value)
