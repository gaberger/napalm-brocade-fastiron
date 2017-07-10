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
from napalm_base.test.base import TestConfigNetworkDriver


def _send_command(command):
    """Wrapper for self.device.send.command().
    If command is a list will iterate through commands until valid command.
    """
    try:
        if isinstance(command, list):
            output = ""
            for cmd in command:
                cmd = re.sub(r'[\[\]\*\^\+\s\|]', '_', cmd)
                output = output + read_txt_file("test/unit/fastiron/mock_data/{}.txt".format(cmd)).read()
        else:
            cmd = re.sub(r'[\[\]\*\^\+\s\|]', '_', command)
            output = read_txt_file("test/unit/fastiron/mock_data/{}.txt".format(cmd)).read()
        return output
    except:
        raise


# ### Test Functions: fn's to be shared between test frameworks ###

def test_show_version(test_obj, device, exp_result):
    """Tests expections FastIronDriver.show_version()"""
    result = device._show_version()
    result.pop('uptime', None)
    test_obj.assertEqual(result, exp_result)

def test_get_interfaces(test_obj, device, exp_result):
    """Tests mocked expections of FastIronDriver.show_interfaces()"""
    interface = {}
    result = device.get_interfaces()
    assert len(result) > 0



# Napalm API

def test_get_config(test_obj, device, exp_result):
    """Tests mocked expections of FastIronDriver.show_interfaces()"""
    result = device.get_config(retrieve='all')
    test_obj.assertEqual(result, exp_result)

def test_get_facts(test_obj, device, exp_result):
    """Tests mocked expections of FastIronDriver.show_interfaces()"""
    result = device.get_facts()
    test_obj.assertEqual(result, exp_result)

def test_get_arp(test_obj, device, exp_result):
    """Tests mocked expections of FastIronDriver.get_arp_table()"""
    result = device.get_arp_table()
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


        patch_target = 'napalm_brocade_fastiron.fastiron.FastIronDriver._send_command'
        self.send_command_patcher = mock.patch(patch_target,
                                               side_effect=_send_command)
        self.send_command_patcher.start()

    def tearDown(self):
        self.send_command_patcher.stop()

    ### Tests

    def test_show_version_mock(self):
        """Tests mocked expections of FastIronDriver.show_version()"""
        exp_res =  {'model': 'ICX7450-48', 'version': '08.0.40bbT211', 'serial_no': 'CYX3318M0Y1'}
        test_show_version(self, self.device, exp_res)

    def test_get_interfaces_mock(self):
        """Tests mocked expections of FastIronDriver.show_interfaces()"""
        exp_res = {'oper': 'down', 'description': 'to196PC', 'admin': 'disabled', 'link_addr': '609c.9f31.b160', 'speed': 'unknown', 'name': 'GigabitEthernet1/1/1'}
        test_get_interfaces(self, self.device, exp_res)

    def test_get_config_mock(self):
        """Tests mocked expections of FastIronDriver.show_config()"""
        exp_res = {'running': "Current configuration:\n!\nver 08.0.40bbT211\n!\nstack unit 1\n  module 1 icx7450-48-port-management-module\n  module 2 icx7400-xgf-4port-40g-module\n  module 3 icx7400-qsfp-1port-40g-module\n  module 4 icx7400-qsfp-1port-40g-module\n!\n!\n!\n!\n!\nvlan 1 name DEFAULT-VLAN by port\n!\nvlan 4 by port\n untagged ethe 1/1/10\n!\nvlan 300 by port\n untagged ethe 1/1/13\n!\nvlan 2001 by port\n untagged ethe 1/1/11\n!\n!\n!\n!\nauthentication\n critical-vlan 2001\n auth-default-vlan 4\n restricted-vlan 300\n re-authentication\n reauth-period 120\n pass-through lldp\n dot1x enable\n dot1x enable ethe 1/1/1\n dot1x max-req 3\n dot1x timeout quiet-period 15\n dot1x timeout supplicant 2\n!\naaa authentication enable default local\naaa authentication dot1x default radius\naaa authentication login default local\naaa accounting dot1x default start-stop radius\nip address 10.21.237.131 255.255.255.128\nno ip dhcp-client enable\nip default-gateway 10.21.237.129\n!\nlogging console\nusername test password .....\nusername admin password .....\nradius-server host 10.21.240.42 auth-port 1812 acct-port 1813 default key 0 config123\n!\n!\nclock summer-time\nclock timezone us Pacific\ninterface ethernet 1/1/1\n dot1x port-control auto\n port-name to196PC\n disable\n!\n!\n!\n!\n!\n!\n!\n!\nalias cd=clear dot1x sessions\nalias sd=show dot1x sess all\n!\nlocal-userdb ssh\n username brocade password $e$)9-C*U%G'K5\n username admin password $e$)J5A,5b+\n username poc password $e$%Za7B%\n!\nend!\n", 'startup': "Startup-config data location is flash memory\n!\nStartup configuration:\n!\nver 08.0.40bbT211\n!\nstack unit 1\n  module 1 icx7450-48-port-management-module\n  module 2 icx7400-xgf-4port-40g-module\n  module 3 icx7400-qsfp-1port-40g-module\n  module 4 icx7400-qsfp-1port-40g-module\n!\n!\n!\n!\n!\nvlan 1 name DEFAULT-VLAN by port\n!\nvlan 4 by port\n untagged ethe 1/1/10\n!\nvlan 300 by port\n untagged ethe 1/1/13\n!\nvlan 2001 by port\n untagged ethe 1/1/11\n!\n!\n!\n!\nauthentication\n critical-vlan 2001\n auth-default-vlan 4\n restricted-vlan 300\n re-authentication\n reauth-period 120\n pass-through lldp\n dot1x enable\n dot1x enable ethe 1/1/1\n dot1x max-req 3\n dot1x timeout quiet-period 15\n dot1x timeout supplicant 2\n!\naaa authentication enable default local\naaa authentication dot1x default radius\naaa accounting dot1x default start-stop radius\nip address 10.21.237.131 255.255.255.128\nno ip dhcp-client enable\nip default-gateway 10.21.237.129\n!\nlogging console\nusername test password .....\nusername admin password .....\nradius-server host 10.21.240.42 auth-port 1812 acct-port 1813 default key 0 config123\n!\n!\nclock summer-time\nclock timezone us Pacific\ninterface ethernet 1/1/1\n dot1x port-control auto\n port-name to196PC\n disable\n!\n!\n!\n!\n!\n!\n!\n!\nalias cd=clear dot1x sessions\nalias sd=show dot1x sess all\n!\nlocal-userdb ssh\n username brocade password $e$)9-C*U%G'K5\n username admin password $e$)J5A,5b+\n username poc password $e$%Za7B%\n!\nend", 'candidate': ''}
        test_get_config(self, self.device, exp_res)

    def test_get_facts_mock(self):
        """Tests mocked expections of FastIronDriver.show_config()"""
        exp_res = {'os_version': '08.0.40bbT211', 'uptime': 578137, 'interface_list': ["40GigabitEthernet1/3/1", "GigabitEthernet1/1/48", "GigabitEthernet1/1/45", "GigabitEthernet1/1/44", "GigabitEthernet1/1/47", "GigabitEthernet1/1/46", "GigabitEthernet1/1/41", "GigabitEthernet1/1/40", "GigabitEthernet1/1/43", "GigabitEthernet1/1/42", "GigabitEthernet1/1/29", "GigabitEthernet1/1/28", "GigabitEthernet1/1/27", "GigabitEthernet1/1/26", "GigabitEthernet1/1/25", "GigabitEthernet1/1/24", "GigabitEthernet1/1/23", "GigabitEthernet1/1/22", "GigabitEthernet1/1/21", "GigabitEthernet1/1/20", "GigabitEthernet1/1/8", "GigabitEthernet1/1/9", "GigabitEthernet1/1/19", "GigabitEthernet1/1/32", "GigabitEthernet1/1/1", "GigabitEthernet1/1/2", "GigabitEthernet1/1/3", "GigabitEthernet1/1/4", "GigabitEthernet1/1/5", "GigabitEthernet1/1/6", "GigabitEthernet1/1/7", "GigEthernetmgmt1", "GigabitEthernet1/1/12", "GigabitEthernet1/1/13", "GigabitEthernet1/1/10", "GigabitEthernet1/1/11", "GigabitEthernet1/1/16", "GigabitEthernet1/1/17", "GigabitEthernet1/1/14", "GigabitEthernet1/1/15", "GigabitEthernet1/1/30", "GigabitEthernet1/1/31", "GigabitEthernet1/1/18", "GigabitEthernet1/1/33", "GigabitEthernet1/1/34", "GigabitEthernet1/1/35", "GigabitEthernet1/1/36", "GigabitEthernet1/1/37", "GigabitEthernet1/1/38", "GigabitEthernet1/1/39", "10GigabitEthernet1/2/4", "10GigabitEthernet1/2/2", "10GigabitEthernet1/2/3", "10GigabitEthernet1/2/1", "40GigabitEthernet1/4/1"], 'vendor': u'Brocade', 'serial_number': 'CYX3318M0Y1', 'model': 'ICX7450-48', 'hostname': 'ICX7450-48-08.0.40bbT211', 'fqdn': 'ICX7450-48-08.0.40bbT211'}
        test_get_facts(self, self.device, exp_res)

    def test_get_arp_mock(self):
        """Tests mocked expections of FastIronDriver.get_arp_table()"""
        exp_res = [{'interface': 'mgmt1', 'ip': '10.21.237.129', 'mac': '748e.f8d5.3d80', 'age': 0.0}, {'interface': 'mgmt1', 'ip': '10.21.237.128', 'mac': '748e.f8d5.3d81', 'age': 0.0}, {'interface': 'mgmt1', 'ip': '10.21.237.127', 'mac': '748e.f8d5.3d82', 'age': 0.0}, {'interface': 'mgmt1', 'ip': '10.21.237.126', 'mac': '748e.f8d5.3d83', 'age': 0.0}]
        test_get_arp(self, self.device, exp_res)


### Device tests

class TestGetterFastIronDriverDevice(unittest.TestCase):
    """Test Case for FastIronDriver using real device endpoint"""

    unittest.TestCase.maxDiff = None

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

    def test_get_config_device(self):
        """Tests expections of FastIronDriver.show_config()"""
        exp_res = {'candidate': '',
                   'running': u"Current configuration:\n!\nver 08.0.40bbT211\n!\nstack unit 1\n  module 1 icx7450-48-port-management-module\n  module 2 icx7400-xgf-4port-40g-module\n  module 3 icx7400-qsfp-1port-40g-module\n  module 4 icx7400-qsfp-1port-40g-module\n!\n!\n!\n!\n!\nvlan 1 name DEFAULT-VLAN by port\n!\nvlan 4 by port\n untagged ethe 1/1/10 \n!\nvlan 300 by port\n untagged ethe 1/1/13 \n!\nvlan 2001 by port\n untagged ethe 1/1/11 \n!\n!\n!\n!\nauthentication\n critical-vlan 2001\n auth-default-vlan 4\n restricted-vlan 300\n re-authentication\n reauth-period 120\n pass-through lldp\n dot1x enable\n dot1x enable ethe 1/1/1 \n dot1x max-req 3\n dot1x timeout quiet-period 15\n dot1x timeout supplicant 2\n!\naaa authentication enable default local\naaa authentication dot1x default radius\naaa authentication login default local\naaa accounting dot1x default start-stop radius\nip address 10.21.237.131 255.255.255.128\nno ip dhcp-client enable\nip default-gateway 10.21.237.129\n!\nlogging console\nusername test password .....\nusername admin password .....\nradius-server host 10.21.240.42 auth-port 1812 acct-port 1813 default key 0 config123\n!\n!\nclock summer-time\nclock timezone us Pacific\ninterface ethernet 1/1/1\n dot1x port-control auto\n port-name to196PC\n disable\n!\n!\n!\n!\n!\n!\n!\n!\nalias cd=clear dot1x sessions \nalias sd=show dot1x sess all\n!\nlocal-userdb ssh\n username brocade password $e$)9-C*U%G'K5\n username admin password $e$)J5A,5b+\n username poc password $e$%Za7B%\n!\nend!\n",
                   'startup': u"Startup-config data location is flash memory\n!\nStartup configuration:\n!\nver 08.0.40bbT211\n!\nstack unit 1\n  module 1 icx7450-48-port-management-module\n  module 2 icx7400-xgf-4port-40g-module\n  module 3 icx7400-qsfp-1port-40g-module\n  module 4 icx7400-qsfp-1port-40g-module\n!\n!\n!\n!\n!\nvlan 1 name DEFAULT-VLAN by port\n!\nvlan 4 by port\n untagged ethe 1/1/10 \n!\nvlan 300 by port\n untagged ethe 1/1/13 \n!\nvlan 2001 by port\n untagged ethe 1/1/11 \n!\n!\n!\n!\nauthentication\n critical-vlan 2001\n auth-default-vlan 4\n restricted-vlan 300\n re-authentication\n reauth-period 120\n pass-through lldp\n dot1x enable\n dot1x enable ethe 1/1/1 \n dot1x max-req 3\n dot1x timeout quiet-period 15\n dot1x timeout supplicant 2\n!\naaa authentication enable default local\naaa authentication dot1x default radius\naaa accounting dot1x default start-stop radius\nip address 10.21.237.131 255.255.255.128\nno ip dhcp-client enable\nip default-gateway 10.21.237.129\n!\nlogging console\nusername test password .....\nusername admin password .....\nradius-server host 10.21.240.42 auth-port 1812 acct-port 1813 default key 0 config123\n!\n!\nclock summer-time\nclock timezone us Pacific\ninterface ethernet 1/1/1\n dot1x port-control auto\n port-name to196PC\n disable\n!\n!\n!\n!\n!\n!\n!\n!\nalias cd=clear dot1x sessions \nalias sd=show dot1x sess all\n!\nlocal-userdb ssh\n username brocade password $e$)9-C*U%G'K5\n username admin password $e$)J5A,5b+\n username poc password $e$%Za7B%\n!\nend"}
        test_get_config(self, self.device, exp_res)



class TestConfigFastIronDriver(unittest.TestCase, TestConfigNetworkDriver):
    """Group of tests that test Configuration related methods."""

    @classmethod
    def setup_class(cls):
        """Run before starting the tests."""
        hostname = '127.0.0.1'
        username = 'vagrant'
        password = 'vagrant'
        cls.vendor = 'skeleton'

        optional_args = { }
        cls.device = napalm_brocade_fastiron.fastiron.FastIronDriver(hostname, username, password, timeout=60,
                                             optional_args=optional_args)
        # cls.device.open()

        cls.device.load_replace_candidate(filename='%s/initial.conf' % cls.vendor)
        cls.device.commit_config()


# Make suites available

MOCK_SUITE = unittest.TestLoader()
MOCK_SUITE = MOCK_SUITE.loadTestsFromTestCase(TestGetterFastIronDriverMock)

DEVICE_SUITE = unittest.TestLoader()
DEVICE_SUITE = DEVICE_SUITE.loadTestsFromTestCase(TestGetterFastIronDriverDevice)
