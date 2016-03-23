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

import mock
import unittest2 as unittest

from acos_client.v30.license_manager import LicenseManager

URL_BASE = "/axapi/v3/license-manager"


class TestLicenseManager(unittest.TestCase):
    def setUp(self):
        self.client = mock.Mock()
        self.target = LicenseManager(self.client)

    def _untested(self):
        raise NotImplementedError("This needs actual test code")

    def _test_create(self, hosts, serial, payload):
        self.target.create(hosts, serial)
        ((method, url, params, header), kwargs) = self.client.http.request.call_args
        self.assertEqual("POST", method)
        self.assertEqual(URL_BASE, url)
        self.assertEqual(payload, params)
        return {"method": method, "url": url, "params": params, "header": header, "kwargs": kwargs}

    def test_create(self):
        hosts = [{"ip": "127.0.0.1", "port": 443}]
        serial = "sn1234567890"

        payload = self.target._build_payload(hosts, serial)

        self._test_create(hosts, serial, payload)

    def test_create_multihosts(self):
        hosts = [{"ip": "127.0.0.1", "port": 443},
                 {"ip": "127.0.0.2", "port": 443}]
        serial = "sn1234567890"

        payload = self.target._build_payload(hosts, serial)

        self._test_create(hosts, serial, payload)

    def test_create_use_mgmt_port(self):
        hosts = [{"ip": "127.0.0.1", "port": 443}]
        serial = "sn1234567890"
        expected = False
        payload = self.target._build_payload(hosts, serial, use_mgmt_port=expected)

        result = self._test_create(hosts, serial, payload)

        actual = result["params"]["license-manager"]["use-mgmt-port"]
        self.assertEqual(expected, actual)

    def test_create_serial(self):
        hosts = [{"ip": "127.0.0.1", "port": 443}]
        serial = "sn1234567890"

        payload = self.target._build_payload(hosts, serial)

        result = self._test_create(hosts, serial, payload)

        actual = result["params"]["license-manager"]["sn"]
        self.assertEqual(serial, actual)

    def test_get(self):
        self.target.get()
        ((method, url, params, header), kwargs) = self.client.http.request.call_args
        self.assertEqual("GET", method)
        self.assertEqual(URL_BASE, url)

    def test_connect_positive(self):
        self._test_connect(True)

    def test_connect_false(self):
        self._test_connect(False)

    def _test_connect(self, connect):
        self.target.connect(connect)

        payload = {
            "connect": {
                "connect": 1 if connect else 0
            }
        }

        ((method, url, params, header), kwargs) = self.client.http.request.call_args
        self.assertEqual("POST", method)
        self.assertEqual(URL_BASE + "/connect", url)
        self.assertEqual(params, payload)

    def test_update(self):
        hosts = [{"ip": "127.0.0.2", "port": 443}]
        serial = "sn1234567890"

        payload = self.target._build_payload(hosts, serial)
        self.target.create(hosts, serial)
        ((method, url, params, header), kwargs) = self.client.http.request.call_args
        self.assertEqual("POST", method)
        self.assertEqual(URL_BASE, url)
        self.assertEqual(payload, params)
        return {"method": method, "url": url, "params": params, "header": header, "kwargs": kwargs}
