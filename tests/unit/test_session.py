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

import json
import mock
import unittest

import acos_client
import test_base
import v21_mocks as mocks


def bad_pass_mock():
    return mock.MagicMock(return_value=json.dumps({
            "response": {
                "status": "fail", 
                "err": {"code": 520486915, "msg": " Admin password error"}
            }
        }))

class TestSession(unittest.TestCase):

    # def test_id(self):
    #     self.assertEqual(self.c.session.session_id, None)
    #     self.assertEqual(self.c.session.id, 'session0')

    # @mocks.acos(mocks.Session({'username': 'admin', 'password': 'xyz'}))
    # def test_id(self):
    #     self.assertEqual(self.c.session.session_id, None)
    #     self.assertEqual(self.c.session.id, 'session0')
    #     self.assertEqual(self.c.session.session_id, 'session0')

    def test_id(self):
        s = mocks.Session({'username': 'mongo', 'password': 'teddybear',
                           'session_id': 'fruitloops'})
        with s.client() as c:
            self.assertEqual(self.c.session.session_id, None)
            self.assertEqual(self.c.session.id, 'fruitloops')
            self.assertEqual(self.c.session.session_id, 'fruitloops')

    # def test_authenticate(self):
    #     self.c.session.authenticate('user', 'pass')
    #     self.c.session.http_client._http.assert_called_once_with(
    #         'POST',
    #         '/services/rest/v2.1/?format=json&method=authenticate',
    #         json.dumps({'username': 'user', 'password': 'pass'}))

    # @mocks.acos(mocks.Session({'username': 'user', 'password': 'clowncar'}))
    # def test_authenticate_with_mocker(self):
    #     r = self.c.session.authenticate('user', 'clowncar')
    #     self.assertEqual(r['session_id'], 'session0')

    ### AAA
    # @mocks.acos(mocks.Session({'username': 'user', 'password': 'clowncar'}))
    # def test_authenticate_with_mocker(self):
    #     r = self.c.session.authenticate('user', 'clowncar')

    ### BBB
    # def test_authenticate(self):
    #     self.mocks = mocks.Session({'username': 'panda', 'password': 'weak'})
    #     r = self.mocks.client().session.authenticate('panda', 'weak')
    #     self.mocks.post_validate()

    ### CCC
    def test_authenticate(self):
        s = mocks.Session({'username': 'panda', 'password': 'weak'})
        with s.client() as c:
            r = c.session.authenticate('panda', 'weak')
            self.assertNotEqual(r['session_id'], None)

    # def test_bad_authenticate(self):
    #     self.c.session.http_client._http = bad_pass_mock()
    #     self.assertEqual(self.c.session.session_id, None)
    #     try:
    #         self.c.session.authenticate('user', 'pass')
    #     except acos_client.errors.AuthenticationFailure:
    #         pass
    #     self.assertEqual(self.c.session.session_id, None)

    # @mocks.acos(mocks.SessionBadPassword({'username': 'user', 'password': 'pass'}))
    # def test_bad_authenticate(self):
    #     self.assertEqual(self.c.session.session_id, None)
    #     try:
    #         self.c.session.authenticate('user', 'pass')
    #     except acos_client.errors.AuthenticationFailure:
    #         pass
    #     self.assertEqual(self.c.session.session_id, None)

    # def test_close(self):
    #     self.c.session.http_client._http = test_base.session_mock('abc')
    #     self.c.session.authenticate('aaa', 'zzz')
    #     self.c.session.http_client._http = test_base.mock_response_ok()
    #     self.c.session.close()
    #     self.c.session.http_client._http.assert_called_with(
    #         'POST',
    #         "/services/rest/v2.1/?format=json&method=session.close&"
    #         "session_id=abc",
    #         json.dumps({'session_id': 'abc'}))
    #     self.assertEqual(self.c.session.session_id, None)

    # @mocks.acos(mocks.Close)
    # def test_close(self):
    #     self.c.session.http_client._http = test_base.session_mock('abc')
    #     self.c.session.authenticate('aaa', 'zzz')
    #     self.c.session.http_client._http = test_base.mock_response_ok()
    #     self.c.session.close()
    #     self.c.session.http_client._http.assert_called_with(
    #         'POST',
    #         "/services/rest/v2.1/?format=json&method=session.close&"
    #         "session_id=abc",
    #         json.dumps({'session_id': 'abc'}))
    #     self.assertEqual(self.c.session.session_id, None)


    # def test_close_and_authenticate(self):
    #     self.c.session.id
    #     self.c.session.close()
    #     self.c.session.id
    #     self.assertEqual(len(self.c.session.http_client._http.mock_calls), 3)

    # def test_close_with_bad_session_id(self):
    #     self.c.session.http_client._http = test_base.invalid_session_mock()
    #     self.c.session.close()
