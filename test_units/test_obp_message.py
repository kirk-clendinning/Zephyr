#!/usr/bin/python

"""
Unit test for the obp_message class
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
from OceanBinaryProtocol import obp_message

# AAaa sets the test order
class AAooMessageTestCases(unittest.TestCase):

    def test_protocol_version(self):
        print('Test protocol_version()')
        message = obp_message.OceanBinaryProtocolMessage()
        self.assertIsInstance(message, obp_message.OceanBinaryProtocolMessage,
                              'The Ocean Binary Protocol message was not instantiated.')

        self.assertEqual(4352, message.protocol_version, "The initial value of protocol_version was wrong.")

        with self.assertRaisesRegex(ValueError, 'The value was out of range. 0x0000 to 0xFFFF inclusive.',
                                    msg='high bounds'):
            message.protocol_version = 65536

        with self.assertRaisesRegex(ValueError, 'The value was out of range. 0x0000 to 0xFFFF inclusive.',
                                    msg='low bounds'):
            message.protocol_version = -1

        message.protocol_version = 32786
        self.assertEqual(32786, message.protocol_version)

    def test_flags(self):
        print("Test flags()")
        message = obp_message.OceanBinaryProtocolMessage()
        self.assertIsInstance(message, obp_message.OceanBinaryProtocolMessage,
                              'The Ocean Binary Protocol message was not instantiated.')

        self.assertEqual(4, message.flags, 'The initial value of flags was wrong.')

        with self.assertRaisesRegex(ValueError, 'The value was out of range. 0x0000 to 0xFFFF inclusive.',
                                    msg='high bounds'):
            message.flags = 65536

        with self.assertRaisesRegex(ValueError, 'The value was out of range. 0x0000 to 0xFFFF inclusive.',
                                    msg='low bounds'):
            message.flags = -1

        message.flags = 32786
        self.assertEqual(32786, message.flags)

    def test_error_number(self):
        print("Test error_number()")
        message = obp_message.OceanBinaryProtocolMessage()
        self.assertIsInstance(message, obp_message.OceanBinaryProtocolMessage,
                              'The Ocean Binary Protocol message was not instantiated.')

        self.assertEqual(0, message.error_number, 'The initial value of error_number was wrong.')

        with self.assertRaisesRegex(ValueError, 'The value was out of range. 0x0000 to 0xFFFF inclusive.',
                                    msg='high bounds'):
            message.error_number = 65536

        with self.assertRaisesRegex(ValueError, 'The value was out of range. 0x0000 to 0xFFFF inclusive.',
                                    msg='low bounds'):
            message.error_number = -1

        message.error_number = 32786
        self.assertEqual(32786, message.error_number)

    def test_message_type(self):
        print("Test message_type()")
        message = obp_message.OceanBinaryProtocolMessage()
        self.assertIsInstance(message, obp_message.OceanBinaryProtocolMessage,
                              'The Ocean Binary Protocol message was not instantiated.')

        self.assertEqual(0, message.message_type, 'The initial value of message_type was wrong.')

        with self.assertRaisesRegex(ValueError, 'The value was out of range. 0x00000000 to 0xFFFFFFFF inclusive.',
                                    msg='high bounds'):
            message.message_type = 4294967296

        with self.assertRaisesRegex(ValueError, 'The value was out of range. 0x00000000 to 0xFFFFFFFF inclusive.',
                                    msg='low bounds'):
            message.message_type = -1

        message.message_type = 2147483647
        self.assertEqual(2147483647, message.message_type)

    def test_regarding(self):
        print("Test regarding()")
        message = obp_message.OceanBinaryProtocolMessage()
        self.assertIsInstance(message, obp_message.OceanBinaryProtocolMessage,
                              'The Ocean Binary Protocol message was not instantiated.')

        self.assertEqual(0, message.regarding, 'The initial value of regarding was wrong.')

        with self.assertRaisesRegex(ValueError, 'The value was out of range. 0x00000000 to 0xFFFFFFFF inclusive.',
                                    msg='high bounds'):
            message.regarding = 4294967296

        with self.assertRaisesRegex(ValueError, 'The value was out of range. 0x00000000 to 0xFFFFFFFF inclusive.',
                                    msg='low bounds'):
            message.regarding = -1

        message.regarding = 2147483647
        self.assertEqual(2147483647, message.regarding)

    def test_reserved(self):
        print("Test reserved()")
        test_reserved = [0x00]*6

        message = obp_message.OceanBinaryProtocolMessage()
        self.assertIsInstance(message, obp_message.OceanBinaryProtocolMessage,
                              'The Ocean Binary Protocol message was not instantiated.')

        self.assertEqual(test_reserved, message.reserved_retrieve(), 'The initial value of regarding was wrong.')

        with self.assertRaisesRegex(TypeError, 'The value should be a 6 element array of bytes.'):
            message.reserved_assign([0]*7)

        with self.assertRaisesRegex(ValueError, 'Element values should be between 0x00 and 0xFF inclusive.',
                                    msg='element low bounds'):
            message.reserved_assign([0, 1, 2, -1, 4, 5])

        with self.assertRaisesRegex(ValueError, 'Element values should be between 0x00 and 0xFF inclusive.',
                                    msg='element high bounds'):
            message.reserved_assign([0, 1, 2, 322, 4, 5])

        for index in range(0, 5):
            with self.assertRaisesRegex(ValueError, 'The value should be between 0x00 and 0xFF inclusive.',
                                        msg='high bounds'):
                message.reserved_set(index, 256)

            with self.assertRaisesRegex(ValueError, 'The value should be between 0x00 and 0xFF inclusive.',
                                        msg='low bounds'):
                message.reserved_set(index, -1)

        for index in range(0, 5):
            message.reserved_set(index, 129 + index)
            test_reserved[index] = 129 + index

        self.assertEqual(test_reserved, message.reserved_retrieve())
        self.assertEqual(129, message.reserved_get(0))

        with self.assertRaisesRegex(IndexError, 'The index should be between 0 and 5 inclusive.'):
            message.reserved_set(6, 129)

        with self.assertRaisesRegex(IndexError, 'The index should be between 0 and 5 inclusive.'):
            bogus = message.reserved_get(6)

    def test_checksum_type(self):
        print('Test checksum_type()')
        message = obp_message.OceanBinaryProtocolMessage()
        self.assertIsInstance(message, obp_message.OceanBinaryProtocolMessage,
                              'The Ocean Binary Protocol message was not instantiated.')

        self.assertEqual(0, message.checksum_type, "The initial value of checksum_type was wrong.")

        with self.assertRaisesRegex(ValueError, 'The value was out of range. 0x00 to 0xFF inclusive.',
                                    msg='high bounds'):
            message.checksum_type = 256

        with self.assertRaisesRegex(ValueError, 'The value was out of range. 0x00 to 0xFF inclusive.',
                                    msg='low bounds'):
            message.checksum_type = -1

        message.checksum_type = 1
        self.assertEqual(1, message.checksum_type)

    def test_immediate_data_length(self):
        print('Test immediate_data_length()')
        message = obp_message.OceanBinaryProtocolMessage()
        self.assertIsInstance(message, obp_message.OceanBinaryProtocolMessage,
                              'The Ocean Binary Protocol message was not instantiated.')

        self.assertEqual(0, message.immediate_data_length, "The initial value of immediate_data_length was wrong.")

        with self.assertRaisesRegex(ValueError, 'The value was out of range. 0x00 to 0xFF inclusive.',
                                    msg='high bounds'):
            message.immediate_data_length = 256

        with self.assertRaisesRegex(ValueError, 'The value was out of range. 0x00 to 0xFF inclusive.',
                                    msg='low bounds'):
            message.immediate_data_length = -1

        message.immediate_data_length = 129
        self.assertEqual(129, message.immediate_data_length)

    def test_immediate_data(self):
        print("Test immediate_data()")
        test_immediate_data = [0x00]*16

        message = obp_message.OceanBinaryProtocolMessage()
        self.assertIsInstance(message, obp_message.OceanBinaryProtocolMessage,
                              'The Ocean Binary Protocol message was not instantiated.')

        self.assertEqual(test_immediate_data, message.immediate_data_retrieve(),
                         'The initial value of regarding was wrong.')

        with self.assertRaisesRegex(TypeError, 'The value should be a 16 element array of bytes.'):
            message.immediate_data_assign([0]*17)

        with self.assertRaisesRegex(ValueError, 'Element values should be between 0x00 and 0xFF inclusive.',
                                    msg='element low bounds'):
            message.immediate_data_assign([47, 166, 245, -12, 212, 59, 78, 92, 23, 14, 77, 32, 90, 184, 65, 192])

        with self.assertRaisesRegex(ValueError, 'Element values should be between 0x00 and 0xFF inclusive.',
                                    msg='element high bounds'):
            message.immediate_data_assign([47, 166, 245, 12, 212, 59, 78, 342, 23, 14, 77, 32, 90, 184, 65, 192])

        with self.assertRaisesRegex(ValueError, 'The value should be between 0x00 and 0xFF inclusive.',
                                    msg='high bounds'):
            message.immediate_data_set(12, 256)

        with self.assertRaisesRegex(ValueError, 'The value should be between 0x00 and 0xFF inclusive.',
                                    msg='low bounds'):
            message.immediate_data_set(8, -1)

        message.immediate_data_set(10, 129)
        test_immediate_data[10] = 129

        self.assertEqual(test_immediate_data, message.immediate_data_retrieve())
        self.assertEqual(129, message.immediate_data_get(10))

        with self.assertRaisesRegex(IndexError, 'The index should be between 0 and 15 inclusive.'):
            message.immediate_data_set(16, 129)

        with self.assertRaisesRegex(IndexError, 'The index should be between 0 and 15 inclusive.'):
            bogus = message.immediate_data_get(16)

    def test_bytes_remaining(self):
        print("Test bytes_remaining()")
        message = obp_message.OceanBinaryProtocolMessage()
        self.assertIsInstance(message, obp_message.OceanBinaryProtocolMessage,
                              'The Ocean Binary Protocol message was not instantiated.')

        self.assertEqual(20, message.bytes_remaining, 'The initial value of bytes_remaining was wrong.')

        with self.assertRaisesRegex(ValueError, 'The value was out of range. 0x00000000 to 0xFFFFFFFF inclusive.',
                                    msg='high bounds'):
            message.bytes_remaining = 4294967296

        with self.assertRaisesRegex(ValueError, 'The value was out of range. 0x00000000 to 0xFFFFFFFF inclusive.',
                                    msg='low bounds'):
            message.bytes_remaining = -1

        message.bytes_remaining = 2147483647
        self.assertEqual(2147483647, message.bytes_remaining)

    def test_payload(self):
        print("Test payload()")
        test_payload = []

        message = obp_message.OceanBinaryProtocolMessage()
        self.assertIsInstance(message, obp_message.OceanBinaryProtocolMessage,
                              'The Ocean Binary Protocol message was not instantiated.')

        self.assertEqual(test_payload, message.payload_retrieve(), 'The initial value of regarding was wrong.')

        message.payload_assign([0]*2316)
        self.assertEqual(message.bytes_remaining, 2336) # 20 plus the size of the payload

        with self.assertRaisesRegex(ValueError, 'Element values should be between 0x00 and 0xFF inclusive.',
                                    msg='low element bounds'):
            message.payload_assign([47, 166, 245, -12, 212, 59, 78, 92, 23, 14, 77, 32, 90, 184, 65, 192])

        with self.assertRaisesRegex(ValueError, 'Element values should be between 0x00 and 0xFF inclusive.',
                                    msg='high element bounds'):
            message.payload_assign([47, 166, 245, 12, 212, 59, 78, 342, 23, 14, 77, 32, 90, 184, 65, 192])

        with self.assertRaisesRegex(ValueError, 'The value should be between 0x00 and 0xFF inclusive.',
                                    msg='high bounds'):
            message.payload_set(12, 256)

        with self.assertRaisesRegex(ValueError, 'The value should be between 0x00 and 0xFF inclusive.',
                                    msg='low bounds'):
            message.payload_set(10, -1)

        message.payload_set(8, 129)
        test_payload = [0]*2316
        test_payload[8] = 129

        self.assertListEqual(test_payload, message.payload_retrieve())
        self.assertEqual(129, message.payload_get(8))

        with self.assertRaisesRegex(IndexError, 'The index should be between '
                                                '0 and {0:d} inclusive.'.format(message.bytes_remaining - 20)):
            message.payload_set(message.bytes_remaining, 129)

        with self.assertRaisesRegex(IndexError, 'The index should be between '
                                                '0 and {0:d} inclusive.'.format(message.bytes_remaining - 20)):
            bogus = message.payload_get(message.bytes_remaining)

    def test_checksum(self):
        print("Test checksum()")
        test_checksum = [0x00]*16

        message = obp_message.OceanBinaryProtocolMessage()
        self.assertIsInstance(message, obp_message.OceanBinaryProtocolMessage,
                              'The Ocean Binary Protocol message was not instantiated.')

        self.assertEqual(test_checksum, message.checksum_retrieve(), 'The initial value of regarding was wrong.')

        with self.assertRaisesRegex(TypeError, 'The value should be a 16 element array of bytes.'):
            message.checksum_assign([0]*17)

        with self.assertRaisesRegex(ValueError, 'Element values should be between 0x00 and 0xFF inclusive.',
                                    msg='element low bounds'):
            message.checksum_assign([47, 166, 245, -12, 212, 59, 78, 92, 23, 14, 77, 32, 90, 184, 65, 192])

        with self.assertRaisesRegex(ValueError, 'Element values should be between 0x00 and 0xFF inclusive.',
                                    msg='element high bounds'):
            message.checksum_assign([47, 166, 245, 12, 212, 59, 78, 342, 23, 14, 77, 32, 90, 184, 65, 192])

        with self.assertRaisesRegex(ValueError, 'The value should be between 0x00 and 0xFF inclusive.',
                                    msg='high bounds'):
            message.checksum_set(12, 256)

        with self.assertRaisesRegex(ValueError, 'The value should be between 0x00 and 0xFF inclusive.',
                                    msg='low bounds'):
            message.checksum_set(8, -1)

        message.checksum_set(10, 129)
        test_checksum[10] = 129

        self.assertEqual(test_checksum, message.checksum_retrieve())
        self.assertEqual(129, message.checksum_get(10))

        with self.assertRaisesRegex(IndexError, 'The index should be between 0 and 15 inclusive.', msg='checksum_set'):
            message.checksum_set(16, 129)

        with self.assertRaisesRegex(IndexError, 'The index should be between 0 and 15 inclusive.', msg='checksum_get'):
            bogus = message.checksum_get(16)

    def test_checksum_calculation(self):
        print("Test compute_checksum_md5()")

        message = obp_message.OceanBinaryProtocolMessage()
        self.assertIsInstance(message, obp_message.OceanBinaryProtocolMessage,
                              'The Ocean Binary Protocol message was not instantiated.')

        message.payload_assign(list(b'This is a test'))
        my_checksum = message.compute_checksum_md5(message.pack_obp())
        self.assertEqual([184, 132, 39, 146, 248, 186, 127, 125, 248, 162, 98, 123, 54, 166, 21, 161],
                         message.checksum_retrieve())

    def test_serialize(self):
        print("Test serialize()")

        message = obp_message.OceanBinaryProtocolMessage()
        self.assertIsInstance(message, obp_message.OceanBinaryProtocolMessage,
                              'The Ocean Binary Protocol message was not instantiated.')

        message.payload_assign(list(b'This is a test'))
        message.checksum_type = 0x01
        my_message = list(message.serialize())
        expected_message = [0xc1, 0xc0, 0x00, 0x11, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x22, 0x00, 0x00, 0x00, 0x54,
                            0x68, 0x69, 0x73, 0x20, 0x69, 0x73, 0x20, 0x61, 0x20, 0x74, 0x65, 0x73, 0x74, 0xAC, 0x9F,
                            0xA9, 0x26, 0xC3, 0x35, 0xE6, 0xBD, 0xBC, 0x8C, 0xAA, 0x54, 0x5B, 0x3D, 0x65, 0x5A, 0xc5,
                            0xc4, 0xc3, 0xc2]
        self.assertEqual(expected_message, my_message)

    def test_deserialize(self):
        print("Test deserialize()")

        message = obp_message.OceanBinaryProtocolMessage()
        self.assertIsInstance(message, obp_message.OceanBinaryProtocolMessage,
                              'The Ocean Binary Protocol message was not instantiated.')

        expected_message = [0xc1, 0xc0, 0x00, 0x11, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x22, 0x00, 0x00, 0x00, 0x54,
                            0x68, 0x69, 0x73, 0x20, 0x69, 0x73, 0x20, 0x61, 0x20, 0x74, 0x65, 0x73, 0x74, 0xAC, 0x9F,
                            0xA9, 0x26, 0xC3, 0x35, 0xE6, 0xBD, 0xBC, 0x8C, 0xAA, 0x54, 0x5B, 0x3D, 0x65, 0x5A, 0xc5,
                            0xc4, 0xc3, 0xc2]
        message.deserialize(bytes(expected_message))
        self.assertEqual(list(b'This is a test'), message.payload_retrieve())

        with self.assertRaisesRegex(ValueError,
                                    'The checksum was incorrect. The message is likely corrupt or malformed.'):
            expected_message = [0xc1, 0xc0, 0x00, 0x11, 0x04, 0x00, 0x00, 0x00,
                                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00,
                                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                0x22, 0x00, 0x00, 0x00, 0x54, 0x68, 0x69, 0x73,
                                0x20, 0x69, 0x73, 0x20, 0x61, 0x20, 0x74, 0x65,
                                0x73, 0x74, 0xAC, 0x9F, 0xA9, 0x26, 0xC3, 0x35,
                                0xE6, 0xBD, 0xBC, 0x8C, 0xAA, 0x54, 0x5B, 0x3D,
                                0x65, 0x00, 0xc5, 0xc4, 0xc3, 0xc2]
            message.deserialize(bytes(expected_message))

        with self.assertRaisesRegex(ValueError,
                                    'An OBP header or footer had the wrong value. Communications is out of sync.'):
            expected_message = [0xc1, 0xc0, 0x00, 0x11, 0x04, 0x00, 0x00, 0x00,
                                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00,
                                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                0x22, 0x00, 0x00, 0x00, 0x54, 0x68, 0x69, 0x73,
                                0x20, 0x69, 0x73, 0x20, 0x61, 0x20, 0x74, 0x65,
                                0x73, 0x74, 0xAC, 0x9F, 0xA9, 0x26, 0xC3, 0x35,
                                0xE6, 0xBD, 0xBC, 0x8C, 0xAA, 0x54, 0x5B, 0x3D,
                                0x65, 0x5A, 0xc5, 0xc4, 0xcc, 0xc2]
            message.deserialize(bytes(expected_message))
