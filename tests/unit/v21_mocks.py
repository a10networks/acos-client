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

import acos_client


class MockPairClient(object):

    def __init__(self, parent, session_id=None):
        self.parent = parent
        self.session_id = session_id

    def __enter__(self):
        c = acos_client.Client('localhost', self.parent.username,
                               self.parent.password)
        c.http._http = self.parent.mock()
        c.session.http._http = c.http._http
        if self.session_id is not None:
            c.session.session_id = self.session_id

        return c

    def __exit__(self, *args, **kwargs):
        self.parent.post_validate()


class MockPair(object):

    def __init__(self, fields={}):
        self.fields = fields
        self.session_id = fields.get('session_id', 'session0')
        self.username = fields.get('username', 'defuser')
        self.password = fields.get('password', 'defpass')

    def client(self):
        return MockPairClient(self, session_id=None)

    def mock(self):
        self._mock = mock.MagicMock(return_value=json.dumps(self.output()))
        return self._mock

    def post_validate(self):
        pass


class AuthenticatedMockPair(MockPair):

    def client(self):
        return MockPairClient(self, session_id=self.session_id)


class Session(MockPair):

    def output(self):
        return {'session_id': self.session_id}

    def post_validate(self):
        self._mock.assert_called_once_with(
            'POST',
            '/services/rest/v2.1/?format=json&method=authenticate',
            json.dumps({'username': self.username, 'password': self.password}))


class SessionBadPassword(Session):

    def output(self):
        return {
            "response": {
                "status": "fail",
                "err": {"code": 520486915, "msg": " Admin password error"}
            }
        }


class Close(AuthenticatedMockPair):

    def output(self):
        return {"response": {"status": "OK"}}

    def post_validate(self):
        self._mock.assert_called_with(
            'POST',
            "/services/rest/v2.1/?format=json&method=session.close&"
            "session_id=%s" % self.session_id,
            json.dumps({'session_id': "%s" % self.session_id}))


class CloseBadSession(Close):

    def output(self):
        return {
            "response": {
                "status": "fail",
                "err": {"code": 1009, "msg": "Invalid session ID"}
            }
        }


class SystemInformation(AuthenticatedMockPair):

    def output(self):
        return {
            'system_information': {
                'advanced_core_os_on_compact_flash1': 'No Software',
                'advanced_core_os_on_compact_flash2': 'No Software',
                'advanced_core_os_on_harddisk1': '2.7.1-P3-AWS(build: 4)',
                'advanced_core_os_on_harddisk2': '2.7.1-P3-AWS(build: 4)',
                'aflex_engine_version': '2.0.0',
                'axapi_version': '2.1',
                'current_time': '03:25:47 IST Tue Jul 1 2014',
                'firmware_version': 'N/A',
                'last_config_saved': '06:25:26 GMT Sat Dec 28 2013',
                'serial_number': 'N/A',
                'software_version': '2.7.1-P3-AWS(build: 4)',
                'startup_mode': 'hard disk primary',
                'technical_support': 'www.a10networks.com/support '
            }
        }

    def post_validate(self):
        self._mock.assert_called_with(
            'GET',
            '/services/rest/v2.1/?format=json&method=system.information.get&'
            'session_id=%s' % self.session_id,
            None)
