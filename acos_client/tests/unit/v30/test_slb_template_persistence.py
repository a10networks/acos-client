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
BASE_URL = "https://{}:443/axapi/v3/".format(HOSTNAME)
AUTH_URL = "{}auth".format(BASE_URL)
SLB_URL = '{}slb/template/persist/cookie/'.format(BASE_URL)
T_NAME = "test1"
T_DOMAIN = "domain1"


class TestSLBTemplateCookiePersistence(unittest.TestCase):

    def setUp(self):
        self.client = client.Client(HOSTNAME, '30', 'fake_username', 'fake_password')

    def get_auth_response(self):
        return {'authresponse': {'signature': 'foo', 'description': 'bar.'}}

    def get_url(self, tname):
        return "{0}{1}".format(SLB_URL, tname)

    @responses.activate
    def test_slb_template_persistence_create(self):
        # NOTE: Create method tries GET request to see if template exists before using POST request to create template.
        responses.add(responses.POST, AUTH_URL, json=self.get_auth_response())
        get_url = self.get_url(T_NAME)
        get_json_response = {
            'response': {'status': 'fail', 'err': {
                'code': 1023460352, 'from': 'CM', 'msg': 'Object specified does not exist (object: cookie)'}}
        }
        responses.add(responses.GET, get_url, json=get_json_response, status=404)
        post_url = SLB_URL
        post_json_response = {
            'cookie': {'name': T_NAME, 'dont-honor-conn-rules': 0, 'insert-always': 0, 'encrypt-level': 1,
                       'encrypted': 'foo', 'cookie-name': 'sto-id', 'path': '/', 'pass-thru': 0, 'secure': 0,
                       'httponly': 0, 'match-type': 0, 'uuid': '40143610-6a61-11e8-9bf6-c3c3b3edcd4e'}
        }
        responses.add(responses.POST, post_url, json=post_json_response, status=200)

        resp = self.client.slb.template.cookie_persistence.create(T_NAME)

        self.assertIsNone(resp)
        self.assertEqual(len(responses.calls), 3)
        self.assertEqual(responses.calls[1].request.method, responses.GET)
        self.assertEqual(responses.calls[1].request.url, get_url)
        self.assertEqual(responses.calls[2].request.method, responses.POST)
        self.assertEqual(responses.calls[2].request.url, post_url)

    @responses.activate
    def test_slb_template_persistence_create_already_exists(self):
        # NOTE: Create method tries GET request to see if template exists before using POST request to create template.
        responses.add(responses.POST, AUTH_URL, json=self.get_auth_response())
        url = self.get_url(T_NAME)

        json_response = {
            'response': {'status': 'fail', 'err': {
                'code': 1023459339, 'from': 'CM', 'msg': 'Failed to handle object "cookie". Object already exists',
                'location': 'cookie'}}
        }
        responses.add(responses.GET, url, json=json_response, status=200)

        with self.assertRaises(acos_errors.ACOSException):
            self.client.slb.template.cookie_persistence.create(T_NAME)

        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.GET)
        self.assertEqual(responses.calls[1].request.url, url)

    @responses.activate
    def test_slb_template_persistence_delete(self):
        responses.add(responses.POST, AUTH_URL, json=self.get_auth_response())
        url = self.get_url(T_NAME)

        json_response = {
            'response': {'status': 'OK'}
        }
        responses.add(responses.DELETE, url, json=json_response, status=200)

        resp = self.client.slb.template.cookie_persistence.delete(T_NAME)

        self.assertIsNone(resp)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.DELETE)
        self.assertEqual(responses.calls[1].request.url, url)

    @responses.activate
    def test_slb_template_persistence_delete_not_found(self):
        responses.add(responses.POST, AUTH_URL, json={'authresponse': {'signature': 'foo', 'description': 'bar.'}})
        url = self.get_url(T_NAME)
        json_response = {
            'response': {'status': 'fail', 'err': {
                'code': 1023460352, 'from': 'CM', 'msg': 'Object specified does not exist (object: cookie)'}}
        }
        responses.add(responses.DELETE, url, json=json_response, status=404)

        resp = self.client.slb.template.cookie_persistence.delete(T_NAME)

        self.assertIsNone(resp)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.DELETE)
        self.assertEqual(responses.calls[1].request.url, url)

    @responses.activate
    def test_slb_template_persistence_search(self):
        responses.add(responses.POST, AUTH_URL, json=self.get_auth_response())
        url = self.get_url(T_NAME)
        json_response = {
            'cookie-list': [{
                'name': T_NAME, 'dont-honor-conn-rules': 0, 'insert-always': 0, 'encrypt-level': 1,
                'encrypted': 'foo', 'cookie-name': 'sto-id', 'path': '/', 'pass-thru': 0, 'secure': 0, 'httponly': 0,
                'match-type': 0, 'uuid': '40143610-6a61-11e8-9bf6-c3c3b3edcd4e',
                'a10-url': '/axapi/v3/slb/template/persist/cookie/test1'}]
        }
        responses.add(responses.GET, url, json=json_response, status=200)

        resp = self.client.slb.template.cookie_persistence.get(T_NAME)

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.GET)
        self.assertEqual(responses.calls[1].request.url, url)

    @responses.activate
    def test_slb_template_persistence_search_not_found(self):
        responses.add(responses.POST, AUTH_URL, json=self.get_auth_response())
        url = self.get_url(T_NAME)
        json_response = {
            'response': {'status': 'fail', 'err': {
                'code': 1023460352, 'from': 'CM', 'msg': 'Object specified does not exist (object: cookie)'}}
        }
        responses.add(responses.GET, url, json=json_response, status=404)

        with self.assertRaises(acos_errors.NotFound):
            self.client.slb.template.cookie_persistence.get(T_NAME)

        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.GET)
        self.assertEqual(responses.calls[1].request.url, url)

    @responses.activate
    def test_slb_template_persistence_create_domain(self):
        # NOTE: Create method tries GET request to see if template exists before using POST request to create template.
        responses.add(responses.POST, AUTH_URL, json=self.get_auth_response())

        get_url = self.get_url(T_NAME)
        get_json_response = {
            'response': {'status': 'fail', 'err': {
                'code': 1023460352, 'from': 'CM', 'msg': 'Object specified does not exist (object: cookie)'}}
        }
        responses.add(responses.GET, get_url, json=get_json_response, status=404)
        post_url = SLB_URL
        post_json_response = {
            'cookie': {'name': T_NAME, 'dont-honor-conn-rules': 0, 'insert-always': 0, 'encrypt-level': 1,
                       'encrypted': 'foo', 'cookie-name': 'sto-id', 'path': '/', 'pass-thru': 0, 'secure': 0,
                       'httponly': 0, 'match-type': 0, 'uuid': '40143610-6a61-11e8-9bf6-c3c3b3edcd4e'}
        }
        responses.add(responses.POST, post_url, json=post_json_response, status=200)

        resp = self.client.slb.template.cookie_persistence.create(T_NAME, T_DOMAIN)

        self.assertIsNone(resp)
        self.assertEqual(len(responses.calls), 3)
        self.assertEqual(responses.calls[1].request.method, responses.GET)
        self.assertEqual(responses.calls[1].request.url, get_url)
        self.assertEqual(responses.calls[2].request.method, responses.POST)
        self.assertEqual(responses.calls[2].request.url, post_url)
