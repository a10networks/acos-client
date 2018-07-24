# Copyright (C) 2016, A10 Networks Inc. All rights reserved.

#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
from __future__ import absolute_import
from __future__ import unicode_literals

try:
    import unittest
    from unittest import mock
except ImportError:
    import mock
    import unittest2 as unittest

from acos_client.v30 import dns


class TestDns(unittest.TestCase):
    def setUp(self):
        self.client = mock.MagicMock()
        self.target = dns.DNS(self.client)
        self.url_prefix = "/axapi/v3/ip/dns/"

    def test_primary_ipv4(self):
        expected = '192.0.2.4'
        self.target.set(primary=expected)

        expected_payload = {'primary': {'ip-v4-addr': expected}}

        self.client.http.request.assert_called_with("POST", self.url_prefix + 'primary',
                                                    expected_payload, mock.ANY)

    def test_primary_ipv6(self):
        expected = '0:0:0:0:0:FFFF:129.144.52.38'
        self.target.set(primary=expected)

        expected_payload = {'primary': {'ip-v6-addr': expected}}

        self.client.http.request.assert_called_with("POST", self.url_prefix + 'primary',
                                                    expected_payload, mock.ANY)

    def test_secondary_ipv4(self):
        expected = '192.0.2.5'
        self.target.set(secondary=expected)

        expected_payload = {'secondary': {'ip-v4-addr': expected}}

        self.client.http.request.assert_called_with("POST", self.url_prefix + 'secondary',
                                                    expected_payload, mock.ANY)

    def test_secondary_ipv6(self):
        expected = '0:0:0:0:0:FFFF:129.144.52.39'
        self.target.set(secondary=expected)

        expected_payload = {'secondary': {'ip-v6-addr': expected}}

        self.client.http.request.assert_called_with("POST", self.url_prefix + 'secondary',
                                                    expected_payload, mock.ANY)

    def test_suffix(self):
        expected = 'example.com'
        self.target.set(suffix=expected)

        expected_payload = {'suffix': {'domain-name': expected}}

        self.client.http.request.assert_called_with("POST", self.url_prefix + 'suffix',
                                                    expected_payload, mock.ANY)
