"""setup.py file."""

import uuid

from setuptools import setup, find_packages
from pip.req import parse_requirements

__author__ = 'Gary Berger <gberger@brocade.com>'

install_reqs = parse_requirements('requirements.txt', session=uuid.uuid1())
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name="napalm-brocade-fastiron",
    version="0.1.0",
    packages=find_packages(),
    author="Gary Berger",
    author_email="gberger@brocade.com",
    description="Network Automation Library for Brocade FastIron",
    classifiers=[
        'Topic :: Utilities',
         'Programming Language :: Python',
         'Programming Language :: Python :: 2',
         'Programming Language :: Python :: 2.7',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
    ],
    url="https://github.com/gaberger/test",
    include_package_data=True,
    install_requires=reqs,
)
