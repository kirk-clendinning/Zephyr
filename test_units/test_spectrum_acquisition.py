#!/usr/bin/python

"""
Unit test for spectrum acquisition methods
"""

__author__ = "Kirk Clendinning"
__date__ = "2018-04-11"
__copyright__ = "Copyright 2018, Ocean Optics"
__credits__ = ["Kirk Clendinning"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Kirk Clendinning"
__email__ = "kirk.clendinning@oceanoptics.com"
__status__ = "Development"
__pkg_name__ = "zephyr"

import unittest
import ocean_optics_device.common
import test_units.test_common
from test_units.test_common import *
from ocean_optics_device.spectrum_acquisition import SpectrumAcquisition


# ACoo sets this module to be run third
class SpectrumAcquisitionTestCases(unittest.TestCase):

    def setUp(self):
        self.spectrum_acquisition = SpectrumAcquisition(test_units.test_common.target_device)

    def test_spectrum_get(self):
        print("Test spectrum_get")
        if should_this_test_run('OceanFX', 'STS', 'QEPro', 'NIRQuest256', 'NIRQuest512', 'USB4000', 'USB2000+',
                                'Maya2000Pro', 'QE65000', 'MayaLSL', 'HR2000_host',
                                'HR4000_host', 'HR4000_eeprom', 'Jaz'):
            spectrum = self.spectrum_acquisition.spectrum_get()
            self.assertTrue(True, msg="testing code not done yet...")

    def test_integration_time_ms_set(self):
        print("Test integration_time_us_set")
        if should_this_test_run('OceanFX', 'STS', 'QEPro', 'NIRQuest256', 'NIRQuest512', 'USB4000', 'USB2000+',
                                'Maya2000Pro', 'QE65000', 'MayaLSL', 'HR2000_host',
                                'HR4000_host', 'HR4000_eeprom', 'Jaz'):
            # default integration time is 1000ms
            spectrum = self.spectrum_acquisition.integration_time_ms_set()
            self.assertTrue(True, msg="testing code not done yet...")