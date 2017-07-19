"""Test fixtures."""
from builtins import super

import pytest
from napalm_base.test import conftest as parent_conftest
from napalm_base.utils import py23_compat

from napalm_base.test.double import BaseTestDouble

from napalm_brocade_fastiron import fastiron


@pytest.fixture(scope='class')
def set_device_parameters(request):
    """Set up the class."""
    def fin():
        request.cls.device.close()
    request.addfinalizer(fin)

    request.cls.driver = fastiron.FastIronDriver
    request.cls.patched_driver = PatchedFastIronDriver
    request.cls.vendor = 'fastiron'
    parent_conftest.set_device_parameters(request)


def pytest_generate_tests(metafunc):
    """Generate test cases dynamically."""
    parent_conftest.pytest_generate_tests(metafunc, __file__)

class PatchedFastIronDriver(fastiron.FastIronDriver):
    """Patched FastIron Driver."""

    def __init__(self, hostname, username, password, timeout=60, optional_args=None):
        """Patched Skeleton Driver constructor."""
        super().__init__(hostname, username, password, timeout, optional_args)

        self.patched_attrs = ['device']
        self.device = FakeFastIronDriver()

    def open(self):
        pass

    def is_alive(self):
        return {
            'is_alive': True  # In testing everything works..
        }

class FakeFastIronDriver(BaseTestDouble):
    """Skeleton device test double."""

    def run_commands(self, command_list, encoding='json'):
        """Fake run_commands."""
        result = list()

        for command in command_list:
            filename = '{}.{}'.format(self.sanitize_text(command), encoding)
            full_path = self.find_file(filename)

            if encoding == 'json':
                result.append(self.read_json_file(full_path))
            else:
                result.append({'output': self.read_txt_file(full_path)})

        return result

    def send_command(self, command, **kwargs):
        filename = '{}.txt'.format(self.sanitize_text(command))
        full_path = self.find_file(filename)
        result = self.read_txt_file(full_path)
        return py23_compat.text_type(result)

    def disconnect(self):
                pass
