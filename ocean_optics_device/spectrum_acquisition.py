#!/usr/bin/python

"""
This class ways of discovering ocean optics devices on usb and ethernet/tcp
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

from ocean_optics_device.common import *
from ocean_optics_device.oo_device import *
from OceanBinaryProtocol import obp_message
import struct
import ctypes


class SpectrumAcquisition:
    def __init__(self, a_device):
        self.__device = a_device

    # immediate spectrum, blocking until spectrum available
    def spectrum_get(self, data_length=0):
        spectrum = None
        if self.__device.ocean_optics_protocol_get() == ProtocolType.OBP:
            message = obp_message.OceanBinaryProtocolMessage()
            message.message_type = 0x00101000
            reply = self.__device.device_message(message.serialize())
            # when a spectrum is sent, it can be assumed that the immediate data is not used.
            # with obp, the size of data to be returned is contained in the bytes remaining - 20 for checksum and
            #  footer
            spectrum = struct.unpack_from('{0:d}s'.format(struct.unpack_from('<I', reply, 40)[0] - 20), reply, 44)[0]
        elif self.__device.ocean_optics_protocol_get() == ProtocolType.BINARY:
            # for the FX2 protocol, the user must specify the number of bytes to be retrieved. It is device dependent
            message = [0x09]
            spectrum = self.__device.device_message(message, data_length)
        elif self.__device.ocean_optics_protocol_get() == ProtocolType.LETTER:
            message = ['S']
            spectrum = self.__device.device_message(message, data_length)
        return spectrum

    def integration_time_ms_set(self, integration_time_ms=1000):
        self.integration_time_us_set(integration_time_ms * 1000)

    # set integration time in microseconds
    def integration_time_us_set(self, integration_time_us=1000):
        if self.__device.ocean_optics_protocol_get() == ProtocolType.OBP:
            message = obp_message.OceanBinaryProtocolMessage()
            message.message_type = 0x00110010
            message.immediate_data_length = 0x04
            immediate_data = ctypes.create_string_buffer(16)
            struct.pack_into('<I', immediate_data, 0, integration_time_us)
            message.immediate_data_assign(bytes(immediate_data))
            reply = self.__device.device_message(message.serialize())
            error_code = struct.unpack_from('<H', reply, 6)[0]
            if error_code != 0:
                raise RuntimeError('obp_error_code={0:d}'.format(error_code))
        elif self.__device.ocean_optics_protocol_get() == ProtocolType.BINARY:
            # for the FX2 protocol, the user must specify the number of bytes to be retrieved. It is device dependent
            reply = self.__device.device_message(struct.pack('<BI', 0x02, integration_time_us), 0)
        elif self.__device.ocean_optics_protocol_get() == ProtocolType.LETTER:
            my_data = 'i{0:d}'.format(integration_time_us)
            message = struct.pack('{0:d}s'.format(len(my_data)), my_data)
            reply = self.__device.device_message(message, 0)
