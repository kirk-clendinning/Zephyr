#!/usr/bin/python

"""Provides and interface into obp devices for serial number, firmware and FPGA versions, etc
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
from OceanBinaryProtocol import obp_message
import struct


class DeviceIntrospection:
    def __init__(self, a_device):
        self.__device = a_device

    def reset(self):
        if self.__device.ocean_optics_protocol_get() == ProtocolType.OBP:
            message = obp_message.OceanBinaryProtocolMessage()
            message.message_type = 0x00000000
            reply = self.__device.device_message(message.serialize(), 0)
        elif self.__device.ocean_optics_protocol_get() == ProtocolType.BINARY:
            message = [0x01]
            reply = self.__device.device_message(message, 0)[2::]
        elif self.__device.ocean_optics_protocol_get() == ProtocolType.LETTER:
            message = ['Q']
            reply = self.__device.device_message(message, 0)

    def factory_reset(self):
        if self.__device.ocean_optics_protocol_get() == ProtocolType.OBP:
            message = obp_message.OceanBinaryProtocolMessage()
            message.message_type = 0x00000001
            reply = self.__device.device_message(message.serialize(), 0)
        elif self.__device.ocean_optics_protocol_get() == ProtocolType.BINARY:
            raise RuntimeError("factory_reset() is not available for the BINARY command format.")
        elif self.__device.ocean_optics_protocol_get() == ProtocolType.LETTER:
            raise RuntimeError("factory_reset() is not available for the LETTER command format.")

    def hardware_revision_get(self):
        hardware_revision = None
        if self.__device.ocean_optics_protocol_get() == ProtocolType.OBP:
            message = obp_message.OceanBinaryProtocolMessage()
            message.message_type = 0x00000080
            reply = self.__device.device_message(message.serialize())
            bcd_revision_number = struct.unpack_from('B', reply, 24)[0]
            hardware_revision = '{0:d}.{1:d}'.format(bcd_revision_number & 0xF0, bcd_revision_number & 0x0F)
        elif self.__device.ocean_optics_protocol_get() == ProtocolType.BINARY:
            RuntimeError("suppored_commands_get() is not available for the BINARY command format.")
        elif self.__device.ocean_optics_protocol_get() == ProtocolType.LETTER:
            raise RuntimeError("suppored_commands_get() is not available for the LETTER command format.")
        return hardware_revision

    # Not sure if this command is actually supported by Ocean FX
    def supported_commands_get(self):
        supported_commands = None
        if self.__device.ocean_optics_protocol_get() == ProtocolType.OBP:
            message = obp_message.OceanBinaryProtocolMessage()
            message.message_type = 0x00000082
            reply = self.__device.device_message(message.serialize())
            supported_commmands = struct.unpack_from(
                '{0:d}s'.format(struct.unpack_from('B', reply, 23)[0]), reply, 24)[0].decode('UTF-8')
        elif self.__device.ocean_optics_protocol_get() == ProtocolType.BINARY:
            RuntimeError("suppored_commands_get() is not available for the BINARY command format.")
        elif self.__device.ocean_optics_protocol_get() == ProtocolType.LETTER:
            raise RuntimeError("suppored_commands_get() is not available for the LETTER command format.")
        return supported_commands

    def firmware_revision_get(self):
        firmware_revision = None
        if self.__device.ocean_optics_protocol_get() == ProtocolType.OBP:
            message = obp_message.OceanBinaryProtocolMessage()
            message.message_type = 0x00000090
            reply = self.__device.device_message(message.serialize())
            bcd_revision_number = struct.unpack_from('<H', reply, 24)[0]
            firmware_revision = '{0:d}.{1:d}.{2:d}.{3:d}'.format((bcd_revision_number & 0xF000)>>12,
                                                                 (bcd_revision_number & 0x0F00)>>8,
                                                                 (bcd_revision_number & 0x00F0)>>4,
                                                                 bcd_revision_number & 0x000F)
        elif self.__device.ocean_optics_protocol_get() == ProtocolType.BINARY:
            RuntimeError("firmware_revision_get() is not available for the BINARY command format.")
        elif self.__device.ocean_optics_protocol_get() == ProtocolType.LETTER:
            raise RuntimeError("firmware_revision_get() is not available for the LETTER command format.")
        return firmware_revision

    def secondary_firmware_revision_get(self):
        secondary_firmware_revision = None
        if self.__device.ocean_optics_protocol_get() == ProtocolType.OBP:
            message = obp_message.OceanBinaryProtocolMessage()
            message.message_type = 0x00000091
            reply = self.__device.device_message(message.serialize())
            bcd_revision_number = struct.unpack_from('<H', reply, 24)[0]
            secondary_firmware_revision = '{0:d}.{1:d}.{2:d}.{3:d}'.format((bcd_revision_number & 0xF000)>>12,
                                                                 (bcd_revision_number & 0x0F00)>>8,
                                                                 (bcd_revision_number & 0x00F0)>>4,
                                                                 bcd_revision_number & 0x000F)
        elif self.__device.ocean_optics_protocol_get() == ProtocolType.BINARY:
            message = [0x6A, 0x04]
            reply = self.__device.device_message(message, 4)[2:4]
            serial_number = reply[0:next((i for i, j in enumerate(reply) if j == 0), 14):].decode('UTF-8')
        elif self.__device.ocean_optics_protocol_get() == ProtocolType.LETTER:
            raise RuntimeError("secondary_firmware_revision_get() is not available for the LETTER command format.")
        return secondary_firmware_revision

    def firmware_subrevision_get(self):
        firmware_subrevision = None
        if self.__device.ocean_optics_protocol_get() == ProtocolType.OBP:
            message = obp_message.OceanBinaryProtocolMessage()
            message.message_type = 0x00000092
            reply = self.__device.device_message(message.serialize())
            bcd_revision_number = struct.unpack_from('<H', reply, 24)[0]
            firmware_subrevision = '{0:d}.{1:d}.{2:d}.{3:d}'.format((bcd_revision_number & 0xF000)>>12,
                                                                 (bcd_revision_number & 0x0F00)>>8,
                                                                 (bcd_revision_number & 0x00F0)>>4,
                                                                 bcd_revision_number & 0x000F)
        elif self.__device.ocean_optics_protocol_get() == ProtocolType.BINARY:
            RuntimeError("firmware_subrevision_get() is not available for the BINARY command format.")
        elif self.__device.ocean_optics_protocol_get() == ProtocolType.LETTER:
            raise RuntimeError("firmware_subrevision_get() is not available for the LETTER command format.")
        return firmware_subrevision

    def serial_number_get(self):
        serial_number = None
        if self.__device.ocean_optics_protocol_get() == ProtocolType.OBP:
            message = obp_message.OceanBinaryProtocolMessage()
            message.message_type = 0x00000100
            reply = self.__device.device_message(message.serialize())
            serial_number = struct.unpack_from(
                '{0:d}s'.format(struct.unpack_from('B', reply, 23)[0]), reply, 24)[0].decode('UTF-8')
        elif self.__device.ocean_optics_protocol_get() == ProtocolType.BINARY:
            message = [0x05, 0x00]
            reply = self.__device.device_message(message, 17)[2::]
            serial_number = reply[0:next((i for i, j in enumerate(reply) if j == 0), 14):].decode('UTF-8')
        elif self.__device.ocean_optics_protocol_get() == ProtocolType.LETTER:
            raise RuntimeError("serial_number_get() is not available for the LETTER command format.")
        return serial_number

    def serial_number_length_get(self):
        serial_number_length = None
        if self.__device.ocean_optics_protocol_get() == ProtocolType.OBP:
            message = obp_message.OceanBinaryProtocolMessage()
            message.message_type = 0x00000101
            reply = self.__device.device_message(message.serialize())
            serial_number_length = struct.unpack_from('B', reply, 24)[0]
        elif self.__device.ocean_optics_protocol_get() == ProtocolType.BINARY:
            serial_number_length = 15  # by definition of the protocol query data are 15 bytes long
        elif self.__device.ocean_optics_protocol_get() == ProtocolType.LETTER:
            raise RuntimeError("serial_number_get() is not available for the LETTER command format.")
        return serial_number_length
