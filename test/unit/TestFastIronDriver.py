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
    result = device.show_version()
    result.pop('uptime', None)
    test_obj.assertEqual(result, exp_result)

def test_show_interfaces(test_obj, device, exp_result):
    """Tests mocked expections of FastIronDriver.show_interfaces()"""
    result = device.show_interfaces()
    interface = result[0]
    interface.pop('uptime', None)
    test_obj.assertEqual(interface, exp_result)



# Napalm API

def test_get_config(test_obj, device, exp_result):
    """Tests mocked expections of FastIronDriver.show_interfaces()"""
    result = device.get_config()
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

    def test_get_config_mock(self):
        """Tests mocked expections of FastIronDriver.show_config()"""
        exp_res = {'running': "Current configuration:\n!\nver 08.0.40bbT211\n!\nstack unit 1\n  module 1 icx7450-48-port-management-module\n  module 2 icx7400-xgf-4port-40g-module\n  module 3 icx7400-qsfp-1port-40g-module\n  module 4 icx7400-qsfp-1port-40g-module\n!\n!\n!\n!\n!\nvlan 1 name DEFAULT-VLAN by port\n!\nvlan 4 by port\n untagged ethe 1/1/10\n!\nvlan 300 by port\n untagged ethe 1/1/13\n!\nvlan 2001 by port\n untagged ethe 1/1/11\n!\n!\n!\n!\nauthentication\n critical-vlan 2001\n auth-default-vlan 4\n restricted-vlan 300\n re-authentication\n reauth-period 120\n pass-through lldp\n dot1x enable\n dot1x enable ethe 1/1/1\n dot1x max-req 3\n dot1x timeout quiet-period 15\n dot1x timeout supplicant 2\n!\naaa authentication enable default local\naaa authentication dot1x default radius\naaa authentication login default local\naaa accounting dot1x default start-stop radius\nip address 10.21.237.131 255.255.255.128\nno ip dhcp-client enable\nip default-gateway 10.21.237.129\n!\nlogging console\nusername test password .....\nusername admin password .....\nradius-server host 10.21.240.42 auth-port 1812 acct-port 1813 default key 0 config123\n!\n!\nclock summer-time\nclock timezone us Pacific\ninterface ethernet 1/1/1\n dot1x port-control auto\n port-name to196PC\n disable\n!\n!\n!\n!\n!\n!\n!\n!\nalias cd=clear dot1x sessions\nalias sd=show dot1x sess all\n!\nlocal-userdb ssh\n username brocade password $e$)9-C*U%G'K5\n username admin password $e$)J5A,5b+\n username poc password $e$%Za7B%\n!\nend!\n", 'startup': "Startup-config data location is flash memory\n!\nStartup configuration:\n!\nver 08.0.40bbT211\n!\nstack unit 1\n  module 1 icx7450-48-port-management-module\n  module 2 icx7400-xgf-4port-40g-module\n  module 3 icx7400-qsfp-1port-40g-module\n  module 4 icx7400-qsfp-1port-40g-module\n!\n!\n!\n!\n!\nvlan 1 name DEFAULT-VLAN by port\n!\nvlan 4 by port\n untagged ethe 1/1/10\n!\nvlan 300 by port\n untagged ethe 1/1/13\n!\nvlan 2001 by port\n untagged ethe 1/1/11\n!\n!\n!\n!\nauthentication\n critical-vlan 2001\n auth-default-vlan 4\n restricted-vlan 300\n re-authentication\n reauth-period 120\n pass-through lldp\n dot1x enable\n dot1x enable ethe 1/1/1\n dot1x max-req 3\n dot1x timeout quiet-period 15\n dot1x timeout supplicant 2\n!\naaa authentication enable default local\naaa authentication dot1x default radius\naaa accounting dot1x default start-stop radius\nip address 10.21.237.131 255.255.255.128\nno ip dhcp-client enable\nip default-gateway 10.21.237.129\n!\nlogging console\nusername test password .....\nusername admin password .....\nradius-server host 10.21.240.42 auth-port 1812 acct-port 1813 default key 0 config123\n!\n!\nclock summer-time\nclock timezone us Pacific\ninterface ethernet 1/1/1\n dot1x port-control auto\n port-name to196PC\n disable\n!\n!\n!\n!\n!\n!\n!\n!\nalias cd=clear dot1x sessions\nalias sd=show dot1x sess all\n!\nlocal-userdb ssh\n username brocade password $e$)9-C*U%G'K5\n username admin password $e$)J5A,5b+\n username poc password $e$%Za7B%\n!\nend", 'candidate': ''}
        test_get_config(self, self.device, exp_res)


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
        """Tests mocked expections of FastIronDriver.show_config()"""
        exp_res = {'candidate': '',
                   'running': u"Current configuration:\n!\nver 08.0.40bbT211\n!\nstack unit 1\n  module 1 icx7450-48-port-management-module\n  module 2 icx7400-xgf-4port-40g-module\n  module 3 icx7400-qsfp-1port-40g-module\n  module 4 icx7400-qsfp-1port-40g-module\n!\n!\n!\n!\n!\nvlan 1 name DEFAULT-VLAN by port\n!\nvlan 4 by port\n untagged ethe 1/1/10 \n!\nvlan 300 by port\n untagged ethe 1/1/13 \n!\nvlan 2001 by port\n untagged ethe 1/1/11 \n!\n!\n!\n!\nauthentication\n critical-vlan 2001\n auth-default-vlan 4\n restricted-vlan 300\n re-authentication\n reauth-period 120\n pass-through lldp\n dot1x enable\n dot1x enable ethe 1/1/1 \n dot1x max-req 3\n dot1x timeout quiet-period 15\n dot1x timeout supplicant 2\n!\naaa authentication enable default local\naaa authentication dot1x default radius\naaa authentication login default local\naaa accounting dot1x default start-stop radius\nip address 10.21.237.131 255.255.255.128\nno ip dhcp-client enable\nip default-gateway 10.21.237.129\n!\nlogging console\nusername test password .....\nusername admin password .....\nradius-server host 10.21.240.42 auth-port 1812 acct-port 1813 default key 0 config123\n!\n!\nclock summer-time\nclock timezone us Pacific\ninterface ethernet 1/1/1\n dot1x port-control auto\n port-name to196PC\n disable\n!\n!\n!\n!\n!\n!\n!\n!\nalias cd=clear dot1x sessions \nalias sd=show dot1x sess all\n!\nlocal-userdb ssh\n username brocade password $e$)9-C*U%G'K5\n username admin password $e$)J5A,5b+\n username poc password $e$%Za7B%\n!\nend!\n",
                   'startup': u"Startup-config data location is flash memory\n!\nStartup configuration:\n!\nver 08.0.40bbT211\n!\nstack unit 1\n  module 1 icx7450-48-port-management-module\n  module 2 icx7400-xgf-4port-40g-module\n  module 3 icx7400-qsfp-1port-40g-module\n  module 4 icx7400-qsfp-1port-40g-module\n!\n!\n!\n!\n!\nvlan 1 name DEFAULT-VLAN by port\n!\nvlan 4 by port\n untagged ethe 1/1/10 \n!\nvlan 300 by port\n untagged ethe 1/1/13 \n!\nvlan 2001 by port\n untagged ethe 1/1/11 \n!\n!\n!\n!\nauthentication\n critical-vlan 2001\n auth-default-vlan 4\n restricted-vlan 300\n re-authentication\n reauth-period 120\n pass-through lldp\n dot1x enable\n dot1x enable ethe 1/1/1 \n dot1x max-req 3\n dot1x timeout quiet-period 15\n dot1x timeout supplicant 2\n!\naaa authentication enable default local\naaa authentication dot1x default radius\naaa accounting dot1x default start-stop radius\nip address 10.21.237.131 255.255.255.128\nno ip dhcp-client enable\nip default-gateway 10.21.237.129\n!\nlogging console\nusername test password .....\nusername admin password .....\nradius-server host 10.21.240.42 auth-port 1812 acct-port 1813 default key 0 config123\n!\n!\nclock summer-time\nclock timezone us Pacific\ninterface ethernet 1/1/1\n dot1x port-control auto\n port-name to196PC\n disable\n!\n!\n!\n!\n!\n!\n!\n!\nalias cd=clear dot1x sessions \nalias sd=show dot1x sess all\n!\nlocal-userdb ssh\n username brocade password $e$)9-C*U%G'K5\n username admin password $e$)J5A,5b+\n username poc password $e$%Za7B%\n!\nend"}
        test_get_config(self, self.device, exp_res)


# Make suites available

MOCK_SUITE = unittest.TestLoader()
MOCK_SUITE = MOCK_SUITE.loadTestsFromTestCase(TestGetterFastIronDriverMock)

DEVICE_SUITE = unittest.TestLoader()
DEVICE_SUITE = DEVICE_SUITE.loadTestsFromTestCase(TestGetterFastIronDriverDevice)
