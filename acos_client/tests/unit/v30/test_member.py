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
import json
import responses

try:
    import unittest
except ImportError:
    import unittest2 as unittest

from acos_client import client

HOSTNAME = 'fake_a10'
BASE_URL = 'https://{}:443/axapi/v3'.format(HOSTNAME)
AUTH_URL = '{}/auth'.format(BASE_URL)
MEM_NAME = 'fake-server'
SG_NAME = 'fake-sg'
CREATE_URL = '{}/slb/service-group/{}/member/'.format(BASE_URL, SG_NAME)
OBJECT_URL = '{}/slb/service-group/{}/member/{}+{}/'
OK_RESP = {'response': {'status': 'OK'}}


class TestMember(unittest.TestCase):

    def setUp(self):
        self.client = client.Client(HOSTNAME, '30', 'fake_username', 'fake_password')
        self.member = self.client.slb.service_group.member

    @responses.activate
    def test_create_enable_member(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        responses.add(responses.POST, CREATE_URL, json=OK_RESP, status=200)
        params = {
            'member': {
                'name': MEM_NAME,
                'port': 80,
                'member-stats-data-disable': self.member.STATUS_ENABLE,
                'member-state': 'enable',
            }
        }
        resp = self.member.create(SG_NAME, MEM_NAME, 80)

        self.assertEqual(resp, OK_RESP)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, CREATE_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @responses.activate
    def test_create_disable_member(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        responses.add(responses.POST, CREATE_URL, json=OK_RESP, status=200)
        params = {
            'member': {
                'name': MEM_NAME,
                'port': 80,
                'member-stats-data-disable': self.member.STATUS_DISABLE,
                'member-state': 'disable',
            }
        }
        resp = self.member.create(SG_NAME, MEM_NAME, 80,
                                  self.member.STATUS_DISABLE,
                                  False)

        self.assertEqual(resp, OK_RESP)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, CREATE_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @responses.activate
    def test_update_enable_member(self):
        port = 443
        object_url = OBJECT_URL.format(BASE_URL, SG_NAME, MEM_NAME, port)
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        responses.add(responses.POST, object_url, json=OK_RESP, status=200)
        params = {
            'member': {
                'name': MEM_NAME,
                'port': port,
                'member-stats-data-disable': self.member.STATUS_ENABLE,
                'member-state': 'enable',
            }
        }
        resp = self.member.update(SG_NAME, MEM_NAME, port)

        self.assertEqual(resp, OK_RESP)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, object_url)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @responses.activate
    def test_update_disable_member(self):
        port = 443
        object_url = OBJECT_URL.format(BASE_URL, SG_NAME, MEM_NAME, port)
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        responses.add(responses.POST, object_url, json=OK_RESP, status=200)
        params = {
            'member': {
                'name': MEM_NAME,
                'port': port,
                'member-stats-data-disable': self.member.STATUS_DISABLE,
                'member-state': 'disable',
            }
        }
        resp = self.member.update(SG_NAME, MEM_NAME, port,
                                  self.member.STATUS_DISABLE,
                                  False)

        self.assertEqual(resp, OK_RESP)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, object_url)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @responses.activate
    def test_replace_enable_member(self):
        port = 443
        object_url = OBJECT_URL.format(BASE_URL, SG_NAME, MEM_NAME, port)
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        responses.add(responses.PUT, object_url, json=OK_RESP, status=200)
        params = {
            'member': {
                'name': MEM_NAME,
                'port': port,
                'member-stats-data-disable': self.member.STATUS_ENABLE,
                'member-state': 'enable',
            }
        }
        resp = self.member.replace(SG_NAME, MEM_NAME, port)

        self.assertEqual(resp, OK_RESP)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.PUT)
        self.assertEqual(responses.calls[1].request.url, object_url)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)
