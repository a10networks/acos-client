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
BASE_URL = 'https://{}:443/services/rest/v2.1/?format=json&method='.format(HOSTNAME)
AUTH_URL = '{}authenticate'.format(BASE_URL)
SESSION_ID = 'foobar'
CREATE_URL = '{}slb.virtual_server.vport.create&session_id={}'.format(BASE_URL, SESSION_ID)
UPDATE_URL = '{}slb.virtual_server.vport.update&session_id={}'.format(BASE_URL, SESSION_ID)
DELETE_URL = '{}slb.virtual_server.vport.delete&session_id={}'.format(BASE_URL, SESSION_ID)
SEARCH_URL = '{}slb.virtual_server.search&session_id={}'.format(BASE_URL, SESSION_ID)


class TestVirtualPort(unittest.TestCase):

    def setUp(self):
        self.client = client.Client(HOSTNAME, '21', 'fake_username', 'fake_password')
        self.maxDiff = None

    @responses.activate
    def test_virtual_port_create_no_params(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': SESSION_ID})
        json_response = {"foo": "bar"}
        responses.add(responses.POST, CREATE_URL, json=json_response, status=200)
        params = {
            "name": "test1",
            "vport": {
                "name": "test1_VPORT",
                "service_group": "pool1",
                "protocol": 11,
                "port": 80,
                "status": 1
            }
        }

        resp = self.client.slb.virtual_server.vport.create(
            'test1', 'test1_VPORT', protocol=self.client.slb.virtual_server.vport.HTTP, port='80',
            service_group_name='pool1'
        )

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, CREATE_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @responses.activate
    def test_virtual_port_create_with_params(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': SESSION_ID})
        json_response = {"foo": "bar"}
        responses.add(responses.POST, CREATE_URL, json=json_response, status=200)
        params = {
            'name': 'test1',
            'vport': {
                'cookie_persistence_template': 'test_c_pers_template',
                'ip_in_ip': 1,
                'name': 'test1_VPORT',
                'port': 80,
                'protocol': 11,
                'service_group': 'pool1',
                'source_ip_persistence_template': 'test_s_pers_template',
                'ha-conn-mirror': 1,
                'no-dest-nat': 1,
                'conn-limit': 50000,
                'source_nat': 'test_nat_pool',
                'source_nat_auto': 1,
                'status': 1,
                'tcp_template': 'test_tcp_template',
                'udp_template': 'test_udp_template'
            }
        }

        resp = self.client.slb.virtual_server.vport.create(
            virtual_server_name='test1',
            name='test1_VPORT',
            protocol=self.client.slb.virtual_server.vport.HTTP,
            port='80',
            service_group_name='pool1',
            s_pers_name="test_s_pers_template",
            c_pers_name="test_c_pers_template",
            status=1,
            autosnat=True,
            ipinip=True,
            ha_conn_mirror=1,
            no_dest_nat=1,
            conn_limit=50000,
            source_nat_pool="test_nat_pool",
            tcp_template="test_tcp_template",
            udp_template="test_udp_template",
        )

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, CREATE_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @responses.activate
    def test_virtual_port_create_already_exists(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': SESSION_ID})
        json_response = {
            "response": {"status": "fail", "err": {"code": 1406, "msg": "The virtual port already exists."}}
        }
        responses.add(responses.POST, CREATE_URL, json=json_response, status=200)
        params = {
            "name": "test1",
            "vport": {
                "name": "test1_VPORT",
                "service_group": "pool1",
                "protocol": 11,
                "port": 80,
                "status": 1
            }
        }

        with self.assertRaises(acos_errors.Exists):
            self.client.slb.virtual_server.vport.create(
                'test1', 'test1_VPORT', protocol=self.client.slb.virtual_server.vport.HTTP, port='80',
                service_group_name='pool1'
            )

        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, CREATE_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @responses.activate
    def test_virtual_port_update_no_params(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': SESSION_ID})
        json_response = {"foo": "bar"}
        responses.add(responses.POST, UPDATE_URL, json=json_response, status=200)
        params = {
            "name": "test1",
            "vport": {
                "name": "test1_VPORT",
                "service_group": "pool1",
                "protocol": 11,
                "port": 80,
                "status": 1
            }
        }

        resp = self.client.slb.virtual_server.vport.update(
            'test1', 'test1_VPORT', protocol=self.client.slb.virtual_server.vport.HTTP, port='80',
            service_group_name='pool1'
        )

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, UPDATE_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @responses.activate
    def test_virtual_port_update_with_params(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': SESSION_ID})
        json_response = {"foo": "bar"}
        responses.add(responses.POST, UPDATE_URL, json=json_response, status=200)
        params = {
            'name': 'test1',
            'vport': {
                'cookie_persistence_template': 'test_c_pers_template',
                'ip_in_ip': 1,
                'name': 'test1_VPORT',
                'port': 80,
                'protocol': 11,
                'service_group': 'pool1',
                'source_ip_persistence_template': 'test_s_pers_template',
                'source_nat': 'test_nat_pool',
                'source_nat_auto': 1,
                'status': 1,
                'ha-conn-mirror': 1,
                'no-dest-nat': 1,
                'conn-limit': 50000,
                'tcp_template': 'test_tcp_template',
                'udp_template': 'test_udp_template'
            }
        }

        resp = self.client.slb.virtual_server.vport.update(
            virtual_server_name='test1',
            name='test1_VPORT',
            protocol=self.client.slb.virtual_server.vport.HTTP,
            port='80',
            service_group_name='pool1',
            s_pers_name="test_s_pers_template",
            c_pers_name="test_c_pers_template",
            status=1,
            autosnat=True,
            ipinip=True,
            ha_conn_mirror=1,
            no_dest_nat=1,
            conn_limit=50000,
            source_nat_pool="test_nat_pool",
            tcp_template="test_tcp_template",
            udp_template="test_udp_template",
        )

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, UPDATE_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @responses.activate
    def test_virtual_port_delete(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': SESSION_ID})
        json_response = {"foo": "bar"}
        responses.add(responses.POST, DELETE_URL, json=json_response, status=200)
        params = {
            "name": "test1",
            "vport": {
                "name": "test1_VPORT",
                "protocol": 11,
                "port": 80,
            }
        }

        resp = self.client.slb.virtual_server.vport.delete(
            'test1', 'test1_VPORT', self.client.slb.virtual_server.vport.HTTP, '80'
        )

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, DELETE_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @responses.activate
    def test_virtual_port_delete_not_found(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': SESSION_ID})
        json_response = {
            "response": {"status": "fail", "err": {"code": 1043, "msg": "Can not find the virtual server port"}}
        }
        responses.add(responses.POST, DELETE_URL, json=json_response, status=200)
        params = {
            "name": "test1",
            "vport": {
                "name": "test1_VPORT",
                "protocol": 11,
                "port": 80,
            }
        }

        resp = self.client.slb.virtual_server.vport.delete(
            'test1', 'test1_VPORT', self.client.slb.virtual_server.vport.HTTP, '80'
        )

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, DELETE_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @mock.patch('acos_client.v21.slb.virtual_port.VirtualPort._post')
    @responses.activate
    def test_virtual_port_search(self, mocked__post):
        mocked__post.return_value = {
            'virtual_server': {
                'name': 'test1',
                'vport_list': [
                    {
                        'protocol': 12,
                        'port': 443,
                        'name': 'test2_VPORT',
                    },
                    {
                        'protocol': 11,
                        'port': 80,
                        'name': 'test1_VPORT',
                    }
                ]
            }
        }
        json_response = {
            'protocol': 11,
            'port': 80,
            'name': 'test1_VPORT',
        }

        resp = self.client.slb.virtual_server.vport.get(
            'test1', 'test1_VPORT', protocol=self.client.slb.virtual_server.vport.HTTP, port='80'
        )

        self.assertEqual(resp, json_response)

    @responses.activate
    def test_virtual_port_search_virtual_server_not_found(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': SESSION_ID})
        json_response = {
            "response": {"status": "fail", "err": {"code": 1043, "msg": "Can not find the virtual server port"}}
        }
        responses.add(responses.POST, SEARCH_URL, json=json_response, status=200)

        with self.assertRaises(acos_errors.NotFound):
            self.client.slb.virtual_server.vport.get(
                'test1', 'test1_VPORT', protocol=self.client.slb.virtual_server.vport.HTTP, port='80'
            )

        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, SEARCH_URL)
