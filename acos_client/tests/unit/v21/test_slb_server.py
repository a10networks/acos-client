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
import acos_client.errors as acos_errors
import responses


HOSTNAME = 'fake_a10'
BASE_URL = "https://{}:443/services/rest/v2.1/?format=json&method=".format(HOSTNAME)
AUTH_URL = "{}authenticate".format(BASE_URL)
CREATE_URL = '{}slb.server.create&session_id={}'.format(BASE_URL, 'foobar')
DELETE_URL = '{}slb.server.delete&session_id={}'.format(BASE_URL, 'foobar')
SEARCH_URL = '{}slb.server.search&session_id={}'.format(BASE_URL, 'foobar')


class TestServer(unittest.TestCase):

    def setUp(self):
        self.client = client.Client(HOSTNAME, '21', 'fake_username', 'fake_password')

    @responses.activate
    def test_server_create(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {
            'response': {'status': 'OK'}
        }
        responses.add(responses.POST, CREATE_URL, json=json_response, status=200)

        resp = self.client.slb.server.create('test', '192.168.2.254')

        self.assertIsNone(resp)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, CREATE_URL)

    @responses.activate
    def test_server_create_already_exists(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {
            "response": {"status": "fail", "err": {"code": 402653200, "msg": " Name or IP address already exists."}}
        }
        responses.add(responses.POST, CREATE_URL, json=json_response, status=200)

        with self.assertRaises(acos_errors.Exists):
            self.client.slb.server.create('test', '192.168.2.254')

        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, CREATE_URL)

    @responses.activate
    def test_server_delete(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {
            'response': {'status': 'OK'}
        }
        responses.add(responses.POST, DELETE_URL, json=json_response, status=200)

        resp = self.client.slb.server.delete('test')

        self.assertIsNone(resp)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, DELETE_URL)

    @responses.activate
    def test_server_delete_not_found(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {
            "response": {"status": "fail", "err": {"code": 67174402, "msg": " No such Server"}}
        }
        responses.add(responses.POST, DELETE_URL, json=json_response, status=200)

        resp = self.client.slb.server.delete('test')

        self.assertIsNone(resp)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, DELETE_URL)

    @responses.activate
    def test_server_search(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {
            'server': {
                'status': 1, 'conn_resume': 0, 'weight': 1, 'conn_limit': 8000000, 'host': '192.168.2.254',
                'spoofing_cache': 0, 'port_list': [], 'gslb_external_address': '0.0.0.0', 'slow_start': 0,
                'name': 's1', 'health_monitor': '(default)', 'extended_stats': 0, 'template': 'default',
                'stats_data': 1, 'conn_limit_log': 0
            }
        }
        responses.add(responses.POST, SEARCH_URL, json=json_response, status=200)

        resp = self.client.slb.server.get('test')

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, SEARCH_URL)

    @responses.activate
    def test_server_search_not_found(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {
            "response": {"status": "fail", "err": {"code": 67174402, "msg": " No such Server"}}
        }
        responses.add(responses.POST, SEARCH_URL, json=json_response, status=200)

        with self.assertRaises(acos_errors.NotFound):
            self.client.slb.server.get('test')

        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)


class TestIPv6Server(unittest.TestCase):

    def setUp(self):
        self.client = client.Client(HOSTNAME, '21', 'fake_username', 'fake_password')

    @responses.activate
    def test_server_create(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {
            'response': {'status': 'OK'}
        }
        responses.add(responses.POST, CREATE_URL, json=json_response, status=200)

        resp = self.client.slb.server.create('test', '2001:baad:deed:bead:daab:daad:cead:100e')

        self.assertIsNone(resp)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, CREATE_URL)

    @responses.activate
    def test_server_create_already_exists(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {
            "response": {"status": "fail", "err": {"code": 402653200, "msg": " Name or IP address already exists."}}
        }
        responses.add(responses.POST, CREATE_URL, json=json_response, status=200)

        with self.assertRaises(acos_errors.Exists):
            self.client.slb.server.create('test', '2001:baad:deed:bead:daab:daad:cead:100e')

        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, CREATE_URL)

    @responses.activate
    def test_server_delete(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {
            'response': {'status': 'OK'}
        }
        responses.add(responses.POST, DELETE_URL, json=json_response, status=200)

        resp = self.client.slb.server.delete('test')

        self.assertIsNone(resp)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, DELETE_URL)

    @responses.activate
    def test_server_delete_not_found(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {
            "response": {"status": "fail", "err": {"code": 67174402, "msg": " No such Server"}}
        }
        responses.add(responses.POST, DELETE_URL, json=json_response, status=200)

        resp = self.client.slb.server.delete('test')

        self.assertIsNone(resp)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, DELETE_URL)

    @responses.activate
    def test_server_search(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {
            'server': {
                'status': 1, 'conn_resume': 0, 'weight': 1, 'conn_limit': 8000000,
                'host': '2001:baad:deed:bead:daab:daad:cead:100e',
                'spoofing_cache': 0, 'port_list': [], 'gslb_external_address': '0.0.0.0', 'slow_start': 0,
                'name': 's1', 'health_monitor': '(default)', 'extended_stats': 0, 'template': 'default',
                'stats_data': 1, 'conn_limit_log': 0
            }
        }
        responses.add(responses.POST, SEARCH_URL, json=json_response, status=200)

        resp = self.client.slb.server.get('test')

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, SEARCH_URL)

    @responses.activate
    def test_server_search_not_found(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {
            "response": {"status": "fail", "err": {"code": 67174402, "msg": " No such Server"}}
        }
        responses.add(responses.POST, SEARCH_URL, json=json_response, status=200)

        with self.assertRaises(acos_errors.NotFound):
            self.client.slb.server.get('test')

        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, SEARCH_URL)
