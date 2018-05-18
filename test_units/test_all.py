#!/usr/bin/python

"""
Unit test for zephyr
"""
__author__ = 'Kirk Clendinning'
__date__ = '2018-04-02'
__copyright__ = 'Copyright 2018, Ocean Optics'
__credits__ = ['Kirk Clendinning']
__license__ = 'GPL'
__version__ = '1.0.0'
__maintainer__ = 'Kirk Clendinning'
__email__ = 'kirk.clendinning@oceanoptics.com'
__status__ = 'Development'
__pkg_name__ = 'zephyr'

import unittest
import sys
import ocean_optics_device
import ocean_optics_device.common
import test_units.test_common
from ocean_optics_device.oo_device import *

# must be here so unittest finds the tests
from test_units.test_obp_message import *
from test_units.test_obp_device_introspection import *
from test_units.test_spectrum_acquisition import *


if __name__ == '__main__':
    target_serial_number = ''
    my_interface_type = None

    for index in range(len(sys.argv) - 1, 0, -1):
        if sys.argv[index] == '--sn':
            target_serial_number = sys.argv[index + 1]
            print('Serial number on command line')
            sys.argv.remove(sys.argv[index + 1])
            sys.argv.remove(sys.argv[index])
        else:
            if sys.argv[index] == '--usb':
                my_interface_type = InterfaceType.USB
                print('Looking for USB device')
                sys.argv.remove(sys.argv[index])
            elif sys.argv[index] == '--tcp':
                my_interface_type = InterfaceType.TCP
                print('Looking for TCP device')
                sys.argv.remove(sys.argv[index])
            elif sys.argv[index] == '--spi':
                my_interface_type = InterfaceType.SPI
                print('Looking for SPI device')
                sys.argv.remove(sys.argv[index])
            elif sys.argv[index] == '--i2c':
                my_interface_type = InterfaceType.I2C
                print('Looking for I2C device')
                sys.argv.remove(sys.argv[index])
            elif sys.argv[index] == '--serial':
                my_interface_type = InterfaceType.SERIAL
                print('Looking for SERIAL device')
                sys.argv.remove(sys.argv[index])
            else:
                # USB is the most commonly used interface to date
                my_interface_type = InterfaceType.USB

    if len(target_serial_number) > 0:

        try:
            # the device needs to be identified, so the serial number is read. That means the serial number
            #  facility has to work for any of the other communications based messages can be run
            test_units.test_common.target_device = \
                OceanOpticsDevice(target_serial_number, interface_type=InterfaceType.USB)
        except RuntimeError as myError:
            print(myError.__str__())
            sys.stdout.flush()
    else:
        print('No serial number entered, so no device message tests will be made.')
    unittest.main()
