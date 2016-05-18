#!/usr/bin/env python
# flake8: noqa

from setuptools import setup, find_packages

setup(
    name = "acos-client",
    version = "1.3.4",
    packages = find_packages(),

    author = "A10 Networks",
    author_email = "dougw@a10networks.com",
    description = "A10 Networks ACOS API Client",
    license = "Apache",
    keywords = "a10 axapi acos adc slb load balancer",
    url = "https://github.com/a10networks/acos-client",

    long_description = open('README.md').read(),

    classifiers = [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],

    install_requires = ['hash_ring>=1.3.1', 'requests>=2.3.0']
)
