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
_RFM69_I2C_ADDRESS    = const(0x20)
_I2C_BUF_LEN          = const(16)
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
