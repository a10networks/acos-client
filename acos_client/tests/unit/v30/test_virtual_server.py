# Copyright 2014-2016, A10 Networks.
#
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

import mock

import unittest2 as unittest

from acos_client import errors as acos_errors
from acos_client.v30.slb import virtual_server


EXPECTED_URL = '/axapi/v3/slb/virtual-server/'


class TestVirtualServer(unittest.TestCase):
    def setUp(self):
        self.client = mock.MagicMock()
        self.target = virtual_server.VirtualServer(self.client)
        self.target._get = mock.MagicMock(side_effect=acos_errors.NotFound)

    def test_arp_disable_positive(self):
        self._test_arp_disable(True)

    def test_arp_disable_negative(self):
        self._test_arp_disable(False)

    def _build_payload(self, arp_disable=False):
        return {'virtual-server': {'arp-disable': None if arp_disable is None else int(arp_disable),
                                   'name': 'virtualserver', 'ip-address': '127.0.0.1'}}

    def _test_arp_disable(self, arp_disable):
        self.target.create("virtualserver", "127.0.0.1",
                           arp_disable=arp_disable)
        call_source = self.client.http
        expected_payload = self._build_payload(arp_disable=arp_disable)
        call_source.request.assert_called_with('POST', EXPECTED_URL, expected_payload, mock.ANY)
