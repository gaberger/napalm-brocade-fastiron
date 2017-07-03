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
Napalm driver for Brocade FastIron.

Read https://napalm.readthedocs.io for more information.
"""

from napalm_base.base import NetworkDriver
from napalm_base.exceptions import (
    ConnectionException,
    SessionLockedException,
    MergeConfigException,
    ReplaceConfigException,
    CommandErrorException,
    )

from utils.utils import read_txt_file

from netmiko import ConnectHandler
import textfsm
import socket

class FastIronDriver(NetworkDriver):
    """Napalm driver for FastIron."""
    def __init__(self, hostname, username, password, timeout=60, optional_args=None):
        """Constructor."""
        self.hostname = hostname
        self.username = username
        self.password = password
        self.timeout = timeout        

        if optional_args is None:
            optional_args = {}

    def open(self):
        """Implementation of NAPALM method open."""
        self.session = ConnectHandler(device_type = 'brocade_fastiron',
                                      ip =   self.hostname,
                                      username =  self.username,
                                      password = self.password,
                                      secret = "test",    
                                      verbose = True,
                                      use_keys = False,
                                      session_timeout = 300)
        self.session.session_preparation()
        
    def close(self):
        """Implementation of NAPALM method close."""
        self.session.disconnect()

    def send_command(self, command):
        """Wrapper for self.device.send.command().
        If command is a list will iterate through commands until valid command.
        """
        try:
            if isinstance(command, list):
                for cmd in command:
                    output = self.session.send_command(cmd)
                    # TODO Check exception handling
                    if "% Invalid" not in output:
                        break
            else:
                output = self.session.send_command(command)
            return output
        except (socket.error, EOFError) as e:
            raise ConnectionClosedException(str(e))

    def show_version(self):
        output = self.send_command(['show version'])
        tplt = read_txt_file("napalm_brocade_fastiron/utils/textfsm_templates/fastiron_show_version.template")
        t = textfsm.TextFSM(tplt)
        result = t.ParseText(output)
        return result

    def show_interfaces(self):
        output = self.send_command(['show interfaces'])
        tplt = read_txt_file("napalm_brocade_fastiron/utils/textfsm_templates/fastiron_show_interfaces.template")
        t = textfsm.TextFSM(tplt)
        result = t.ParseText(output)
        return result


    def get_facts(self):
            commands = []
            commands.append('show version')

            try:
                result = self.send_command(commands)
                print(result)
                facts = p.parse_get_facts(result)
            except:
                raise

            return {
                    'hostname': "-".join((facts['model'], facts['os_version'])),
                    'fqdn': "-".join((facts['model'], facts['os_version'])),
                    'vendor': u'Brocade',
                    'model': facts['model'],
                    'serial_number': facts['serial_no'],
                    'os_version': facts['os_version'],
                    'uptime': facts['uptime'],
                    # 'interface_list': interfaces,
                }

            return sv


    