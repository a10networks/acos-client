# Copyright 2014-2016, Omkar Telee, A10 Networks.
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
import responses


HOSTNAME = 'fake_a10'
BASE_URL = 'https://{}:443/axapi/v3'.format(HOSTNAME)
AUTH_URL = '{}/auth'.format(BASE_URL)
AFLEX_NAME = 'test1'
CREATE_URL = '{}/file/aflex/'.format(BASE_URL)
OBJECT_URL = '{}/file/aflex/{}'.format(BASE_URL, AFLEX_NAME)


class TestAFlex(unittest.TestCase):

    def setUp(self):
        self.client = client.Client(HOSTNAME, '30', 'fake_username', 'fake_password')

    @mock.patch('acos_client.v30.slb.aflex_policy.AFlexPolicy.get')
    @responses.activate
    def test_aflex_create(self, mocked_get):
        mocked_get.side_effect = acos_errors.NotFound
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {"foo": "bar"}
        responses.add(responses.POST, CREATE_URL, json=json_response, status=200)
        filename = "testaflexpolicy"
        script = "when RULE_INIT{ change }"
        size = len(script.encode('utf-8'))
        action = "import"

        resp = self.client.slb.aflex_policy.create(filename, script, size, action)
        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, CREATE_URL)
        self.assertIn(filename, responses.calls[1].request.body.decode('UTF-8'))
        self.assertIn(action, responses.calls[1].request.body.decode('UTF-8'))

    @mock.patch('acos_client.v30.slb.aflex_policy.AFlexPolicy.get')
    @responses.activate
    def test_aflex_update(self, mocked_get):
        mocked_get.side_effect = acos_errors.NotFound
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {"foo": "bar"}
        responses.add(responses.POST, CREATE_URL, json=json_response, status=200)
        filename = "testaflexpolicy"
        script = "when RULE_INIT{}"
        size = len(script.encode('utf-8'))
        action = "import"

        resp = self.client.slb.aflex_policy.update(filename, script, size, action)
        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, CREATE_URL)
        self.assertIn(filename, responses.calls[1].request.body.decode('UTF-8'))
        self.assertIn(action, responses.calls[1].request.body.decode('UTF-8'))

    @mock.patch('acos_client.v30.slb.aflex_policy.AFlexPolicy.get')
    @responses.activate
    def test_aflex_delete(self, mocked_get):
        mocked_get.side_effect = acos_errors.NotFound
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {"foo": "bar"}
        responses.add(responses.POST, CREATE_URL, json=json_response, status=200)
        filename = "testaflexpolicy"

        resp = self.client.slb.aflex_policy.delete(filename)
        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, CREATE_URL)
        self.assertIn(filename, responses.calls[1].request.body.decode('UTF-8'))
        self.assertIn('delete', responses.calls[1].request.body.decode('UTF-8'))
