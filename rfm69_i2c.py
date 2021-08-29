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
import time
import struct
from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_register.i2c_bit import RWBit, ROBit


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
_RFM69_GET_ID         = const(0x05)
_RFM69_SEND_MSG       = const(0x10)
_RFM69_TX_DATA        = const(0x11)
_RFM69_RX_AVAIL       = const(0x40)
_RFM69_RX_LOAD_MSG    = const(0x41)
_RFM69_RX_RD_MSG1     = const(0x42)
_RFM69_RX_RD_MSG2     = const(0x43)
_RFM69_RX_RD_LEN      = const(0x44)
_RFM69_TX_FREE        = const(0x50)

_RFM69_ID             = const(0x42)
_RFM69_HALF_MSG_LEN   = const(32)
  
_ADT7410_TEMPMSB = const(0x0)
_ADT7410_TEMPLSB = const(0x1)
_ADT7410_STATUS = const(0x2)
_ADT7410_CONFIG = const(0x3)
_ADT7410_ID = const(0xB)
_ADT7410_SWRST = const(0x2F)
 
 
# User-facing constants:

class RFM69_I2C:
    # Class-level buffer to reduce memory usage and allocations.
    # Note this is NOT thread-safe or re-entrant by design.
    _BUFFER     = bytearray(_I2C_BUF_LEN)
    _RFM69_BUFF = bytearray(_RFM69_BUF_LEN )

    def __init__(self, i2c, address=_RFM69_I2C_ADDRESS):
        self.i2c_device = I2CDevice(i2c, address)
        self._buf = bytearray(_I2C_BUF_LEN )
        print('RFM69_I2C:__init__')
         # Verify the manufacturer and device ids to ensure we are talking to
        # what we expect.
        _id = (self._read_register(_RFM69_GET_ID )[0]) 
        print('ID=',_id)
        if _id != _RFM69_ID:
            raise ValueError("Unable to find RFM69_I2C at i2c address " + str(hex(address)))
        
        # Put the device in a powered on state after initialization.
        self.reset()
        print('RFM69 Initialized')
 
    def reset(self):
        """Perform a software reset"""
        try:
            self._write_register(_ADT7410_SWRST)
        except:
            pass
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


    def test_i2c_read(self):
        t1 = self._read_register(0x02)
        print('test_i2c_read',t1)

    @property
    def rfm69_data_avail(self):
        """Get number of available messages"""
        try:
            return self._read_register(_RFM69_RX_AVAIL)[0]
        except:
            return 0
    def rfm69_load_msg(self):
        """Get number of available messages"""
        try:
            return self._read_register(_RFM69_RX_LOAD_MSG)[0]
        except:
            return 0
    
    def rfm69_get_data(self, sub_indx):
        """ Get part of the message """      
        try:
            if sub_indx == 1:
                return self._read_register(_RFM69_RX_RD_MSG1,_RFM69_HALF_MSG_LEN )
            else:   # if sub_indx = 2:
                return self._read_register(_RFM69_RX_RD_MSG2,_RFM69_HALF_MSG_LEN )
        except:
            return 0
        
        
         
    def reset(self):
        """Perform a software reset"""
        self._write_register(_RFM69_RESET)
        time.sleep(0.5)

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


    