#!/usr/bin/python

"""
Common definitions
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

from enum import Enum


class ProtocolType(Enum):
    OBP = 0
    BINARY = 1
    LETTER = 2


class InterfaceType(Enum):
    USB = 0
    TCP = 1
    SERIAL = 2
    SPI = 3
    I2C = 4

class ReadOrWrite(Enum):
    READ = 0
    WRITE = 1


class DeviceIdentity:
    def __init__(self):
        self.__usb_oo_protocol_type_device_name = \
            {
                0x1002: (ProtocolType.BINARY, 'USB2000', (0x02, 0x07), (0x82, 0x87)),
                0x1009: (ProtocolType.BINARY, 'HR2000_host', (0x02, 0x07), (0x82, 0x87)),
                0x100A: (ProtocolType.BINARY, 'HR2000_eeprom', (0x02, 0x07), (0x82, 0x87)),
                0x1011: (ProtocolType.BINARY, 'HR4000_host', (0x01,), (0x81, 0x82, 0x86)),
                0x1012: (ProtocolType.BINARY, 'HR4000_eeprom', (0x01,), (0x81, 0x82, 0x86)),
                0x1016: (ProtocolType.BINARY, 'HR2000+', (0x01,), (0x81, 0x82, 0x86)),
                0x1018: (ProtocolType.BINARY, 'QE65000', (0x01,), (0x81, 0x82, 0x86)),
                0x101E: (ProtocolType.BINARY, 'USB2000+', (0x01,), (0x81, 0x82, 0x86)),
                0x1022: (ProtocolType.BINARY, 'USB4000', (0x01,), (0x81, 0x82, 0x86)),
                0x1026: (ProtocolType.BINARY, 'NIRQuest512', (0x01,), (0x81, 0x82, 0x86)),
                0x1028: (ProtocolType.BINARY, 'NIRQuest256', (0x01,), (0x81, 0x82, 0x86)),
                0x102A: (ProtocolType.BINARY, 'Maya2000Pro', (0x01,), (0x81, 0x82, 0x86)),
                0x102C: (ProtocolType.BINARY, 'Maya2000', (0x01,), (0x81, 0x82, 0x86)),
                0x1044: (ProtocolType.BINARY, 'Apex', (0x01,), (0x81, 0x82)),
                0x1046: (ProtocolType.BINARY, 'MayaLSL', (0x01,), (0x81, 0x82, 0x86)),
                0x104B: (ProtocolType.BINARY, 'FlameNIR', (0x01,), (0x81, 0x82, 0x86)),
                0x2000: (ProtocolType.BINARY, 'Jaz', (0x01,), (0x81, 0x82)),
                0x2001: (ProtocolType.OBP, 'OceanFX', (0x01,), (0x81,)),
                0x4000: (ProtocolType.OBP, 'STS', (0x01, 0x02), (0x81, 0x82, 0x83)),
                0x4200: (ProtocolType.OBP, 'Spark', (0x01, 0x02), (0x81, 0x82))
            }

    def get_usb_endpoints(self, product_id, read_or_write):
        endpoints = None
        if product_id is not None:
            if read_or_write == ReadOrWrite.READ:
                endpoints = self.__usb_oo_protocol_type_device_name.get(product_id)[3]
            else:
                endpoints = self.__usb_oo_protocol_type_device_name.get(product_id)[2]
        return endpoints

    def get_protocol(self, serial_number, interface_type):
        oo_protocol = None

        # serial and tcp interfaces always use the same protocol
        if interface_type == InterfaceType.SERIAL:
            oo_protocol = ProtocolType.LETTER
        elif interface_type == InterfaceType.TCP:
            oo_protocol = ProtocolType.OBP
        else:
            if (serial_number.find('OFX') == 0) or (serial_number.find('QEP') == 0) or (serial_number.find('S') == 0):
                oo_protocol = ProtocolType.OBP
            else:
                oo_protocol = ProtocolType.BINARY

        return oo_protocol

    def get_product_id_from_unique_name(self, name):
        for device_info in self.__usb_oo_protocol_type_device_name:
            if device_info[1][1] == name:
                return device_info[1][0]

    def get_ocean_optics_device_protocol(self, productID):
        return self.__usb_oo_protocol_type_device_name.get(productID)[0]

    def get_ocean_optics_device_name(self, productID):
        return self.__usb_oo_protocol_type_device_name.get(productID)[1]

device_identity = DeviceIdentity()
