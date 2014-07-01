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


def session_mock(session_id="session0"):
    return mock.MagicMock(return_value=json.dumps({'session_id': session_id}))

def invalid_session_mock():
    return mock.MagicMock(return_value=json.dumps({
            "response": {
                "status": "fail", 
                "err": {"code": 1009, "msg": "Invalid session ID"}
            }
        }))

def mock_response_ok():
    return mock.MagicMock(return_value=json.dumps(
        {"response": {"status": "OK"}}))

class UnitTestBase(unittest.TestCase):

    def setUp(self):
        self.c = acos_client.Client('localhost', 'admin', 'xyz')
        # self.c.http_client._http = mock.MagicMock()
        # self.c.session.http_client._http = session_mock()
