# Copyright 2017 Brocade Communications. All rights reserved.
#
# The contents of this file are licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

"""
Tests for FastIronDriver that can test both against a mocked and real device.
"""

import re
import unittest

import mock
#from napalm_base.exceptions import (CommandErrorException, ConnectionException,
#                                    MergeConfigException,
#                                    ReplaceConfigException,
#                                    SessionLockedException)

from netmiko import NetMikoTimeoutException

import napalm_brocade_fastiron.fastiron
from napalm_brocade_fastiron.utils.utils import read_txt_file


def send_command(command):
    """Wrapper for self.device.send.command().
    If command is a list will iterate through commands until valid command.
    """
    try:
        if isinstance(command, list):
            for cmd in command:
                cmd = re.sub(r'[\[\]\*\^\+\s\|]', '_', cmd)
                output = read_txt_file("test/unit/fastiron/mock_data/{}.txt".format(cmd)).read()
                return output
        else:
            cmd = re.sub(r'[\[\]\*\^\+\s\|]', '_', command)
            output = read_txt_file("test/unit/fastiron/mock_data/{}.txt".format(cmd)).read()
        return output
    except:
        raise


# ### Test Functions: fn's to be shared between test frameworks ###

def test_show_version(test_obj, device, exp_result):
    """Tests expections FastIronDriver.show_version()"""
    result = device.show_version()
    result.pop('uptime', None)
    test_obj.assertEqual(result, exp_result)

def test_show_interfaces(test_obj, device, exp_result):
    """Tests mocked expections of FastIronDriver.show_interfaces()"""
    result = device.show_interfaces()[0]
    result.pop('uptime', None)
    test_obj.assertEqual(result, exp_result)


### Mock Tests ###

class TestGetterFastIronDriverMock(unittest.TestCase):
    """Test Case for FastIronDriver using mock endpoints"""

    ### Test helper methods

    def setUp(self):
        ipaddr = "10.21.237.131"
        user = "test"
        password = "test"

        self.vendor = 'brocade_fastiron'
        try:
            self.device = napalm_brocade_fastiron.fastiron.FastIronDriver(ipaddr, user, password)
        except NetMikoTimeoutException:
             self.fail('Network Timeout Error:')
        except:
            raise 


        patch_target = 'napalm_brocade_fastiron.fastiron.FastIronDriver.send_command'
        self.send_command_patcher = mock.patch(patch_target,
                                               side_effect=send_command)
        self.send_command_patcher.start()

    def tearDown(self):
        self.send_command_patcher.stop()

    ### Tests

    def test_show_version_mock(self):
        """Tests mocked expections of FastIronDriver.show_version()"""
        exp_res =  {'model': 'ICX7450-48', 'version': '08.0.40bbT211', 'serial_no': 'CYX3318M0Y1'}
        test_show_version(self, self.device, exp_res)

    def test_show_interfaces_mock(self):
        """Tests mocked expections of FastIronDriver.show_interfaces()"""
        exp_res = {'oper': 'down', 'description': 'to196PC', 'admin': 'disabled', 'link_addr': '609c.9f31.b160', 'speed': 'unknown', 'name': 'GigabitEthernet1/1/1'}
        test_show_interfaces(self, self.device, exp_res)


### Device tests

class TestGetterFastIronDriverDevice(unittest.TestCase):
    """Test Case for FastIronDriver using real device endpoint"""

    def setUp(self):
        ipaddr = "10.21.237.131"
        user = "test"
        password = "test"

        self.vendor = 'brocade_fastiron'
        self.device = napalm_brocade_fastiron.fastiron.FastIronDriver(ipaddr, user, password)
        
        try:
            self.device.open()
        except NetMikoTimeoutException:
             self.fail('Network Timeout Error:')
        except:
             raise

    def test_show_version_device(self):
        """Tests FastIronDriver.show_version() on real device"""
        exp_res = {'model': u'ICX7450-48', 'version': u'08.0.40bbT211', 'serial_no': u'CYX3318M0Y1'}
        test_show_version(self, self.device, exp_res)
    
    def test_show_interfaces_device(self):
        """Tests FastIronDriver.show_interfaces() on real device"""
        exp_res = {'oper': u'down', 'description': u'to196PC', 'admin': u'disabled', 'link_addr': u'609c.9f31.b160', 'speed': u'unknown', 'name': u'GigabitEthernet1/1/1'}
        test_show_interfaces(self, self.device, exp_res)


# Make suites available

MOCK_SUITE = unittest.TestLoader()
MOCK_SUITE = MOCK_SUITE.loadTestsFromTestCase(TestGetterFastIronDriverMock)

DEVICE_SUITE = unittest.TestLoader()
DEVICE_SUITE = DEVICE_SUITE.loadTestsFromTestCase(TestGetterFastIronDriverDevice)
