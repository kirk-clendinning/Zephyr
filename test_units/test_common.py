#!/usr/bin/python

"""
Common definitions for unit test
"""

__author__ = 'Kirk Clendinning'
__date__ = '2018-04-09'
__copyright__ = 'Copyright 2018, Ocean Optics'
__credits__ = ['Kirk Clendinning']
__license__ = 'GPL'
__version__ = '1.0.0'
__maintainer__ = 'Kirk Clendinning'
__email__ = 'kirk.clendinning@oceanoptics.com'
__status__ = 'Development'
__pkg_name__ = 'zephyr'

import sys
from ocean_optics_device.oo_device import *
from ocean_optics_device.common import DeviceIdentity

target_device = None


def should_this_test_run(*devices_to_test):
    result = False
    if target_device != None:
        product_name = device_identity.get_ocean_optics_device_name(target_device.product_id_get())
        if product_name in devices_to_test:
             result = True
        else:
            print('--->Not implemented for {0}.'.format((product_name)))
            sys.stdout.flush()
    return result