from napalm_base.exceptions import ConnectionException
from netmiko import BaseConnection
import re
import socket

import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

debug = True


class BrocadeFastironSSH(BaseConnection):
    """Brocade FastIron aka ICX support."""

    def __init__(self, ip, username, password, verbose, use_keys, session_timeout, port, device_type):
        """Subclassed here, needs PR to NetMiko when ready."""
        super(BrocadeFastironSSH, self).__init__(ip=ip, username=username, password=password, verbose=verbose)

    def session_preparation(self):
        """FastIron requires to be enable mode to disable paging."""
        self._test_channel_read()
        self.set_base_prompt()
        self.enable()
        self.disable_paging(command="skip-page-display")

    @staticmethod
    def normalize_linefeeds(a_string):
        """Convert '\r\n\r\n', '\r\r\n','\r\n', '\n\r' to '\n."""
        newline = re.compile(r'(\r\n\r\n|\r\r\n|\r\n|\n\r|\r)')
        return newline.sub('\n', a_string)

    def check_enable_mode(self, check_string='#'):
        """Check if in enable mode. Return boolean."""
        debug = False
        self.write_channel('\n')
        output = self.read_until_prompt()
        if debug:
            print(output)
        return check_string in output

    def check_telnet_auth(self):
        auth = False
        command = "show running"
        try:
            output = self.send_command(command)
            for line in output:
                if "enable telnet authentication" in line:
                    auth = True
            return auth
        except (socket.error, EOFError) as e:
            raise ConnectionException(str(e))

    def enable(self, cmd='enable', pattern='password', re_flags=""):
        """Deal with various enable control flow scenarios."""
        if not self.check_enable_mode():
            self.write_channel(self.normalize_cmd(cmd))
            self.read_until_pattern(pattern="User Name:")
            self.write_channel(self.normalize_cmd(self.username))
            self.read_until_pattern(pattern="Password:")
            self.write_channel(self.normalize_cmd(self.password))
            if not self.check_enable_mode():
                raise ValueError("Failed to enter enable mode.")
        else:
            self.write_channel(self.normalize_cmd(cmd))
            if not self.check_enable_mode():
                raise ValueError("Failed to enter enable mode.")
