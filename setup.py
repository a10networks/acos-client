#!/usr/bin/env python
# flake8: noqa

from setuptools import find_packages, setup
from os import path


setup(
    name = "acos-client",
    version = "2.2.0",
    packages = find_packages(),

    author = "A10 Networks",
    author_email = "opensource@a10networks.com",
    description = "A10 Networks ACOS API Client",
    license = "Apache",
    keywords = "a10 axapi acos adc slb load balancer",
    url = "https://github.com/a10networks/acos-client",

    long_description = open('README.md').read(),
    long_description_content_type = "text/markdown",

    classifiers = [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],

    install_requires = ['requests>=2.3.0', 'six', 'uhashring'],

    test_suite="acos_client.tests.test_suite"
)
