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
from __future__ import absolute_import
from __future__ import unicode_literals

try:
    import unittest
except ImportError:
    import unittest2 as unittest

from acos_client import client
import acos_client.errors as acos_errors
import json
import responses


HOSTNAME = 'fake_a10'
BASE_URL = 'https://{}:443/axapi/v3'.format(HOSTNAME)
AUTH_URL = '{}/auth'.format(BASE_URL)
SERVICE_GROUP_NAME = 'test1'
CREATE_URL = '{}/slb/service-group/'.format(BASE_URL)
OBJECT_URL = '{}/slb/service-group/{}'.format(BASE_URL, SERVICE_GROUP_NAME)


class TestVirtualServer(unittest.TestCase):

    def setUp(self):
        self.client = client.Client(HOSTNAME, '30', 'fake_username', 'fake_password')

    @responses.activate
    def test_server_group_create(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {"foo": "bar"}
        responses.add(responses.POST, CREATE_URL, json=json_response, status=200)

        resp = self.client.slb.service_group.create('test1')

        self.assertEqual(resp, json_response)
        # One responses call for auth and one responses call for post
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, CREATE_URL)

    @responses.activate
    def test_server_group_create_with_templates(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {"foo": "bar"}
        responses.add(responses.POST, CREATE_URL, json=json_response, status=200)
        templates = {
            'template-server': 'template_sv',
            'template-port': 'template_port',
            'template-policy': 'template-pl'
        }
        resp = self.client.slb.service_group.create('test1', service_group_templates=templates)
        params = {
            'service-group':
            {
                'health-check-disable': 0,
                'lb-method': 'round-robin',
                'name': 'test1',
                'protocol': 'tcp',
                'stateless-auto-switch': 0,
                'template-server': 'template_sv',
                'template-port': 'template_port',
                'template-policy': 'template-pl'
            }
        }

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, CREATE_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @responses.activate
    def test_server_group_create_with_kwargs(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {"foo": "bar"}
        responses.add(responses.POST, CREATE_URL, json=json_response, status=200)
        templates = {
            'template-server': 'template_sv',
            'template-port': 'template_port',
            'template-policy': 'template-pl'
        }
        args = {
            'service_group':
            {
                'health_check_disable': 1,
            }
        }
        resp = self.client.slb.service_group.create('test1', service_group_templates=templates, **args)
        params = {
            'service-group':
            {
                'health-check-disable': 1,
                'lb-method': 'round-robin',
                'name': 'test1',
                'protocol': 'tcp',
                'stateless-auto-switch': 0,
                'template-server': 'template_sv',
                'template-port': 'template_port',
                'template-policy': 'template-pl'
            }
        }

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, CREATE_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @responses.activate
    def test_server_group_create_with_partial_templates(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {"foo": "bar"}
        responses.add(responses.POST, CREATE_URL, json=json_response, status=200)

        templates = {
            'template-server': 'template_sv',
            'template-port': 'template_port',
        }
        resp = self.client.slb.service_group.create('test1', service_group_templates=templates)

        params = {
            'service-group':
            {
                'health-check-disable': 0,
                'lb-method': 'round-robin',
                'name': 'test1',
                'protocol': 'tcp',
                'stateless-auto-switch': 0,
                'template-server': 'template_sv',
                'template-port': 'template_port'
            }
        }

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, CREATE_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @responses.activate
    def test_server_group_update(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {"foo": "bar"}
        responses.add(responses.POST, OBJECT_URL, json=json_response, status=200)

        resp = self.client.slb.service_group.update('test1')

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, OBJECT_URL)

    @responses.activate
    def test_server_group_update_with_kwargs(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {"foo": "bar"}
        responses.add(responses.POST, OBJECT_URL, json=json_response, status=200)
        args = {
            'service_group':
            {
                'health_check_disable': 1,
            }
        }
        resp = self.client.slb.service_group.update('test1', **args)
        params = {
            'service-group':
            {
                'health-check-disable': 1,
                'name': 'test1',
            }
        }

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, OBJECT_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @responses.activate
    def test_server_group_replace(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {"foo": "bar"}
        responses.add(responses.PUT, OBJECT_URL, json=json_response, status=200)

        resp = self.client.slb.service_group.replace('test1', protocl='tcp')

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.PUT)
        self.assertEqual(responses.calls[1].request.url, OBJECT_URL)

    @responses.activate
    def test_server_group_delete(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {"foo": "bar"}
        responses.add(responses.DELETE, OBJECT_URL, json=json_response, status=200)

        resp = self.client.slb.service_group.delete('test1')

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.DELETE)
        self.assertEqual(responses.calls[1].request.url, OBJECT_URL)

    @responses.activate
    def test_server_group_delete_not_found(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {
            "response": {"status": "fail", "err": {"code": 67239937, "msg": " No such Virtual Server"}}
        }
        responses.add(responses.DELETE, OBJECT_URL, json=json_response, status=200)

        with self.assertRaises(acos_errors.ACOSException):
            self.client.slb.service_group.delete('test1')

        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.DELETE)
        self.assertEqual(responses.calls[1].request.url, OBJECT_URL)

    @responses.activate
    def test_server_group_stats(self):
        STATS_URL = '{}/slb/service-group/{}/stats'.format(BASE_URL, SERVICE_GROUP_NAME)
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {"foo": "bar"}
        responses.add(responses.GET, STATS_URL, json=json_response, status=200)

        resp = self.client.slb.service_group.stats('test1')

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.GET)
        self.assertEqual(responses.calls[1].request.url, STATS_URL)

    @responses.activate
    def test_server_group_oper(self):
        OPER_URL = '{}/slb/service-group/{}/oper'.format(BASE_URL, SERVICE_GROUP_NAME)
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {"foo": "bar"}
        responses.add(responses.GET, OPER_URL, json=json_response, status=200)

        resp = self.client.slb.service_group.oper('test1')

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.GET)
        self.assertEqual(responses.calls[1].request.url, OPER_URL)

    @responses.activate
    def test_server_group_all(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {"foo": "bar"}
        responses.add(responses.GET, CREATE_URL, json=json_response, status=200)

        resp = self.client.slb.service_group.all('test1')

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.GET)
        self.assertEqual(responses.calls[1].request.url, CREATE_URL)

    @responses.activate
    def test_server_group_all_stats(self):
        ALL_STATS_URL = '{}/slb/service-group/stats'.format(BASE_URL)
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {"foo": "bar"}
        responses.add(responses.GET, ALL_STATS_URL, json=json_response, status=200)

        resp = self.client.slb.service_group.all_stats('test1')

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.GET)
        self.assertEqual(responses.calls[1].request.url, ALL_STATS_URL)

    @responses.activate
    def test_server_group_all_oper(self):
        ALL_OPER_URL = '{}/slb/service-group/oper'.format(BASE_URL)
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {"foo": "bar"}
        responses.add(responses.GET, ALL_OPER_URL, json=json_response, status=200)

        resp = self.client.slb.service_group.all_oper('test1')

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.GET)
        self.assertEqual(responses.calls[1].request.url, ALL_OPER_URL)
