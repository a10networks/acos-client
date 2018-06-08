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
BASE_URL = 'https://{}:443/services/rest/v2.1/?format=json&method='.format(HOSTNAME)
AUTH_URL = '{}authenticate'.format(BASE_URL)
CLOSE_AUTH_URL = '{}session.close&session_id={}'.format(BASE_URL, 'foobar')
BAD_CLOSE_AUTH_URL = '{}session.close&session_id={}'.format(BASE_URL, 'bad_foobar')
SYS_PARTITION_ACTIVE_URL = '{}system.partition.active&session_id={}'.format(BASE_URL, 'foobar')


class TestSession(unittest.TestCase):

    def setUp(self):
        self.client = client.Client(HOSTNAME, '21', 'fake_username', 'fake_password')

    @responses.activate
    def test_session_id_is_none_at_init(self):
        json_response = {'session_id': 'foobar'}
        responses.add(responses.POST, AUTH_URL, json=json_response)

        resp = self.client.session.session_id

        self.assertIsNone(resp)
        self.assertEqual(len(responses.calls), 0)

    @responses.activate
    def test_session_id(self):
        json_response = {'session_id': 'foobar'}
        responses.add(responses.POST, AUTH_URL, json=json_response)

        resp = self.client.session.id

        self.assertEqual(resp, 'foobar')
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.method, responses.POST)
        self.assertEqual(responses.calls[0].request.url, AUTH_URL)

    @responses.activate
    def test_session_authenticate_good_credentials(self):
        json_response = {'session_id': 'foobar'}
        responses.add(responses.POST, AUTH_URL, json=json_response)

        resp = self.client.session.authenticate('fake_username', 'fake_password')

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.method, responses.POST)
        self.assertEqual(responses.calls[0].request.url, AUTH_URL)

    @responses.activate
    def test_session_authenticate_bad_credentials(self):
        json_response = {"response": {"status": "fail", "err": {"code": 520486915, "msg": " Admin password error"}}}
        responses.add(responses.POST, AUTH_URL, json=json_response)

        with self.assertRaises(acos_errors.AuthenticationFailure):
            self.client.session.authenticate('bad_username', 'bad_password')

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.method, responses.POST)
        self.assertEqual(responses.calls[0].request.url, AUTH_URL)

    @responses.activate
    def test_session_close_good_session_id(self):
        auth_json_response = {'session_id': 'foobar'}
        responses.add(responses.POST, AUTH_URL, json=auth_json_response, status=200)
        close_json_response = {'response': {'status': 'OK'}}
        responses.add(responses.POST, CLOSE_AUTH_URL, json=close_json_response, status=200)

        self.client.session.id
        self.assertEqual(self.client.session.session_id, 'foobar')

        resp = self.client.session.close()

        self.assertEqual(resp, close_json_response)
        self.assertEqual(self.client.session.session_id, None)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, CLOSE_AUTH_URL)

    @responses.activate
    def test_session_close_bad_session_id(self):
        auth_json_response = {'session_id': 'foobar'}
        responses.add(responses.POST, AUTH_URL, json=auth_json_response, status=200)
        close_json_response = {"response": {"status": "fail", "err": {"code": 1009, "msg": "Invalid session ID"}}}
        responses.add(responses.POST, BAD_CLOSE_AUTH_URL, json=close_json_response, status=200)

        self.client.session.id
        self.assertEqual(self.client.session.session_id, 'foobar')
        self.client.session.session_id = 'bad_foobar'

        resp = self.client.session.close()

        self.assertEqual(resp, close_json_response)
        self.assertEqual(self.client.session.session_id, None)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, BAD_CLOSE_AUTH_URL)
