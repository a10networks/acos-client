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

from acos_client.v30.slb import port


class TestPort(unittest.TestCase):
    def setUp(self):
        self.client = mock.MagicMock()
        self.port = port.Port(self.client)

        # common test parameter(s) throughout all test-cases
        self._server_name = 'test_server'

    def test_create_port(self):
        expected = {
            'port': {
                "conn-resume": None,
                "conn-limit": 8000000,
                "stats-data-action": "stats-data-enable",
                "weight": 1,
                "port-number": 80,
                "range": 0,
                "action": "enable",
                "protocol": 'tcp'
            }
        }
        self.port.create('test_server', 80, 'tcp')

        ((method, url, params, header), kwargs) = self.client.http.request.call_args

        self.assertEqual(method, 'POST')
        self.assertEqual(url, '/axapi/v3/slb/server/%s/port/' % self._server_name)
        self.assertEqual(params, expected)

    def test_update_port(self):
        expected = {
            'port': {
                "conn-resume": None,
                "conn-limit": 12345,
                "stats-data-action": "stats-data-enable",
                "weight": 2,
                "port-number": 80,
                "range": 0,
                "action": "enable",
                "protocol": 'tcp'
            }
        }
        self.port.update('test_server', 80, 'tcp', conn_limit=12345, weight=2)

        ((method, url, params, header), kwargs) = self.client.http.request.call_args

        self.assertEqual(method, 'PUT')
        self.assertEqual(url, '/axapi/v3/slb/server/%s/port/%s+%s/' %
                              (self._server_name, 80, 'tcp'))
        self.assertEqual(params, expected)

    def test_delete_port(self):
        self.port.delete('test_server', 80, 'tcp')

        ((method, url, params, header), kwargs) = self.client.http.request.call_args

        self.assertEqual(method, 'DELETE')
        self.assertEqual(url, '/axapi/v3/slb/server/%s/port/%s+%s/' %
                              (self._server_name, 80, 'tcp'))
