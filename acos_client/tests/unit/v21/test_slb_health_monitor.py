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
CREATE_URL = '{}slb.hm.create&session_id={}'.format(BASE_URL, 'foobar')
DELETE_URL = '{}slb.hm.delete&session_id={}'.format(BASE_URL, 'foobar')
SEARCH_URL = '{}slb.hm.search&session_id={}'.format(BASE_URL, 'foobar')
UPDATE_URL = '{}slb.hm.update&session_id={}'.format(BASE_URL, 'foobar')


class TestHealthMonitor(unittest.TestCase):

    def setUp(self):
        self.client = client.Client(HOSTNAME, '21', 'fake_username', 'fake_password')

    @responses.activate
    def test_health_monitor_create(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {
            'response': {'status': 'OK'}
        }
        responses.add(responses.POST, CREATE_URL, json=json_response, status=200)

        resp = self.client.slb.hm.create('test1', 'HTTP', 5, 5, 5, 'GET', '/', '200', 80)

        self.assertIsNone(resp)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, CREATE_URL)

    @responses.activate
    def test_health_monitor_create_already_exists(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {
            "response": {"status": "fail", "err": {
                "code": 2941, "msg": "The same health monitor name already exist."}}
        }
        responses.add(responses.POST, CREATE_URL, json=json_response, status=200)

        with self.assertRaises(acos_errors.Exists):
            self.client.slb.hm.create('test1', 'HTTP', 5, 5, 5, 'GET', '/', '200', 80)

        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, CREATE_URL)

    @responses.activate
    def test_health_monitor_delete(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {
            'response': {'status': 'OK'}
        }
        responses.add(responses.POST, DELETE_URL, json=json_response, status=200)

        resp = self.client.slb.hm.delete('test1')

        self.assertIsNone(resp)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, DELETE_URL)

    @responses.activate
    def test_health_monitor_delete_not_found(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {
            "response": {"status": "fail", "err": {"code": 33619968, "msg": " The monitor does not exist."}}
        }
        responses.add(responses.POST, DELETE_URL, json=json_response, status=200)

        resp = self.client.slb.hm.delete('test1')

        self.assertIsNone(resp)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, DELETE_URL)

    @responses.activate
    def test_health_monitor_search(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {
            "health_monitor": {"name": "hfoobar", "retry": 5, "consec_pass_reqd": 5, "interval": 5, "timeout": 5,
                               "strictly_retry": 0, "disable_after_down": 0, "override_ipv4": "0.0.0.0",
                               "override_ipv6": "::", "override_port": 0, "type": 3, "http":
                               {"port": 80, "host": "", "url": "GET /", "user": "", "password": "",
                                "expect_code": "200", "maintenance_code": ""}}}
        responses.add(responses.POST, SEARCH_URL, json=json_response, status=200)

        resp = self.client.slb.hm.get('test1')

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, SEARCH_URL)

    @responses.activate
    def test_health_monitor_search_not_found(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {
            "response": {"status": "fail", "err": {"code": 33619968, "msg": " The monitor does not exist."}}
        }
        responses.add(responses.POST, SEARCH_URL, json=json_response, status=200)

        with self.assertRaises(acos_errors.NotFound):
            self.client.slb.hm.get('test1')

        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, SEARCH_URL)

    @responses.activate
    def test_health_monitor_update(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {
            'response': {'status': 'OK'}
        }
        responses.add(responses.POST, UPDATE_URL, json=json_response, status=200)

        resp = self.client.slb.hm.update('test1', 'HTTP', 5, 5, 5, 'GET', '/', '200', 80)

        self.assertIsNone(resp)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, UPDATE_URL)

    @responses.activate
    def test_health_monitor_update_not_found(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {
            "response": {"status": "fail", "err": {"code": 33619968, "msg": " The monitor does not exist."}}
        }
        responses.add(responses.POST, UPDATE_URL, json=json_response, status=200)

        with self.assertRaises(acos_errors.NotFound):
            self.client.slb.hm.update('test1', 'HTTP', 5, 5, 5, 'GET', '/', '200', 80)

        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, UPDATE_URL)
