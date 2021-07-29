# The MIT License (MIT)
#
# Copyright (c) 2017 Tom Höglund infrapale@gmail.com
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
"""
`keypad_i2c`
====================================================

CircuitPython module for the I2C 5x5 keypad



* Author(s): Tom Hoglund
Implementation Notes
--------------------
**Hardware:**
* I2C keyboard Retro Keyboard 2020
  Arduino Pro Mini

**Software and Dependencies:**
  <https://github.com/infrapale/RetroKeyPad_I2C_Slave>

  reference code:
  https://github.com/adafruit/Adafruit_CircuitPython_TLV493D/blob/master/adafruit_tlv493d.py
  https://github.com/adafruit/Adafruit_CircuitPython_PCF8591/blob/master/adafruit_pcf8591/pcf8591.py

"""

import board

#import adafruit_bus_device.i2c_device as i2cdevice
from adafruit_bus_device.i2c_device import I2CDevice
from micropython import const
__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/infrapale/PyPortal_VA_Control"


_KEYPAD_I2C_DEFAULT_ADDRESS = const(0x18)


class keypad_i2c:
    """
    Driver for the I2C 5x5 kkeypad 2020.
    :param busio.I2C i2c_bus: The I2C bus the keypad is connected to.
    :param int address: The I2C address of the keypad. Defaults to 0x18.
    """
    def __init__(self, i2c_bus, address=_KEYPAD_I2C_DEFAULT_ADDRESS, addr_reg=0):
        self.i2c_device = I2CDevice(i2c_bus, address)
        self.read_buffer = bytearray(2)
        self.write_buffer = bytearray(4)


    def _read_key_dur(self):
        self.read_buffer[0] = 2
        self.read_buffer[1] = 0
        with self.i2c_device as i2c:
            i2c.write_then_readinto(self.read_buffer, self.read_buffer)

    def _read_i2c(self):
        with self.i2c_device as i2c:
            i2c.readinto(self.read_buffer)
    def _write_i2c(self):
        with self.i2c_device as i2c:
            i2c.write(self.write_buffer)




    @property
    def key_pressed(self):
        self._read_key_dur()
        return ((self.read_buffer[0],self.read_buffer[1]))

