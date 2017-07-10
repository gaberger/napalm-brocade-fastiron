"""Test fixtures."""
from builtins import super

import pytest
from napalm_base.test import conftest as parent_conftest

from napalm_base.test.double import BaseTestDouble
from napalm_base.utils import py23_compat

from napalm_brocade_fastiron import fastiron

@pytest.fixture(scope='class')
def set_device_parameters(request):
    """Set up the class."""
    def fin():
        request.cls.device.close()
    request.addfinalizer(fin)

    request.cls.driver = fastiron.FastIronDriver
    request.cls.patched_driver = PatchedFastIronDriver
    request.cls.vendor = 'brocade'
    parent_conftest.set_device_parameters(request)


def pytest_generate_tests(metafunc):
    """Generate test cases dynamically."""
    parent_conftest.pytest_generate_tests(metafunc, __file__)


class PatchedFastIronDriver(fastiron.FastIronDriver):
    """Patched FastIron Driver."""

    def __init__(self, hostname, username, password, timeout=60, optional_args=None):
        """Patched FastIron Driver constructor."""
        super().__init__(hostname, username, password, timeout, optional_args)

        self.patched_attrs = ['device']
        self.device = FakeNetIronDevice()

    def disconnect(self):
        pass
    
    def is_alive(self):
            return {
            'is_alive': True  # In testing everything works..
        }

    def open(self):
        pass

    # def send_command(self,command):
    #     """ Patched send_command  """
    #     try:
    #         result = list()
    #         if isinstance(command, list):
    #             for cmd in command:
    #                 filename = '{}.{}'.format(self.device.sanitize_text(cmd), "txt")
    #                 full_path = self.device.find_file(filename)
    #                 result.append({'output': self.device.read_txt_file(full_path)})
    #         else:
    #              filename = '{}.{}'.format(self.device.sanitize_text(command), "txt")
    #              full_path = self.device.find_file(filename)
    #              result.append({'output': self.device.read_txt_file(full_path)})
    #         return result
    #     except:
    #         raise

class FakeNetIronDevice(BaseTestDouble):
    """FastIron device test double."""

    # def send_command(command):
    #     """Wrapper for self.device.send.command().
    # If command is a list will iterate through commands until valid command.
    # """
    # try:
    #     if isinstance(command, list):
    #         output = ""
    #         for cmd in command:
    #             cmd = re.sub(r'[\[\]\*\^\+\s\|]', '_', cmd)
    #             output = output + read_txt_file("test/unit/fastiron/mock_data/{}.txt".format(cmd)).read()
    #     else:
    #         cmd = re.sub(r'[\[\]\*\^\+\s\|]', '_', command)
    #         output = read_txt_file("test/unit/fastiron/mock_data/{}.txt".format(cmd)).read()
    #     return output
    # except:
    #     raise

    # def send_command(self, command_list, encoding):
    #     """Fake run_commands."""
    #     result = list()

    #     for command in command_list:
    #         filename = '{}.{}'.format(self.sanitize_text(command), encoding)
    #         full_path = self.find_file(filename)

    #         if encoding == 'json':
    #             result.append(self.read_json_file(full_path))
    #         else:
    #             result.append({'output': self.read_txt_file(full_path)})

    #     return result

    # def send_command(self,command):
    #         """ Patched send_command  """
    #         try:
    #             result = list()
    #             if isinstance(command, list):
    #                 for cmd in command:
    #                     filename = '{}.{}'.format(self.sanitize_text(cmd), "txt")
    #                     full_path = self.find_file(filename)
    #                     result.append({'output': self.read_txt_file(full_path)})
    #             else:
    #                 filename = '{}.{}'.format(self.sanitize_text(command), "txt")
    #                 full_path = self.find_file(filename)
    #                 result.append({'output': self.read_txt_file(full_path)})
    #             return result
    #         except:
    #             raise

    def send_command(self, command, **kwargs):
        filename = '{}.txt'.format(self.sanitize_text(command))
        full_path = self.find_file(filename)
        result = self.read_txt_file(full_path)
        return py23_compat.text_type(result)
    
    def disconnect(self):
        pass