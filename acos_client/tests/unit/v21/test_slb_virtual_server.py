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
import json
import responses

HOSTNAME = 'fake_a10'
BASE_URL = 'https://{}:443/services/rest/v2.1/?format=json&method='.format(HOSTNAME)
AUTH_URL = '{}authenticate'.format(BASE_URL)
SESSION_ID = 'foobar'
CREATE_URL = '{}slb.virtual_server.create&session_id={}'.format(BASE_URL, SESSION_ID)
UPDATE_URL = '{}slb.virtual_server.update&session_id={}'.format(BASE_URL, SESSION_ID)
DELETE_URL = '{}slb.virtual_server.delete&session_id={}'.format(BASE_URL, SESSION_ID)
SEARCH_URL = '{}slb.virtual_server.search&session_id={}'.format(BASE_URL, SESSION_ID)
STATS_URL = '{}slb.virtual_server.fetchStatistics&session_id={}'.format(BASE_URL, SESSION_ID)
ALL_STATS_URL = '{}slb.virtual_server.fetchAllStatistics&session_id={}'.format(BASE_URL, SESSION_ID)


class TestVirtualServer(unittest.TestCase):

    def setUp(self):
        self.client = client.Client(HOSTNAME, '21', 'fake_username', 'fake_password')

    @responses.activate
    def test_virtual_server_create_no_params(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': SESSION_ID})
        json_response = {"foo": "bar"}
        responses.add(responses.POST, CREATE_URL, json=json_response, status=200)
        params = {
            'virtual_server': {
                'address': '192.168.2.254',
                'name': 'test',
                'status': 1
            }
        }

        resp = self.client.slb.virtual_server.create('test', '192.168.2.254')

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, CREATE_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @responses.activate
    def test_virtual_server_create_with_params(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': SESSION_ID})
        json_response = {"foo": "bar"}
        responses.add(responses.POST, CREATE_URL, json=json_response, status=200)
        params = {
            'virtual_server': {
                'address': '192.168.2.254',
                'name': 'test',
                'status': 1,
                'vrid': 1,
                'vip_template': 'TEST_VIP_TEMPLATE',

            }
        }

        resp = self.client.slb.virtual_server.create(
            name='test',
            ip_address='192.168.2.254',
            status=1,
            vrid=1,
            template_virtual_server='TEST_VIP_TEMPLATE',
        )

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, CREATE_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @responses.activate
    def test_virtual_server_create_already_exists(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': SESSION_ID})
        json_response = {
            "response": {"status": "fail", "err": {"code": 402653206, "msg": " Name already exists."}}
        }
        responses.add(responses.POST, CREATE_URL, json=json_response, status=200)

        with self.assertRaises(acos_errors.Exists):
            self.client.slb.virtual_server.create('test', '192.168.2.254')

        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, CREATE_URL)

    @responses.activate
    def test_virtual_server_update_no_params(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': SESSION_ID})
        json_response = {"foo": "bar"}
        responses.add(responses.POST, UPDATE_URL, json=json_response, status=200)
        params = {
            'virtual_server': {
                'address': '192.168.2.254',
                'name': 'test',
                'status': 1
            }
        }

        resp = self.client.slb.virtual_server.update('test', '192.168.2.254')

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, UPDATE_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @responses.activate
    def test_virtual_server_update_with_params(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': SESSION_ID})
        json_response = {"foo": "bar"}
        responses.add(responses.POST, UPDATE_URL, json=json_response, status=200)
        params = {
            'virtual_server': {
                'address': '192.168.2.254',
                'name': 'test',
                'status': 1,
                'vrid': 1,
                'vip_template': 'TEST_VIP_TEMPLATE',

            }
        }

        resp = self.client.slb.virtual_server.update(
            name='test',
            ip_address='192.168.2.254',
            status=1,
            vrid=1,
            template_virtual_server='TEST_VIP_TEMPLATE',
        )

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, UPDATE_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @responses.activate
    def test_virtual_server_delete(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': SESSION_ID})
        json_response = {"foo": "bar"}
        params = {'name': 'test'}
        responses.add(responses.POST, DELETE_URL, json=json_response, status=200)

        resp = self.client.slb.virtual_server.delete('test')

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, DELETE_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @responses.activate
    def test_virtual_server_delete_not_found(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': SESSION_ID})
        json_response = {"foo": "bar"}
        params = {'name': 'test'}
        responses.add(responses.POST, DELETE_URL, json=json_response, status=200)

        resp = self.client.slb.virtual_server.delete('test')

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, DELETE_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @responses.activate
    def test_virtual_server_search(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': SESSION_ID})
        json_response = {"foo": "bar"}
        params = {'name': 'test'}
        responses.add(responses.POST, SEARCH_URL, json=json_response, status=200)

        resp = self.client.slb.virtual_server.get('test')

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, SEARCH_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @responses.activate
    def test_virtual_server_search_not_found(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': SESSION_ID})
        json_response = {
            "response": {"status": "fail", "err": {"code": 67239937, "msg": " No such Virtual Server"}}
        }
        params = {'name': 'test'}
        responses.add(responses.POST, SEARCH_URL, json=json_response, status=200)

        with self.assertRaises(acos_errors.NotFound):
            self.client.slb.virtual_server.get('test')

        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, SEARCH_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @responses.activate
    def test_virtual_server_stats(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': SESSION_ID})
        json_response = {"foo": "bar"}
        params = {'name': 'test'}
        responses.add(responses.POST, STATS_URL, json=json_response, status=200)

        resp = self.client.slb.virtual_server.stats('test')

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, STATS_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @responses.activate
    def test_virtual_server_all_stats(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': SESSION_ID})
        json_response = {"foo": "bar"}
        responses.add(responses.GET, ALL_STATS_URL, json=json_response, status=200)

        resp = self.client.slb.virtual_server.all_stats()

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.GET)


class TestIPv6VirtualServer(unittest.TestCase):

    def setUp(self):
        self.client = client.Client(HOSTNAME, '21', 'fake_username', 'fake_password')

    @responses.activate
    def test_virtual_server_create_no_params(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': SESSION_ID})
        json_response = {"foo": "bar"}
        responses.add(responses.POST, CREATE_URL, json=json_response, status=200)
        params = {
            'virtual_server': {
                'address': '2001:dbef:1111:feed:beef:8000:1d01:200f',
                'name': 'test',
                'status': 1
            }
        }

        resp = self.client.slb.virtual_server.create('test', '2001:dbef:1111:feed:beef:8000:1d01:200f')

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, CREATE_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @responses.activate
    def test_virtual_server_create_with_params(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': SESSION_ID})
        json_response = {"foo": "bar"}
        responses.add(responses.POST, CREATE_URL, json=json_response, status=200)
        params = {
            'virtual_server': {
                'address': '2001:dbef:1111:feed:beef:8000:1d01:200f',
                'name': 'test',
                'status': 1,
                'vrid': 1,
                'vip_template': 'TEST_VIP_TEMPLATE',

            }
        }

        resp = self.client.slb.virtual_server.create(
            name='test',
            ip_address='2001:dbef:1111:feed:beef:8000:1d01:200f',
            status=1,
            vrid=1,
            template_virtual_server='TEST_VIP_TEMPLATE',
        )

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, CREATE_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @responses.activate
    def test_virtual_server_create_already_exists(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': SESSION_ID})
        json_response = {
            "response": {"status": "fail", "err": {"code": 402653206, "msg": " Name already exists."}}
        }
        responses.add(responses.POST, CREATE_URL, json=json_response, status=200)

        with self.assertRaises(acos_errors.Exists):
            self.client.slb.virtual_server.create('test', '2001:dbef:1111:feed:beef:8000:1d01:200f')

        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, CREATE_URL)

    @responses.activate
    def test_virtual_server_update_no_params(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': SESSION_ID})
        json_response = {"foo": "bar"}
        responses.add(responses.POST, UPDATE_URL, json=json_response, status=200)
        params = {
            'virtual_server': {
                'address': '2001:dbef:1111:feed:beef:8000:1d01:200f',
                'name': 'test',
                'status': 1
            }
        }

        resp = self.client.slb.virtual_server.update('test', '2001:dbef:1111:feed:beef:8000:1d01:200f')

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, UPDATE_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @responses.activate
    def test_virtual_server_update_with_params(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': SESSION_ID})
        json_response = {"foo": "bar"}
        responses.add(responses.POST, UPDATE_URL, json=json_response, status=200)
        params = {
            'virtual_server': {
                'address': '2001:dbef:1111:feed:beef:8000:1d01:200f',
                'name': 'test',
                'status': 1,
                'vrid': 1,
                'vip_template': 'TEST_VIP_TEMPLATE',

            }
        }

        resp = self.client.slb.virtual_server.update(
            name='test',
            ip_address='2001:dbef:1111:feed:beef:8000:1d01:200f',
            status=1,
            vrid=1,
            template_virtual_server='TEST_VIP_TEMPLATE',
        )

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, UPDATE_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @responses.activate
    def test_virtual_server_delete(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': SESSION_ID})
        json_response = {"foo": "bar"}
        params = {'name': 'test'}
        responses.add(responses.POST, DELETE_URL, json=json_response, status=200)

        resp = self.client.slb.virtual_server.delete('test')

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, DELETE_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @responses.activate
    def test_virtual_server_delete_not_found(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': SESSION_ID})
        json_response = {"foo": "bar"}
        params = {'name': 'test'}
        responses.add(responses.POST, DELETE_URL, json=json_response, status=200)

        resp = self.client.slb.virtual_server.delete('test')

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, DELETE_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @responses.activate
    def test_virtual_server_search(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': SESSION_ID})
        json_response = {"foo": "bar"}
        params = {'name': 'test'}
        responses.add(responses.POST, SEARCH_URL, json=json_response, status=200)

        resp = self.client.slb.virtual_server.get('test')

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, SEARCH_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @responses.activate
    def test_virtual_server_search_not_found(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': SESSION_ID})
        json_response = {
            "response": {"status": "fail", "err": {"code": 67239937, "msg": " No such Virtual Server"}}
        }
        params = {'name': 'test'}
        responses.add(responses.POST, SEARCH_URL, json=json_response, status=200)

        with self.assertRaises(acos_errors.NotFound):
            self.client.slb.virtual_server.get('test')

        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, SEARCH_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @responses.activate
    def test_virtual_server_stats(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': SESSION_ID})
        json_response = {"foo": "bar"}
        params = {'name': 'test'}
        responses.add(responses.POST, STATS_URL, json=json_response, status=200)

        resp = self.client.slb.virtual_server.stats('test')

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, STATS_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @responses.activate
    def test_virtual_server_all_stats(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': SESSION_ID})
        json_response = {"foo": "bar"}
        responses.add(responses.GET, ALL_STATS_URL, json=json_response, status=200)

        resp = self.client.slb.virtual_server.all_stats()

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.GET)
        self.assertEqual(responses.calls[1].request.url, ALL_STATS_URL)
