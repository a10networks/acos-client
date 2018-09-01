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

from __future__ import absolute_import, unicode_literals

from acos_client import client

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestClient(unittest.TestCase):

    def setUp(self):
        self.client_21 = client.Client('fake-host', '2.1', 'fake-username', 'fake-password', max_retries=5, timeout=3)
        self.client_30 = client.Client('fake-host', '3.0', 'fake-username', 'fake-password', max_retries=6, timeout=4)

    def test_dns_v21(self):
        from acos_client.v21.dns import DNS

        self.assertIsInstance(self.client_21.dns, DNS)

    def test_dns_v30(self):
        from acos_client.v30.dns import DNS

        self.assertIsInstance(self.client_30.dns, DNS)

    def test_max_retries_v21(self):

        self.assertEqual(self.client_21.max_retries, 5)
        self.assertEqual(self.client_21.timeout, 3)
        self.assertEqual(self.client_21.http.max_retries, 5)
        self.assertEqual(self.client_21.http.timeout, 3)

    def test_max_retries_v30(self):

        self.assertEqual(self.client_30.max_retries, 6)
        self.assertEqual(self.client_30.timeout, 4)
        self.assertEqual(self.client_30.http.max_retries, 6)
        self.assertEqual(self.client_30.http.timeout, 4)
