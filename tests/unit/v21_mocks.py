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

import functools
import json
import mock

import acos_client


# def acos(mock_pair_instance):
#     def acos_decorator(func):
#         @functools.wraps(func)
#         def func_wrapper(*args):
#             k = args[0]
#             k.c.http_client._http = mock_pair_instance.mock()
#             k.c.session.http_client._http = k.c.http_client._http

#             func(*args)

#             mock_pair_instance.post_validate()

#         return func_wrapper
#     return acos_decorator


class MockPairClient(object):

    def __init__(self, parent):
        self.parent = parent

    def __enter__(self):
        c = acos_client.Client('localhost', self.parent._username,
                               self.parent._password)
        c.http_client._http = self.parent.mock()
        c.session.http_client._http = c.http_client._http
        return c

    def __exit__(self, *args, **kwargs):
        self.parent.post_validate()


class MockPair(object):

    def __init__(self, fields={}):
        self._fields = fields
        self._session_id = fields.get('session_id', 'session0')
        self._username = fields.get('username', 'defuser')
        self._password = fields.get('password', 'defpass')

    def client(self):
        return MockPairClient(self)

    def mock(self):
        self._mock = mock.MagicMock(return_value=json.dumps(self.output()))
        return self._mock

    def post_validate(self):
        pass


class Session(MockPair):

    def output(self):
        return {'session_id': self._session_id}

    def post_validate(self):
        print self._mock.mock_calls
        self._mock.assert_called_once_with(
            'POST',
            '/services/rest/v2.1/?format=json&method=authenticate',
            json.dumps({'username': self._fields['username'],
                        'password': self._fields['password']}))


class SessionBadPassword(Session):

    def output(self):
        return {
            "response": {
                "status": "fail", 
                "err": {"code": 520486915, "msg": " Admin password error"}
            }
        }


def Close(MockPair):

    def output(self):
        return {"response": {"status": "OK"}}

    def post_validate(self):
        self.c.session.http_client._http.assert_called_with(
            'POST',
            "/services/rest/v2.1/?format=json&method=session.close&"
            "session_id=abc",
            json.dumps({'session_id': 'abc'}))


# session_ok = {
#     'mock': mock.MagicMock(return_value=json.dumps(
#                 {'session_id': session_id})),
#     'results': 
# }
# def session_ok()



# def session_mock(session_id="session0"):
#     return mock.MagicMock(return_value=json.dumps({'session_id': session_id}))

# def invalid_session_mock():
#     return mock.MagicMock(return_value=json.dumps({
#             "response": {
#                 "status": "fail", 
#                 "err": {"code": 1009, "msg": "Invalid session ID"}
#             }
#         }))

# def mock_response_ok():
#     return mock.MagicMock(return_value=json.dumps(
#         {"response": {"status": "OK"}}))

# def bad_pass_mock():
#     return mock.MagicMock(return_value=json.dumps({
#             "response": {
#                 "status": "fail", 
#                 "err": {"code": 520486915, "msg": " Admin password error"}
#             }
#         }))

#         self.c.system.information()
#         self.assertEqual(2, self.c.http_client._http.call_count)
#         self.c.http_client._http.assert_called_with(
#             'GET',
#             '/services/rest/v2.1/?format=json&session_id=session0&'
#             'method=system.information.get',
#             None)
