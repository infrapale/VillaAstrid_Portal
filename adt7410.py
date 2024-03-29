# SPDX-FileCopyrightText: 2019 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_adt7410`
====================================================
CircuitPython driver for reading temperature from the Analog Devices ADT7410
precision temperature sensor
* Author(s): ladyada
Implementation Notes
--------------------
**Hardware:**
* `Adafruit's ADT7410 analog temperature Sensor Breakout:
  <https://www.adafruit.com/product/4089>`_ (Product ID: 4089)
**Software and Dependencies:**
* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases
* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
* Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""


import time
import struct
from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_register.i2c_bit import RWBit, ROBit
from micropython import const

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_ADT7410.git"


_ADT7410_TEMPMSB = const(0x0)
_ADT7410_TEMPLSB = const(0x1)
_ADT7410_STATUS = const(0x2)
_ADT7410_CONFIG = const(0x3)
_ADT7410_ID = const(0xB)
_ADT7410_SWRST = const(0x2F)


class ADT7410:
    """Interface to the Analog Devices ADT7410 temperature sensor.
    :param ~busio.I2C i2c_bus: The I2C bus the ADT7410 is connected to.
    :param int address: The I2C device address. Default is :const:`0x48`
    **Quickstart: Importing and using the ADT7410 temperature sensor**
        Here is an example of using the :class:`ADT7410` class.
        First you will need to import the libraries to use the sensor
        .. code-block:: python
            import board
            import adafruit_adt7410
        Once this is done you can define your `board.I2C` object and define your sensor object
        .. code-block:: python
            i2c = board.I2C()  # uses board.SCL and board.SDA
            adt = adafruit_adt7410.ADT7410(i2c_bus, address=0x48)
        Now you have access to the temperature using :attr:`temperature`.
        .. code-block:: python
            temperature = adt.temperature
    """

    # many modes can be set with register objects for simplicity
    ready = ROBit(_ADT7410_STATUS, 7)
    ctpin_polarity = RWBit(_ADT7410_CONFIG, 2)
    intpin_polarity = RWBit(_ADT7410_CONFIG, 3)
    comparator_mode = RWBit(_ADT7410_CONFIG, 4)
    high_resolution = RWBit(_ADT7410_CONFIG, 7)

    def __init__(self, i2c_bus, address=0x48):
        self.i2c_device = I2CDevice(i2c_bus, address)
        self._buf = bytearray(3)
        # Verify the manufacturer and device ids to ensure we are talking to
        # what we expect.
        _id = (self._read_register(_ADT7410_ID)[0]) & 0xF8
        if _id != 0xC8:
            raise ValueError(
                "Unable to find ADT7410 at i2c address " + str(hex(address))
            )
        self.reset()

    @property
    def temperature(self):
        """The temperature in Celsius"""
        temp = self._read_register(_ADT7410_TEMPMSB, 2)
        return struct.unpack(">h", temp)[0] / 128

    @property
    def status(self):
        """The ADT7410 status registers current value"""
        return self._read_register(_ADT7410_STATUS)[0]

    @property
    def configuration(self):
        """The ADT7410 configuration register"""
        return self._read_register(_ADT7410_CONFIG)[0]

    @configuration.setter
    def configuration(self, val):
        return self._write_register(_ADT7410_CONFIG, val)

    def reset(self):
        """Perform a software reset"""
        self._write_register(_ADT7410_SWRST)
        time.sleep(0.5)

    def _read_register(self, addr, num=1):
        self._buf[0] = addr
        with self.i2c_device as i2c:
            i2c.write_then_readinto(
                self._buf, self._buf, out_end=1, in_start=1, in_end=num + 1
            )
        return self._buf[1 : num + 1]

    def _write_register(self, addr, data=None):
        self._buf[0] = addr
        end = 1
        if data:
            self._buf[1] = data
            end = 2
        with self.i2c_device as i2c:
            i2c.write(self._buf, end=end)