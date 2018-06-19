# Copyright 2014,  Doug Wiegley,  A10 Networks.
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

from __future__ import absolute_import
from __future__ import unicode_literals

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from acos_client import client
import responses


HOSTNAME = 'fake_a10'
BASE_URL = "https://{}:443/services/rest/v2.1/?format=json&method=".format(HOSTNAME)
AUTH_URL = "{}authenticate".format(BASE_URL)
INTERFACE_GET_URL = '{}network.interface.get&session_id={}'.format(BASE_URL, 'foobar')
INTERFACE_GET_LIST_URL = '{}network.interface.getAll&session_id={}'.format(BASE_URL, 'foobar')


class TestInterfaceGet(unittest.TestCase):

    def setUp(self):
        self.client = client.Client(HOSTNAME, '21', 'fake_username', 'fake_password')

    @responses.activate
    def test_interface_get(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {
            "interface": {"port_num": 1, "type": "ethernet", }
        }
        responses.add(responses.POST, INTERFACE_GET_URL, json=json_response, status=200)

        resp = self.client.interface.ethernet.get(1)

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, INTERFACE_GET_URL)

    @responses.activate
    def test_interface_get_list(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = [
            {"interface": {"port_num": 1, "type": "ethernet", }}, {"interface": {"port_num": 2, "type": "ethernet", }}
        ]
        responses.add(responses.GET, INTERFACE_GET_LIST_URL, json=json_response, status=200)

        resp = self.client.interface.get_list()

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.GET)
        self.assertEqual(responses.calls[1].request.url, INTERFACE_GET_LIST_URL)
