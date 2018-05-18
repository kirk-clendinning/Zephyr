#!/usr/bin/python

"""Ocean Binary Protocol is used by Ocean Optics to control spectrometer and accessory functionality
A 64 byte frame, which includes up to 16 bytes of data, is mandatory for all messages. Longer messages, such
as spectra, are embedded within the frame as extended data.
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

import hashlib
import struct


class OceanBinaryProtocolMessage:

    def __init__(self):
        self.__header = 0xC0C1               # used to identify the start of the message (little endian)
        self.__protocol_version = 0x1100     # version of obp being used. This hasn't been kept relevant (little endian)
        self.__flags = 0x0004                # indicates status of the message, reply requested  (little endian)
        self.__error_number = 0x0000         # indicates success or the cause of an error  (little endian)
        self.__message_type = 0x00000000     # action to be taken by the device  (little endian)
        self.__regarding = 0x00000000        # allows messages to be linked  (little endian)
        self.__reserved = [0x00] * 6           # six bytes of data for future use  (little endian)
        self.__checksum_type = 0x00          # 0x00 is no check sum, 0x01 is a 16 byte md5
        self.__immediate_data_length = 0x00  # number immediate data bytes that are being used
        self.__immediate_data = [0x00] * 16
        self.__bytes_remaining = 0x00000014  # the number of bytes that follow, payload length + 20 (little endian)
        self.__payload = []
        self.__checksum = [0x00] * 16
        self.__footer = 0xC2C3C4C5           # identifies the end of the message (little endian)

    def initialize(self):
        self.__init__()

    @property
    def protocol_version(self):
        return self.__protocol_version

    @protocol_version.setter
    def protocol_version(self, value):
        if(value >= 0x0000) and (value <= 0xFFFF):
            self.__protocol_version = value
        else:
            raise ValueError('The value was out of range. 0x0000 to 0xFFFF inclusive.')

    @property
    def flags(self):
        return self.__flags

    @flags.setter
    def flags(self, value):
        if(value >= 0x0000) and (value <= 0xFFFF):
            self.__flags = value
        else:
            raise ValueError('The value was out of range. 0x0000 to 0xFFFF inclusive.')

    @property
    def error_number(self):
        return self.__error_number

    @error_number.setter
    def error_number(self, value):
        if(value >= 0x0000) and (value <= 0xFFFF):
            self.__error_number = value
        else:
            raise ValueError('The value was out of range. 0x0000 to 0xFFFF inclusive.')

    @property
    def message_type(self):
        return self.__message_type

    @message_type.setter
    def message_type(self, value):
        if(value >= 0x00000000) and (value <= 0xFFFFFFFF):
            self.__message_type = value
        else:
            raise ValueError('The value was out of range. 0x00000000 to 0xFFFFFFFF inclusive.')

    @property
    def regarding(self):
        return self.__regarding

    @regarding.setter
    def regarding(self, value):
        if (value >= 0x00000000) and (value <= 0xFFFFFFFF):
            self.__regarding = value
        else:
            raise ValueError('The value was out of range. 0x00000000 to 0xFFFFFFFF inclusive.')

    def reserved_retrieve(self):
        return list(self.__reserved)

    def reserved_assign(self, value):
        if len(value) == 6:
            in_bounds = True
            for index in range(0,5):
                if (value[index] < 0) or (value[index] > 255):
                    in_bounds = False
                    break
            if in_bounds:
                self.__reserved = value
            else:
                raise ValueError('Element values should be between 0x00 and 0xFF inclusive.')
        else:
            raise TypeError('The value should be a 6 element array of bytes.')

    def reserved_set(self, index, value):
        if (index >= 0) and (index <= 5):
            if(value >= 0) and (value <=255):
                self.__reserved[index] = value
            else:
                raise ValueError('The value should be between 0x00 and 0xFF inclusive.')
        else:
            raise IndexError('The index should be between 0 and 5 inclusive.')

    def reserved_get(self, index):
        if (index >= 0) and (index <= 5):
            return self.__reserved[index]
        else:
            raise IndexError('The index should be between 0 and 5 inclusive.')

    @property
    def checksum_type(self):
        return self.__checksum_type

    @checksum_type.setter
    def checksum_type(self, value):
        if (value >= 0x00) and (value <= 0xFF):
            self.__checksum_type = value
        else:
            raise ValueError('The value was out of range. 0x00 to 0xFF inclusive.')

    @property
    def immediate_data_length(self):
        return self.__immediate_data_length

    @immediate_data_length.setter
    def immediate_data_length(self, value):
        if (value >= 0x00) and (value <= 0xFF):
            self.__immediate_data_length = value
        else:
            raise ValueError('The value was out of range. 0x00 to 0xFF inclusive.')

    def immediate_data_retrieve(self):
        return list(self.__immediate_data)

    def immediate_data_assign(self, value):
        if len(value) == 16:
            in_bounds = True
            for index in range(0,15):
                if (value[index] < 0x00) or (value[index] > 0xFF):
                    in_bounds = False
                    break
            if in_bounds:
                self.__immediate_data = value
            else:
                raise ValueError('Element values should be between 0x00 and 0xFF inclusive.')
        else:
            raise TypeError('The value should be a 16 element array of bytes.')

    def immediate_data_set(self, index, value):
        if(index >= 0) and (index <= 15):
            if (value >= 0x00) and (value <= 0xFF):
                self.__immediate_data[index] = value
            else:
                raise ValueError('The value should be between 0x00 and 0xFF inclusive.')
        else:
            raise IndexError('The index should be between 0 and 15 inclusive.')

    def immediate_data_get(self, index):
        if(index >= 0) and (index <= 15):
            return self.__immediate_data[index]
        else:
            raise IndexError('The index should be between 0 and 15 inclusive.')

    @property
    def bytes_remaining(self):
        return self.__bytes_remaining

    @bytes_remaining.setter
    def bytes_remaining(self, value):
        if(value >= 0x00000000) and (value <= 0xFFFFFFFF):
            self.__bytes_remaining = value
        else:
            raise ValueError('The value was out of range. 0x00000000 to 0xFFFFFFFF inclusive.')

    def payload_retrieve(self):
        return self.__payload

    def payload_assign(self, value):
        in_bounds = True
        for index in range(0,len(value)):
            if (value[index] < 0) or (value[index] > 255):
                in_bounds = False
                break
        if in_bounds:
            self.__payload = value
            self.__bytes_remaining = len(value) + 20
        else:
            raise ValueError('Element values should be between 0x00 and 0xFF inclusive.')

    def payload_set(self, index, value):
        if(index >= 0) and (index <= len(self.__payload)):
            if (value >= 0x00) and (value <= 0xFF):
                self.__payload[index] = value
            else:
                raise ValueError('The value should be between 0x00 and 0xFF inclusive.')
        else:
            raise IndexError('The index should be between 0 and {0:d} inclusive.'.format(len(self.__payload)))

    def payload_get(self, index):
        if (index >= 0) and (index <= len(self.__payload)):
            return self.__payload[index]
        else:
            raise IndexError('The index should be between 0 and {0:d} inclusive.'.format(len(self.__payload)))

    def checksum_retrieve(self):
        return self.__checksum

    def checksum_assign(self, value):
        if len(value) == 16:
            in_bounds = True
            for index in range(0,15):
                if (value[index] < 0) or (value[index] > 255):
                    in_bounds = False
                    break
            if in_bounds:
                self.__checksum = value
            else:
                raise ValueError('Element values should be between 0x00 and 0xFF inclusive.')
        else:
            raise TypeError('The value should be a 16 element array of bytes.')

    def checksum_set(self, index, value):
        if(index >= 0) and (index <= 15):
            if (value >= 0x00) and (value <= 0xFF):
                self.__checksum[index] = value
            else:
                raise ValueError('The value should be between 0x00 and 0xFF inclusive.')
        else:
            raise IndexError('The index should be between 0 and 15 inclusive.')

    def checksum_get(self, index):
        if (index >= 0) and (index <= 15):
            return self.__checksum[index]
        else:
            raise IndexError('The index should be between 0 and 15 inclusive.')

    def pack_obp(self):
        format_string = '<HHHHII6sBB16sI{0:d}s'.format(len(self.__payload))
        packed_obp = struct.pack(format_string, self.__header, self.__protocol_version, self.__flags, self.__error_number,
                          self.__message_type, self.__regarding, bytes(self.__reserved), self.__checksum_type,
                          self.__immediate_data_length, bytes(self.__immediate_data), self.__bytes_remaining,
                          bytes(self.__payload))
        return packed_obp

    def unpack_obp(self, obp_message):
        payload_size = struct.unpack_from('I', obp_message, 40)

    def compute_checksum_md5(self, packed_obp):
        md5 = hashlib.md5()
        md5.update(packed_obp)
        self.__checksum = list(md5.digest())

    def serialize(self):
        if self.checksum_type == 0x01:
            my_message = self.pack_obp()
            self.compute_checksum_md5(my_message)
        else:
            my_message = self.pack_obp()

        return struct.pack('<{0:d}s16sI'.format(len(my_message)), my_message, bytes(self.__checksum), self.__footer)

    def deserialize(self, obp_message):
        payload_length = struct.unpack_from('<I', obp_message, 40)[0] - 20
        my_message = struct.unpack('<HHHHII6sBB16sI{0:d}s16sI'.format(payload_length), obp_message)
        if (self.__header != my_message[0]) or (self.__footer != my_message[13]):
            raise ValueError('An OBP header or footer had the wrong value. Communications is out of sync.')
        else:
            # put all of the values into the appropriate variables
            self.__protocol_version = my_message[1]
            self.__flags = my_message[2]
            self.__error_number = my_message[3]
            self.__message_type = my_message[4]
            self.__regarding = my_message[5]
            self.__reserved = list(my_message[6])
            self.__checksum_type = my_message[7]
            self.__immediate_data_length = my_message[8]
            self.__immediate_data = list(my_message[9])
            self.__bytes_remaining = my_message[10]
            self.__payload = list(my_message[11])

            # confirm that the checksum, if any is correct
            if self.__checksum_type == 0x01:
                my_checksum = list(my_message[12])
                self.compute_checksum_md5(self.pack_obp())
                if my_checksum != self.__checksum:
                    raise ValueError('The checksum was incorrect. The message is likely corrupt or malformed.')

    def error_code_description(self, error_code):
        if error_code == 0:
            description = 'Success(no detectable errors).'
        elif error_code == 1:
            description = 'Invalid / unsupported protocol.'
        elif error_code == 2:
            description = 'Unknown message type.'
        elif error_code == 3:
            description = 'Bad checksum.'
        elif error_code == 4:
            description = 'Message too large.'
        elif error_code == 5:
            description = 'Payload length does not match message type.'
        elif error_code == 6:
            description = 'Payload data invalid.'
        elif error_code == 7:
            description = 'Device not ready for given message type.'
        elif error_code == 8:
            description = 'Unknown checksum type.'
        elif error_code == 9:
            description = 'Device reset unexpectedly.'
        elif error_code == 10:
            description = 'Too many buses. Messages have come from too many different bus interfaces.'
        elif error_code == 11:
            description = 'Out of memory. Failed to allocate enough space to complete the request.'
        elif error_code == 12:
            description = 'Message is valid, but requesterd information does not exist.'
        elif error_code == 13:
            description = 'Internal error. May be unrecoverable.'
        elif error_code == 14:
            description = 'Message did not end properly'
        elif error_code == 15:
            description = 'Current scan interrupted.'
        elif error_code == 100:
            description = 'Could not decrypt properly.'
        elif error_code == 101:
            description = 'Firmware layout invalid.'
        elif error_code == 102:
            description = 'Data packet was wrong size (not 64 bytes).'
        elif error_code == 103:
            description = 'Hardware revision is not compatible with downloaded firmware.'
        elif error_code == 104:
            description = 'Existing flash map not compatible with downloaded firmware.'
        else:
            description = 'Unknown error code.'
        return description
