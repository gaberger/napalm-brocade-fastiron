import unittest

import os
import re
from netmiko import NetMikoTimeoutException, NetMikoAuthenticationException, py23_compat
from napalm_base.exceptions import ConnectionException, MergeConfigException, \
ReplaceConfigException, SessionLockedException, CommandErrorException

import napalm_brocade_fastiron.fastiron
# from napalm_base.test.base import TestConfigNetworkDriver, TestGettersNetworkDriver
from napalm_brocade_fastiron.utils import parsers as p

import mock
import textfsm

from napalm_brocade_fastiron.utils.utils import send_command, read_txt_file

def _send_command(command):
    
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
    #         return py23_compat.text_type(output)

            else:
                 cmd = re.sub(r'[\[\]\*\^\+\s\|]', '_', command)
                 output = read_txt_file("test/unit/fastiron/mock_data/{}.txt".format(cmd)).read()
            return output
        except:
            raise


class TestGetterFastIronDriver(unittest.TestCase):

    # Proxy for mocking
    def send_command(command):
        return _send_command(command)

    @classmethod
    def setUpClass(cls):
        cls.mock = True

        ipaddr = "10.21.237.131"
        user = "test"

        password = "test"
        secret = "test"

        cls.vendor = 'brocade_fastiron'
        cls.device = napalm_brocade_fastiron.fastiron.FastIronDriver(ipaddr, user, password)
        if not cls.mock:
            cls.device.open()
        
    @mock.patch('napalm_brocade_fastiron.fastiron.FastIronDriver.send_command', side_effect=send_command)
    def test_show_version(self, mock):
        result = self.device.show_version()
        self.assertEqual(result, [['08.0.40bbT211', 'ICX7450-48', 'CYX3318M0Y1', '6', '16', '35', '37']])

    @mock.patch('napalm_brocade_fastiron.fastiron.FastIronDriver.send_command', side_effect=send_command)
    def test_show_interfaces(self, mock):
        result = self.device.show_interfaces()
        self.assertEqual(result[0], ['GigabitEthernet1/1/1', 'disabled', 'down', '5', '17', '53', '9', '609c.9f31.b160', 'unknown', 'to196PC'])

    # def test_show_version(self):
    #     result = self.device.show_version()
    #     # TODO Fix this because the uptime results are dynamic.
    #     self.assertEqual(result,[[u'08.0.40bbT211', u'ICX7450-48', u'CYX3318M0Y1', u'6', u'16', u'38', u'2']])
    # TODO FIX THIS
    # def test_show_interfaces(self):
    #     result = self.device.show_interfaces()
    #     self.assertEqual(result[0], "")

if __name__ == '__main__':
    unittest.main()

