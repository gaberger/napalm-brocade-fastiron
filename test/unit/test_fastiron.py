"""
Tests for FastIronDriver that can test both against a mocked and real device.
"""

#import os
import re
import unittest

import mock
#import textfsm
#from napalm_base.exceptions import (CommandErrorException, ConnectionException,
#                                    MergeConfigException,
#                                    ReplaceConfigException,
#                                    SessionLockedException)
#from netmiko import (NetMikoAuthenticationException, NetMikoTimeoutException,
#                     py23_compat)

import napalm_brocade_fastiron.fastiron
#from napalm_brocade_fastiron.utils import parsers as p
from napalm_brocade_fastiron.utils.utils import read_txt_file


def send_command(command):
    """Wrapper for self.device.send.command().
    If command is a list will iterate through commands until valid command.
    """
    try:
        if isinstance(command, list):
            for cmd in command:
                # output = self.session.send_command(cmd)
                cmd = re.sub(r'[\[\]\*\^\+\s\|]', '_', cmd)
                output = read_txt_file("test/unit/fastiron/mock_data/{}.txt".format(cmd)).read()
                return output
                # return py23_compat.text_type(output)

        else:
            cmd = re.sub(r'[\[\]\*\^\+\s\|]', '_', command)
            output = read_txt_file("test/unit/fastiron/mock_data/{}.txt".format(cmd)).read()
        return output
    except:
        raise


### Test Functions: fn's to be shared between test frameworks ###

def test_show_verion(test_obj, device, exp_result):
    """Tests expections FastIronDriver.show_version()"""
    result = device.show_version()
    test_obj.assertEqual(result, exp_result)

def test_show_interfaces(test_obj, device, exp_result):
    """Tests mocked expections of FastIronDriver.show_interfaces()"""
    result = device.show_interfaces()
    test_obj.assertEqual(result[0], exp_result)


### Mock Tests ###

class TestGetterFastIronDriverMock(unittest.TestCase):
    """Test Case for FastIronDriver using mock endpoints"""

    ### Test helper methods

    def setUp(self):
        ipaddr = "10.21.237.131"
        user = "test"
        password = "test"
        #secret = "test"

        self.vendor = 'brocade_fastiron'
        self.device = napalm_brocade_fastiron.fastiron.FastIronDriver(ipaddr, user, password)

        patch_target = 'napalm_brocade_fastiron.fastiron.FastIronDriver.send_command'
        self.send_command_patcher = mock.patch(patch_target,
                                               side_effect=send_command)
        self.send_command_patcher.start()

    def tearDown(self):
        self.send_command_patcher.stop()

    ### Tests

    def test_show_version_mock(self):
        """Tests mocked expections of FastIronDriver.show_version()"""
        exp_res = [['08.0.40bbT211', 'ICX7450-48', 'CYX3318M0Y1', '6', '16', '35', '37']]
        test_show_verion(self, self.device, exp_res)

    def test_show_interfaces_mock(self):
        """Tests mocked expections of FastIronDriver.show_interfaces()"""
        exp_res = ['GigabitEthernet1/1/1', 'disabled', 'down', '5', '17', '53',
                   '9', '609c.9f31.b160', 'unknown', 'to196PC']
        test_show_interfaces(self, self.device, exp_res)


### Device tests

class TestGetterFastIronDriverDevice(unittest.TestCase):
    """Test Case for FastIronDriver using real device endpoint"""

    def setUp(self):
        ipaddr = "10.21.237.131"
        user = "test"

        password = "test"
        #secret = "test"

        self.vendor = 'brocade_fastiron'
        self.device = napalm_brocade_fastiron.fastiron.FastIronDriver(ipaddr, user, password)
        self.device.open()

    def test_show_version_device(self):
        """Tests FastIronDriver.show_version() on real device"""
        # TODO Fix this because the uptime results are dynamic.
        exp_res = [[u'08.0.40bbT211', u'ICX7450-48', u'CYX3318M0Y1', u'6', u'16', u'38', u'2']]
        test_show_verion(self, self.device, exp_res)
    # TODO FIX THIS

    def test_show_interfaces_device(self):
        """Tests FastIronDriver.show_interfaces() on real device"""
        exp_res = ""
        test_show_interfaces(self, self.device, exp_res)


# Make suites available

MOCK_SUITE = unittest.TestLoader()
MOCK_SUITE = MOCK_SUITE.loadTestsFromTestCase(TestGetterFastIronDriverMock)

DEVICE_SUITE = unittest.TestLoader()
DEVICE_SUITE = DEVICE_SUITE.loadTestsFromTestCase(TestGetterFastIronDriverDevice)
