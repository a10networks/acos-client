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
    import unittest
    from unittest import mock
except ImportError:
    import mock
    import unittest2 as unittest

from acos_client import client
import acos_client.errors as acos_errors
import json
import responses


HOSTNAME = 'fake_a10'
BASE_URL = "https://{}:443/axapi/v3".format(HOSTNAME)
AUTH_URL = "{}/auth".format(BASE_URL)
VSERVER_NAME = 'test'
CREATE_URL = '{}/slb/server/'.format(BASE_URL)
OBJECT_URL = '{}/slb/server/{}'.format(BASE_URL, VSERVER_NAME)


class TestServer(unittest.TestCase):

    def setUp(self):
        self.client = client.Client(HOSTNAME, '30', 'fake_username', 'fake_password')

    @mock.patch('acos_client.v30.slb.server.Server.get')
    @responses.activate
    def test_server_create(self, mocked_get):
        mocked_get.side_effect = acos_errors.NotFound
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {'foo': 'bar'}
        responses.add(responses.POST, CREATE_URL, json=json_response, status=200)
        params = {
            'server': {
                'action': 'enable',
                'conn-limit': None,
                'conn-resume': None,
                'health-check': None,
                'host': '192.168.2.254',
                'name': VSERVER_NAME,
            }
        }

        resp = self.client.slb.server.create('test', '192.168.2.254')

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, CREATE_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @mock.patch('acos_client.v30.slb.server.Server.get')
    @responses.activate
    def test_server_create_already_exists(self, mocked_get):
        mocked_get.return_value = {"foo": "bar"}

        with self.assertRaises(acos_errors.Exists):
            self.client.slb.server.create('test', '192.168.2.254')

    @mock.patch('acos_client.v30.slb.server.Server.get')
    @responses.activate
    def test_server_create_with_template(self, mocked_get):
        mocked_get.side_effect = acos_errors.NotFound
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {'foo': 'bar'}
        responses.add(responses.POST, CREATE_URL, json=json_response, status=200)
        params = {
            'server': {
                'action': 'enable',
                'conn-limit': None,
                'conn-resume': None,
                'host': '192.168.2.254',
                'name': VSERVER_NAME,
                'health-check': None,
                'template-server': 'test-template-server'
            }
        }
        templates = {
            "template-server": "test-template-server"
        }
        resp = self.client.slb.server.create('test', '192.168.2.254', server_templates=templates)

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, CREATE_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @responses.activate
    def test_server_delete(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {'foo': 'bar'}
        responses.add(responses.DELETE, OBJECT_URL, json=json_response, status=200)

        resp = self.client.slb.server.delete('test')

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.DELETE)
        self.assertEqual(responses.calls[1].request.url, OBJECT_URL)

    @responses.activate
    def test_server_delete_not_found(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {
            "response": {"status": "fail", "err": {"code": 67174402, "msg": " No such Server"}}
        }
        responses.add(responses.DELETE, OBJECT_URL, json=json_response, status=200)

        with self.assertRaises(acos_errors.ACOSException):
            self.client.slb.server.delete('test')

        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.DELETE)
        self.assertEqual(responses.calls[1].request.url, OBJECT_URL)

    @responses.activate
    def test_server_search(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {
            'server': {
                'status': 1, 'conn_resume': 0, 'weight': 1, 'conn_limit': 64000000, 'host': '192.168.2.254',
                'spoofing_cache': 0, 'port_list': [], 'gslb_external_address': '0.0.0.0', 'slow_start': 0,
                'name': 's1', 'health_monitor': '(default)', 'extended_stats': 0, 'template': 'default',
                'stats_data': 1, 'conn_limit_log': 0
            }
        }
        responses.add(responses.GET, OBJECT_URL, json=json_response, status=200)

        resp = self.client.slb.server.get('test')

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.GET)
        self.assertEqual(responses.calls[1].request.url, OBJECT_URL)

    @responses.activate
    def test_server_search_not_found(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {
            "response": {"status": "fail", "err": {"code": 67174402, "msg": " No such Server"}}
        }
        responses.add(responses.GET, OBJECT_URL, json=json_response, status=200)

        with self.assertRaises(acos_errors.ACOSException):
            self.client.slb.server.get('test')

        self.assertEqual(len(responses.calls), 2)


class TestIPv6Server(unittest.TestCase):

    def setUp(self):
        self.client = client.Client(HOSTNAME, '30', 'fake_username', 'fake_password')

    @mock.patch('acos_client.v30.slb.server.Server.get')
    @responses.activate
    def test_server_create(self, mocked_get):
        mocked_get.side_effect = acos_errors.NotFound
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {'foo': 'bar'}
        responses.add(responses.POST, CREATE_URL, json=json_response, status=200)
        params = {
            'server': {
                'action': 'enable',
                'conn-limit': None,
                'conn-resume': None,
                'health-check': None,
                'server-ipv6-addr': '2001:baad:deed:bead:daab:daad:cead:100e',
                'name': VSERVER_NAME,
            }
        }

        resp = self.client.slb.server.create('test', '2001:baad:deed:bead:daab:daad:cead:100e')

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, CREATE_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @mock.patch('acos_client.v30.slb.server.Server.get')
    @responses.activate
    def test_server_create_already_exists(self, mocked_get):
        mocked_get.return_value = {"foo": "bar"}

        with self.assertRaises(acos_errors.Exists):
            self.client.slb.server.create('test', '2001:baad:deed:bead:daab:daad:cead:100e')

    @mock.patch('acos_client.v30.slb.server.Server.get')
    @responses.activate
    def test_server_create_with_template(self, mocked_get):
        mocked_get.side_effect = acos_errors.NotFound
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {'foo': 'bar'}
        responses.add(responses.POST, CREATE_URL, json=json_response, status=200)
        params = {
            'server': {
                'action': 'enable',
                'conn-limit': None,
                'conn-resume': None,
                'host': '192.168.2.254',
                'name': VSERVER_NAME,
                'health-check': None,
                'template-server': 'test-template-server'
            }
        }
        templates = {
            "template-server": "test-template-server"
        }
        resp = self.client.slb.server.create('test', '192.168.2.254', server_templates=templates)

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, CREATE_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @responses.activate
    def test_server_delete(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {'foo': 'bar'}
        responses.add(responses.DELETE, OBJECT_URL, json=json_response, status=200)

        resp = self.client.slb.server.delete('test')

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.DELETE)
        self.assertEqual(responses.calls[1].request.url, OBJECT_URL)

    @responses.activate
    def test_server_delete_not_found(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {
            "response": {"status": "fail", "err": {"code": 67174402, "msg": " No such Server"}}
        }
        responses.add(responses.DELETE, OBJECT_URL, json=json_response, status=200)

        with self.assertRaises(acos_errors.ACOSException):
            self.client.slb.server.delete('test')

        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.DELETE)
        self.assertEqual(responses.calls[1].request.url, OBJECT_URL)

    @responses.activate
    def test_server_search(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {
            'server': {
                'status': 1, 'conn_resume': 0, 'weight': 1, 'conn_limit': 64000000,
                'server-ipv6-addr': '2001:baad:deed:bead:daab:aad:cead:100e',
                'spoofing_cache': 0, 'port_list': [], 'gslb_external_address': '0.0.0.0', 'slow_start': 0,
                'name': 's1', 'health_monitor': '(default)', 'extended_stats': 0, 'template': 'default',
                'stats_data': 1, 'conn_limit_log': 0
            }
        }
        responses.add(responses.GET, OBJECT_URL, json=json_response, status=200)

        resp = self.client.slb.server.get('test')

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.GET)
        self.assertEqual(responses.calls[1].request.url, OBJECT_URL)

    @responses.activate
    def test_server_search_not_found(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {
            "response": {"status": "fail", "err": {"code": 67174402, "msg": " No such Server"}}
        }
        responses.add(responses.GET, OBJECT_URL, json=json_response, status=200)

        with self.assertRaises(acos_errors.ACOSException):
            self.client.slb.server.get('test')

        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.GET)
        self.assertEqual(responses.calls[1].request.url, OBJECT_URL)
