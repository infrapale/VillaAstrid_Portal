# SPDX-FileCopyrightText: 2021 Tom Hoglund
#
# SPDX-License-Identifier: MIT

"""
`rfm69_i2c`
====================================================
CircuitPython module for the I2C based RFM69 radio module.  See
examples/simpletest.py for a demo of the usage.
* Author(s): Tom Hoglund
Implementation Notes
--------------------
**Hardware:**
*
**Software and Dependencies:**
* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads
 * Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
 * Reference code: https://github.com/adafruit/Adafruit_CircuitPython_TSL2591/blob/main/adafruit_tsl2591.py
"""
from micropython import const

import adafruit_bus_device.i2c_device as i2c_device

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/infrapale/VillaAstrid_Portal"

# Internal constants:
#_RFM69_I2C_ADDRESS    = const(0x20)
_RFM69_I2C_ADDRESS    = const(0x48)
_I2C_BUF_LEN          = const(32+2)
_RFM69_BUF_LEN        = const(_I2C_BUF_LEN *2)
_RFM69_RESET          = const(0x01)
_RFM69_CLR_RX         = const(0x02)
_RFM69_CLR_TX         = const(0x03)
_RFM69_SEND_MSG       = const(0x10)
_RFM69_TX_DATA        = const(0x11)
_RFM69_RX_AVAIL       = const(0x40)
_RFM69_RX_LOAD_MSG    = const(0x41)
_RFM69_RX_RD_MSG1     = const(0x42)
_RFM69_RX_RD_MSG2     = const(0x43)
_RFM69_RX_RD_LEN      = const(0x44)
_RFM69_TX_FREE        = const(0x50)
_TSL2591_REGISTER_DEVICE_ID = const(0x12)

# User-facing constants:

class RFM69_I2C:
    # Class-level buffer to reduce memory usage and allocations.
    # Note this is NOT thread-safe or re-entrant by design.
    _BUFFER     = bytearray(_I2C_BUF_LEN)
    _RFM69_BUFF = bytearray(_RFM69_BUF_LEN )

    def __init__(self, i2c, address=_RFM69_I2C_ADDRESS):
        self._device = i2c_device.I2CDevice(i2c, address)
        print('RFM69_I2C:__init__')
        # Verify the chip ID.
        if self._read_u8(_TSL2591_REGISTER_DEVICE_ID) != 0x50:
            raise RuntimeError("Failed to find TSL2591, check wiring!")
        
        # Put the device in a powered on state after initialization.
        self.enable()

    def _read_u8(self, address):
        # Read an 8-bit unsigned value from the specified 8-bit address.
        print('_read_u8')
        with self._device as i2c:
            # Make sure to add command bit to read request.
            self._BUFFER[0] = (address) & 0xFF
            print('BUFFER', self._BUFFER)
            i2c.write_then_readinto(self._BUFFER, self._BUFFER, out_end=1, in_end=1)
            print('BUFFER', self._BUFFER)
        print('in i2c')
        return self._BUFFER[0]
        # return 69

    # Disable invalid name check since pylint isn't smart enough to know LE
    # is an abbreviation for little-endian.
    # pylint: disable=invalid-name
    def _read_u16LE(self, address):
        # Read a 16-bit little-endian unsigned value from the specified 8-bit
        # address.
        with self._device as i2c:
            # Make sure to add command bit to read request.
            self._BUFFER[0] = ( address) & 0xFF
            i2c.write_then_readinto(self._BUFFER, self._BUFFER, out_end=1, in_end=2)
        return (self._BUFFER[1] << 8) | self._BUFFER[0]

    # pylint: enable=invalid-name

    def _write_u8(self, address, val):
        # Write an 8-bit unsigned value to the specified 8-bit address.
        with self._device as i2c:
            # Make sure to add command bit to write request.
            self._BUFFER[0] = (address) & 0xFF
            self._BUFFER[1] = val & 0xFF
            i2c.write(self._BUFFER, end=2)

    def test_i2c_read(self):
        t1 = self._read_u8(0x02)
        print(t1)

    def rfm69_data_avail(self):
        rx_avail = 99
        print('rfm69_data_avail(self)')
        rx_avail =self._read_u8(_RFM69_RX_AVAIL)
        print('Rx Available = ',rx_avail)
        print('Failed when bus.read_byte_data')
        return rx_avail


    def read_rfm69_msg(self,rd_buff):
        do_continue = False
        rd_len = 0
        if self.rfm69_data_avail(self) > 0:
            try:
                rd_len = self._read_u8(RFM69_RX_LOAD_MSG)
                print('rd_len=',rd_len)
            except:
                do_continue = False
                print('LOAD_MSG Error')
        else:
            do_continue = False


    def enable(self):
        """Put the device in a fully powered enabled mode."""
        # self._write_u8(0,0)
        pass

    def disable(self):
        """Disable the device and go into low power mode."""
        # self._write_u8(1)
        pass
