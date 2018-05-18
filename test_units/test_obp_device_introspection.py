#!/usr/bin/python

"""
Unit test for the obp device introspection methods
"""

__author__ = "Kirk Clendinning"
__date__ = "2018-04-02"
__copyright__ = "Copyright 2018, Ocean Optics"
__credits__ = ["Kirk Clendinning"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Kirk Clendinning"
__email__ = "kirk.clendinning@oceanoptics.com"
__status__ = "Development"
__pkg_name__ = "zephyr"

import unittest
import test_units.test_common
from test_units.test_common import *
from ocean_optics_device.device_introspection import DeviceIntrospection


# ACoo sets this module to be run third
class ACooDeviceIntrospectionTestCases(unittest.TestCase):

    def setUp(self):
        self.introspection = DeviceIntrospection(test_units.test_common.target_device)

    def test_serial_number_length_get(self):
        test = target_device
        print("Test serial_number_length_get")
        if should_this_test_run('OceanFX', 'STS', 'QEPro', 'NIRQuest256', 'NIRQuest512', 'USB4000', 'USB2000+',
                                'Maya2000Pro', 'QE65000', 'MayaLSL', 'HR2000_host',
                                'HR4000_host', 'HR4000_eeprom', 'Jaz'):
            serial_number_length = self.introspection.serial_number_length_get()
            self.assertTrue((serial_number_length == 15) or (serial_number_length == 16) or (serial_number_length == 32),
                            msg="The serial length number was not in the expected range.")

    def test_reset(self):
        if target_device is not None:
            print("reset is currently not tested")

    def test_factory_reset(self):
        if target_device is not None:
            print("factory reset is currently not tested")

    @unittest.skip('This command is apparently not working on the OceanFX')
    def test_supported_commands_get(self):
        print("Test supported_commands_get")
        if should_this_test_run('OceanFX'):
            supported_commands = self.introspection.supported_commands_get()
            test = 1
            #self.assertTrue((len(supported_commands) > 15),
             #               msg="The supported commands number was not in the expected range.")

    @unittest.skip('This command is not supported on the OceanFX')
    def test_hardware_revision_get(self):
        print("Test hardware_revision_get")
        if should_this_test_run('STS', 'QEPro', 'NIRQuest256', 'NIRQuest512', 'USB4000', 'USB2000+',
                                'Maya2000Pro', 'QE65000', 'MayaLSL', 'HR2000_host',
                                'HR4000_host', 'HR4000_eeprom', 'Jaz'):
            hardware_revision = self.introspection.hardware_revision_get()
            self.assertTrue(True, msg="The not done yet....")

    def test_firmware_revision_get(self):
        print("Test firmware_revision_get")
        if should_this_test_run('OceanFX', 'STS', 'QEPro', 'NIRQuest256', 'NIRQuest512', 'USB4000', 'USB2000+',
                                'Maya2000Pro', 'QE65000', 'MayaLSL', 'HR2000_host',
                                'HR4000_host', 'HR4000_eeprom', 'Jaz'):
            firmware_revision = self.introspection.firmware_revision_get()
            self.assertTrue(True, msg="Not done yet...")

    def test_secondary_firmware_revision_get(self):
        print("Test secondary_firmware_revision_get")
        if should_this_test_run('OceanFX', 'QEPro', 'NIRQuest256', 'NIRQuest512', 'USB4000', 'USB2000+',
                                'Maya2000Pro', 'QE65000', 'MayaLSL', 'HR2000_host',
                                'HR4000_host', 'HR4000_eeprom', 'Jaz'):
            secondary_firmware_revision = self.introspection.secondary_firmware_revision_get()
            self.assertTrue(True, msg="Not done yet...")
