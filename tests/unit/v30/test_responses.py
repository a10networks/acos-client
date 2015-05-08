# Copyright (C) 2015, A10 Networks Inc. All rights reserved.

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

import unittest
import uuid

from acos_client import errors as ae
from acos_client.v30 import responses as target


class TestResponse(unittest.TestCase):
    def _build_test_response(self, code, msg):
        return {
            "response": {
                "err": {
                    "code": code,
                    "msg": msg
                }
            }
        }

    def _test_raise_axapi_ex(self, response, method, api_url):
        self.assertRaises(ae.NotFound, target.raise_axapi_ex, response, method, api_url)

    def test_raise_axapi_ex_NotFound(self):
        not_found_codes = [1023443968, 1023475727, 1207959957, 520749062, 1023410176, 1023410181]
        # 1023410181 is a special case.  It matches on anything that's NOT DELETE and starts with
        # /axapi/v3/slb/service-group/.*/member/
        # That probably needs to be fixed and this test should break when it does
        test_obj = uuid.uuid4()
        test_url = "/axapi/v3/object/{0}".format(test_obj)
        test_method = "GET"
        test_msg = "Could not find object {0}".format(test_obj)

        for x in not_found_codes:
            test_response = self._build_test_response(x, test_msg)
            self._test_raise_axapi_ex(test_response, test_method, test_url)
