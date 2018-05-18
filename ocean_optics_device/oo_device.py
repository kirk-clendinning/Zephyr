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


from ocean_optics_device.device_introspection import *
from ocean_optics_device.spectrum_acquisition import *

import sys
from usb import core
from usb import util
from ocean_optics_device.common import *

# ToDo: just written. currently untested
def find_all_usb_devices():
    device_list = list()
    try:
        all_devices = core.find(find_all=True, idVendor=0x2457)
        for a_usb_device in all_devices:
            try:
                a_usb_device.set_configuration()
            except core.USBError:
                raise core.USBError("Could not configure the usb device in OceanOpticsDevice.find_usb_device()")

            oo_protocol = device_identity.get_ocean_optics_device_protocol(a_usb_device.idProduct)
            oo_device_name = device_identity.get_ocean_optics_device_name(a_usb_device.idProduct)
            oo_device = OceanOpticsDevice(interface_type=InterfaceType.USB, product_id=a_usb_device.idProduct,
                                          ocean_optics_protocol=oo_protocol,
                                          ocean_optics_device_name = oo_device_name)
            device_list.append(a_usb_device)
    except core.NoBackendError:
        raise RuntimeError("Error: libusb is probably not installed on the host machine.\n{0}", sys.exc_info()[0])
    return device_list


class OceanOpticsDevice:

    def __init__(self, serial_number=None, interface_type=None, ocean_optics_protocol=None,
                 product_id=None, tcp_port=57357, ocean_optics_device_name=None):

        # bring in all of the message types. These are done in smaller classes to make things easier to read
        self.__introspection_methods = DeviceIntrospection(self)
        self.__spectrum_acquisition_methods = SpectrumAcquisition(self)

        self.__endpoints_write = (0x01,)
        self.__endpoints_read = (0x81,)

        self.__tcp_port = tcp_port
        self.__interface_type = interface_type
        self.__serial_number = serial_number
        self.__device_name = ocean_optics_device_name
        self.__usb_device = None
        self.__tcp_socket = None

        if product_id is not None:
            self.__product_id = product_id
            self.set_product_id_and_usb_endpoints(product_id)
            self.__introspection_methods.serial_number_get()

        if (serial_number is not None) and (interface_type is not None):

            if ocean_optics_protocol is None:
                self.__ocean_optics_protocol = \
                    device_identity.get_protocol(serial_number, interface_type)
            else:
                self.__ocean_optics_protocol = ocean_optics_protocol

            if self.__interface_type == InterfaceType.USB:
                if not self.find_usb_device(serial_number):
                    raise RuntimeError('USB device, {0:s}, was not found.'.format(serial_number))
            elif self.__interface_type == InterfaceType.TCP:
                if not self.find_network_device(serial_number):
                    raise RuntimeError('Network device, {0:s}, was not found.'.format(serial_number))
            elif self.__interface_type == InterfaceType.SPI:
                if not self.find_spi_device(serial_number):
                    raise RuntimeError('SPI device, {0:s}, was not found.'.format(serial_number))
            elif self.__interface_type == InterfaceType.I2C:
                if not self.find_i2c_device(serial_number):
                    raise RuntimeError('I2C device, {0:s}, was not found.'.format(serial_number))
            elif self.__interface_type == InterfaceType.SERIAL:
                if not self.find_rs232_device(serial_number):
                    raise RuntimeError('SERIAL device, {0:s}, was not found.'.format(serial_number))
            else:
                raise RuntimeError(
                    'Unknown interface type, {0}, in OceanOpticsDevice()'.format(str(self.__interface_type)))

    def set_product_id_and_usb_endpoints(self, product_id):
        if product_id is not None:
            self.__product_id = product_id
            self.__endpoints_write = device_identity.get_usb_endpoints(product_id, ReadOrWrite.WRITE)
            self.__endpoints_read = device_identity.get_usb_endpoints(product_id, ReadOrWrite.READ)

    # the first letters of the serial number give a hint as to what kind of device it is so that the usb endpoints
    #  can be surmised
    def set_usb_endpoints(self, serial_number):
        pass

    def usb_1st_read_endpoint_get(self):
        return self.__endpoints_read[0]

    def usb_1st_write_endpoint_get(self):
        return self.__endpoints_write[0]

    def usb_2nd_read_endpoint_get(self):
        return self.__endpoints_read[1]

    def usb_2nd_write_endpoint_get(self):
        return self.__endpoints_write[1]

    def usb_3rd_read_endpoint_get(self):
        return self.__endpoints_read[2]

    def usb_3rd_write_endpoint_get(self):
        return self.__endpoints_write[2]

    def product_id_get(self):
        return self.__product_id

    def ocean_optics_protocol_get(self):
        return self.__ocean_optics_protocol

    def interface_type_get(self):
        return self.__interface_type

    def serial_number_get(self):
        return self.__serial_number

    def device_message(self, data, expected_reply_size=64, usb_read_endpoint=None, usb_write_endpoint=None):
        reply = None
        # if no endpoints are given use the primary endpoints
        if usb_read_endpoint is None:
            usb_read_endpoint = self.__endpoints_read[0]
        if usb_write_endpoint is None:
            usb_write_endpoint = self.__endpoints_write[0]

        if self.__interface_type == InterfaceType.USB:
            try:
                self.__usb_device.write(usb_write_endpoint, data, timeout=1000)
                if expected_reply_size > 0:
                    reply = self.__usb_device.read(usb_read_endpoint, expected_reply_size, timeout=1000)
                    error_code = struct.unpack_from('<H', reply, 6)[0]
                    if error_code == 0:
                        if self.__ocean_optics_protocol == ProtocolType.OBP:
                            bytes_remaining = struct.unpack_from('I', reply, 40)[0]
                            if bytes_remaining > 20:
                                reply += self.__usb_device.read(usb_read_endpoint, bytes_remaining - 20, timeout=1000)
                    else:
                        raise RuntimeError('obp_error_code={0:d}'.format(error_code))
            except core.USBError as myError:
                print('USBError :' + myError.__str__())
        elif self.__interface_type == InterfaceType.TCP:
            pass
        elif self.__interface_type == InterfaceType.SERIAL:
            pass
        elif self.__interface_type == InterfaceType.SPI:
            pass
        elif self.__interface_type == InterfaceType.I2C:
            pass
        else:
            raise RuntimeError("Unknown device type in OceanOpticsDevice.write()")
        return bytes(reply)

    def find_usb_device(self, serial_number):
        # return a usb_device
        try:
            all_devices = core.find(find_all = True, idVendor=0x2457)
            found_device = False
            for self.__usb_device in all_devices:
                try:
                    self.__usb_device.set_configuration()
                except core.USBError:
                    raise core.USBError("Could not configure the usb device in OceanOpticsDevice.find_usb_device()")
                # since this is USB the device name and ocean optics protocol are implied from the productID
                self.__ocean_optics_protocol = \
                    device_identity.get_ocean_optics_device_protocol(self.__usb_device.idProduct)
                self.__device_name = device_identity.get_ocean_optics_device_name(self.__usb_device.idProduct)
                self.set_product_id_and_usb_endpoints(self.__usb_device.idProduct)
                self.__serial_number = self.__introspection_methods.serial_number_get()
                if serial_number == self.__serial_number:
                    found_device = True
                    break
        except core.NoBackendError:
            raise RuntimeError("Error: libusb is probably not installed on the host machine.\n{0}", sys.exc_info()[0])
        return found_device

    def release(self):
        util.dispose_resources(self.__usb_device)

    def find_network_device(self, serial_number):
        print("find network device")

    def find_rs232_device(self, serial_number):
        print("find rs232 device")

    def find_i2c_device(self, serial_number):
        print("find i2c device")

    def find_spi_device(self, serial_number):
        print("find spi device")

    def find_all_devices(self):
        print("find all devices")
