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
AUTH_CLOSE_URL = "{}session.close&session_id=None".format(BASE_URL)
CREATE_URL = '{}system.partition.create&session_id={}'.format(BASE_URL, 'foobar')
DELETE_URL = '{}system.partition.delete&session_id={}'.format(BASE_URL, 'foobar')
SEARCH_URL = '{}system.partition.search&session_id={}'.format(BASE_URL, 'foobar')
ACTIVE_URL = '{}system.partition.active&session_id={}'.format(BASE_URL, 'foobar')


class TestPartition(unittest.TestCase):

    def setUp(self):
        self.client = client.Client(HOSTNAME, '21', 'fake_username', 'fake_password')

    @responses.activate
    def test_system_partition_create(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {
            'response': {'status': 'OK'}
        }
        responses.add(responses.POST, CREATE_URL, json=json_response, status=200)

        resp = self.client.system.partition.create('test1')

        self.assertIsNone(resp)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, CREATE_URL)

    @responses.activate
    def test_system_partition_create_already_exists(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {
            "response": {"status": "fail", "err": {"code": 1982, "msg": "The partition already exists"}}
        }
        responses.add(responses.POST, CREATE_URL, json=json_response, status=200)

        with self.assertRaises(acos_errors.Exists):
            self.client.system.partition.create('test1')
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, CREATE_URL)

    @responses.activate
    def test_system_partition_delete(self):
        responses.add(responses.POST, AUTH_CLOSE_URL)
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {
            'response': {'status': 'OK'}
        }
        responses.add(responses.POST, DELETE_URL, json=json_response, status=200)
        resp = self.client.system.partition.delete('test1')

        self.assertIsNone(resp)
        self.assertEqual(len(responses.calls), 3)
        self.assertEqual(responses.calls[2].request.method, responses.POST)
        self.assertEqual(responses.calls[2].request.url, DELETE_URL)

    @responses.activate
    def test_system_partition_delete_not_found(self):
        responses.add(responses.POST, AUTH_CLOSE_URL)
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {
            "response": {"status": "fail", "err": {"code": 520749062, "msg": " Partition does not exist."}}
        }
        responses.add(responses.POST, DELETE_URL, json=json_response, status=200)

        with self.assertRaises(acos_errors.NotFound):
            self.client.system.partition.delete('test1')
        self.assertEqual(len(responses.calls), 3)
        self.assertEqual(responses.calls[2].request.method, responses.POST)
        self.assertEqual(responses.calls[2].request.url, DELETE_URL)

    @responses.activate
    def test_system_partition_search(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {
            "partition": {"partition_id": 1, "name": "p1", "max_aflex_file": 32, "network_partition": 0}
        }
        responses.add(responses.POST, SEARCH_URL, json=json_response, status=200)

        resp = self.client.system.partition.exists('test1')

        self.assertEqual(resp, True)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, SEARCH_URL)

    @responses.activate
    def test_system_partition_search_not_found(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {
            "response": {"status": "fail", "err": {"code": 520749062, "msg": " Partition does not exist."}}
        }
        responses.add(responses.POST, SEARCH_URL, json=json_response, status=200)

        resp = self.client.system.partition.exists('test1')

        self.assertEqual(resp, False)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, SEARCH_URL)

    @responses.activate
    def test_system_partition_active(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {
            'response': {'status': 'OK'}
        }
        responses.add(responses.POST, ACTIVE_URL, json=json_response, status=200)

        resp = self.client.system.partition.active('test1')

        self.assertIsNone(resp)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, ACTIVE_URL)

    @responses.activate
    def test_system_partition_active_not_found(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {
            "response": {"status": "fail", "err": {"code": 402718800, "msg": " Failed to get partition."}}
        }
        responses.add(responses.POST, ACTIVE_URL, json=json_response, status=200)

        with self.assertRaises(acos_errors.NotFound):
            self.client.system.partition.active('test1')
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, ACTIVE_URL)
