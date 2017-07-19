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
    ReplaceConfigException,
    )

from utils.utils import read_txt_file, convert_uptime, convert_speed
from utils.parsers import parse_get_facts
from netmiko import ConnectHandler

import textfsm
import socket
import StringIO


class FastIronDriver(NetworkDriver):
    """Napalm driver for FastIron."""
    def __init__(self, hostname, username, password, timeout=60, optional_args=None):
        """Constructor."""
        self.hostname = hostname
        self.username = username
        self.password = password
        self.timeout = timeout
        self.config_replace = True
        self.device = None

        if optional_args is None:
            optional_args = {}

    def open(self):
        """Implementation of NAPALM method open."""
        self.device = ConnectHandler(device_type='brocade_fastiron',
                                     ip=self.hostname,
                                     username=self.username,
                                     password=self.password,
                                     verbose=False,
                                     use_keys=False,
                                     session_timeout=300)
        self.device.session_preparation()

    def close(self):
        """Implementation of NAPALM method close."""
        self.device.disconnect()

    def _send_command(self, command):
        """Wrapper for self.device.send.command().
        If command is a list will iterate through commands until valid command.
        """
        try:
            if isinstance(command, list):
                output = ""
                for cmd in command:
                    output = output + self.device.send_command(cmd)
                    # TODO Check exception handling
                    # if "% Invalid" not in output:
                    #     break
            else:
                output = self.device.send_command(command)
            return output
        except (socket.error, EOFError) as e:
            raise ConnectionException(str(e))

    def _show_version(self):
        output = self._send_command(['show version'])
        tplt = read_txt_file("napalm_brocade_fastiron/utils/textfsm_templates/fastiron_show_version.template")
        t = textfsm.TextFSM(tplt)
        result = t.ParseText(output).pop()
        result = {"version": result[0],
                  "model": result[1],
                  "serial_no": result[2],
                  "uptime": convert_uptime(result[3], result[4], result[5], result[6])}
        return result

    # Napalm API

    def get_interfaces(self):
        """Returns a dictionary of dictionaries.
        The keys for the first dictionary will be the interfaces in the devices. """
        interfaces = {}
        output = self._send_command(['show interfaces'])
        tplt = read_txt_file("napalm_brocade_fastiron/utils/textfsm_templates/fastiron_show_interfaces.template")
        t = textfsm.TextFSM(tplt)
        result = t.ParseText(output)
        if result is not None:
            for i in result:
                entry = {
                    i[0] : {
                        "is_enabled":  True if i[1] == 'enabled' else False,
                        "is_up": True if i[2] == 'up' else False,
                        "mac_address": i[3],
                        "speed": 0 if i[4] == 'unknown' else convert_speed(i[4]),
                        "description": unicode(i[5]),
                        "last_flapped": convert_uptime(i[6], i[7], i[8], i[9]) # TODO Check
                        }
                }
                interfaces.update(entry)
        return interfaces

    def get_arp_table(self):
        table = []
        output = self._send_command(['show arp'])
        tplt = read_txt_file("napalm_brocade_fastiron/utils/textfsm_templates/fastiron_show_arp.template")
        t = textfsm.TextFSM(tplt)
        result = t.ParseText(output)
        if result is not None:
            for i in result:
                entry = {
                    "interface" : i[2],
                    "mac": i[1],
                    "ip": i[0],
                    "age": float(i[3])
                }
                table.append(entry)
        return table

    def get_config(self, retrieve='all'):
        configs = { 
                 'startup': "",
                 'running': "",
                 'candidate': ""}

        def parse_stream(stream, config):

            running_config_buffer = StringIO.StringIO()
            startup_config_buffer = StringIO.StringIO()

            stringbuffer = StringIO.StringIO(stream)
            startup = False

            for line in stringbuffer.readlines():
                # TODO what order do the commands have to be in?
                if 'Startup-config' in line:
                    if not startup:        
                        startup = True
                if startup:
                    startup_config_buffer.write(line)
                else:
                    running_config_buffer.write(line)

            config['running'] = unicode(running_config_buffer.getvalue())
            config['startup'] = unicode(startup_config_buffer.getvalue())
            config['candidate'] = unicode("")

            running_config_buffer.close()
            startup_config_buffer.close()
            
            return config

        if retrieve == 'all':
            command = ['show running-config', 'show config']
            output = self._send_command(command)
            configs = parse_stream(output, configs)

        if retrieve == 'startup':
            command = 'show config'
            output = self._send_command(command)
            configs['startup'] = unicode(output)
            
        if retrieve == 'running':
            command = 'show running-config'
            output = self._send_command(command)
            configs['running'] = unicode(output)
            
        return configs

    # TODO Handle Exception
    def commit_config(self):
        output = self._send_command(['write memory'])
        if not "Copy Done." in output:
            raise ValueError

    def _load_config(self, filename=None, config=None):
        return True, "bar"

    def load_replace_candidate(self, filename=None, config=None):
        """
        FastIron writes to the running configuration but is not commited until write mem
        """
        return_status = None
        msg = ""

        if filename and config:
            raise ValueError("Cannot simultaneously set source_file and source_config")

        if config:
            (return_status, msg) = self._load_config(config=config)
        elif filename:
            print("DEBUG: Source File {}".format(filename))
            (return_status, msg) = self._load_config(filename=filename)
            
        if not return_status:
            raise ReplaceConfigException(msg)

    # TODO finish interface list
    def get_facts(self):
        try:
            result = self._send_command(['show version'])
            interfaces = self.get_interfaces()
            facts = parse_get_facts(result)
        except:
            raise

        facts = {
                'hostname': "-".join((facts['model'], facts['os_version'])),
                'fqdn': "-".join((facts['model'], facts['os_version'])),
                'vendor': u'Brocade',
                'model': facts['model'],
                'serial_number': facts['serial_no'],
                'os_version': facts['os_version'],
                'uptime': facts['uptime'],
                'interface_list': interfaces.keys(),
            }

        return facts

    def is_alive(self):
        """Returns a flag with the state of the connection."""
        null = chr(0)
        try:
            # Try sending ASCII null byte to maintain
            #   the connection alive
            self.device.send_command(null)
        except (socket.error, EOFError):
            # If unable to send, we can tell for sure
            #   that the connection is unusable,
            #   hence return False.
            return {
                'is_alive': False
            }
        return {
            'is_alive': self.device.remote_conn.transport.is_active()
        }

