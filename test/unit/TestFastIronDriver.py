# Copyright 2016 Dravetech AB. All rights reserved.
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

"""Tests."""

import unittest
import re
import difflib
import mock
from napalm_base import exceptions
from napalm_base.test import models

from napalm_brocade_fastiron import fastiron
# from napalm_base.test.base import TestConfigNetworkDriver
import json
from unittest import SkipTest
from napalm_base.utils import py23_compat
from napalm_brocade_fastiron.utils.utils import read_txt_file


def _send_command(command):
    """Wrapper for self.device.send.command().
    If command is a list will iterate through commands until valid command.
    """
    output = ""

    try:
        if isinstance(command, list):
            for cmd in command:
                # output = self.session.send_command(cmd)
                cmd = re.sub(r'[\[\]\*\^\+\s\|]', '_', cmd)
                output = output + \
                    read_txt_file(
                        "test/unit/fastiron/mock_data/{}.txt".format(cmd)).read()
                #         return py23_compat.text_type(output)

        else:
            cmd = re.sub(r'[\[\]\*\^\+\s\|]', '_', command)
            output = read_txt_file(
                "test/unit/fastiron/mock_data/{}.txt".format(cmd)).read()
        return output
    except:
        raise





class TestConfigDriver(unittest.TestCase):
    """Group of tests that test Configuration related methods."""

    def send_command(command):
        return _send_command(command)

    @classmethod
    def setUpClass(cls):
        cls.mock = False

        ipaddr = "10.21.237.131"
        user = "admin"
        password = "admin"
        secret = "test"

        cls.vendor = 'test/unit/fastiron'
        cls.device = fastiron.FastIronDriver(ipaddr, user, password)
        if not cls.mock:
            cls.device.open()

    @staticmethod
    def read_file(filename):
        with open(filename, 'r') as f:
            return f.read().strip()

    @staticmethod
    def print_diff_strings(orig, new):
        for line in difflib.context_diff(orig.splitlines(), new.splitlines()):
            print(line)
    #
    # @mock.patch('napalm_brocade_fastiron.fastiron.FastIronDriver._send_command', side_effect=send_command)
    # def test_replacing_and_committing_config(self, mock):
    #     try:
    #         self.device.load_replace_candidate(filename='%s/new_good.conf' % self.vendor)
    #         self.device.commit_config()
    #     except NotImplementedError:
    #         raise SkipTest()
    #
    #     # The diff should be empty as the configuration has been committed already
    #     diff = self.device.compare_config()
    #
    #     # Reverting changes
    #     self.device.load_replace_candidate(filename='%s/initial.conf' % self.vendor)
    #     self.device.commit_config()
    #
    #     self.assertEqual(len(diff), 0)
    #
    # @mock.patch('napalm_brocade_fastiron.fastiron.FastIronDriver._send_command', side_effect=send_command)
    # def test_replacing_config_with_typo(self, mock):
    #     result = False
    #     try:
    #         self.device.load_replace_candidate(filename='%s/new_typo.conf' % self.vendor)
    #         self.device.commit_config()
    #     except NotImplementedError:
    #         raise SkipTest()
    #     except exceptions.ReplaceConfigException:
    #         self.device.load_replace_candidate(filename='%s/initial.conf' % self.vendor)
    #         diff = self.device.compare_config()
    #         self.device.discard_config()
    #         result = True and len(diff) == 0
    #     self.assertTrue(result)
    #
    # @mock.patch('napalm_brocade_fastiron.fastiron.FastIronDriver._send_command', side_effect=send_command)
    # def test_replacing_config_and_diff_and_discard(self, mock):
    #     intended_diff = self.read_file('%s/new_good.diff' % self.vendor)
    #
    #     self.device.load_replace_candidate(filename='%s/new_good.conf' % self.vendor)
    #     commit_diff = self.device.compare_config()
    #
    #     print(commit_diff)
    #
    #     self.device.discard_config()
    #     discard_diff = self.device.compare_config()
    #     self.device.discard_config()
    #
    #     result = (commit_diff == intended_diff) and (discard_diff == '')
    #     self.assertTrue(result)
    #
    # @mock.patch('napalm_brocade_fastiron.fastiron.FastIronDriver._send_command', side_effect=send_command)
    # def test_replacing_config_and_rollback(self, mock):
    #     self.device.load_replace_candidate(filename='%s/new_good.conf' % self.vendor)
    #     orig_diff = self.device.compare_config()
    #     self.device.commit_config()
    #
    #     # Now we rollback changes
    #     replace_config_diff = self.device.compare_config()
    #     self.device.rollback()
    #
    #     # We try to load the config again. If the rollback was successful new diff should be
    #     # like the first one
    #     self.device.load_replace_candidate(filename='%s/new_good.conf' % self.vendor)
    #     last_diff = self.device.compare_config()
    #     self.device.discard_config()
    #
    #     result = (orig_diff == last_diff) and (len(replace_config_diff) == 0)
    #
    #     self.assertTrue(result)
    #
    # @mock.patch('napalm_brocade_fastiron.fastiron.FastIronDriver._send_command', side_effect=send_command)
    # def test_merge_configuration(self, mock):
    #     intended_diff = self.read_file('%s/merge_good.diff' % self.vendor)
    #
    #     self.device.load_merge_candidate(filename='%s/merge_good.conf' % self.vendor)
    #     self.device.commit_config()
    #
    #     # Reverting changes
    #     self.device.load_replace_candidate(filename='%s/initial.conf' % self.vendor)
    #     diff = self.device.compare_config()
    #
    #     print(diff)
    #
    #     self.device.commit_config()
    #
    #     self.assertEqual(diff, intended_diff)
    #
    # @mock.patch('napalm_brocade_fastiron.fastiron.FastIronDriver._send_command', side_effect=send_command)
    # def test_merge_configuration_typo_and_rollback(self, mock):
    #     result = False
    #     try:
    #         self.device.load_merge_candidate(filename='%s/merge_typo.conf' % self.vendor)
    #         self.device.compare_config()
    #         self.device.commit_config()
    #         raise Exception("We shouldn't be here")
    #     except exceptions.MergeConfigException:
    #         # We load the original config as candidate. If the commit failed cleanly the
    #         # compare_config should be empty
    #         self.device.load_replace_candidate(filename='%s/initial.conf' % self.vendor)
    #         result = self.device.compare_config() == ''
    #         self.device.discard_config()
    #
    #     self.assertTrue(result)

    @mock.patch('napalm_brocade_fastiron.fastiron.FastIronDriver._send_command', side_effect=send_command)
    def test_load_template(self, mock):
        """Test load_template method."""
        result = self.device.load_template('set_hostname', hostname='my-hostname')
        print("DEBUG: {}".format(result))

        diff = self.device.compare_config()
        self.device.discard_config()
        self.assertFalse(diff is not '')


# class FakeDevice(fastiron.FastIronDriver):
#     """Test double."""
#
#     @staticmethod
#     def read_json_file(filename):
#         """Return the content of a file with content formatted as json."""
#         with open(filename) as data_file:
#             return json.load(data_file)
#
#     @staticmethod
#     def read_txt_file(filename):
#         """Return the content of a file."""
#         with open(filename) as data_file:
#             return data_file.read()
#
#     def send_command_expect(self, command, **kwargs):
#         """Fake execute a command in the device by just returning the content of a file."""
#         cmd = re.sub(r'[\[\]\*\^\+\s\|]', '_', command)
#         output = self.read_txt_file('test/unit/fastiron/mock_data/{}.txt'.format(cmd))
#         return py23_compat.text_type(output)
#
#     def send_command(self, command, **kwargs):
#         """Fake execute a command in the device by just returning the content of a file."""
#         return self.send_command_expect(command)
#
#     def disconnect(self, mock):
#         pass


if __name__ == '__main__':
    unittest.main()
